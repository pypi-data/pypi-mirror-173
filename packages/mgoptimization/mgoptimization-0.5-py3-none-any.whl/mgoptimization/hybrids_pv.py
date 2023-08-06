import numpy as np
import pandas as pd
import numba
from numba import prange
import requests
import os
import json
import time


def get_pv_data(latitude, longitude, token, output_folder='None'):  # ToDo update to require  output folder
    api_base = 'https://www.renewables.ninja/api/'
    s = requests.session()
    # Send token header with each request
    s.headers = {'Authorization': 'Token ' + token}

    if output_folder == 'None':
        out_dir = os.getcwd() + '/../../pv_data'

        try:
            os.mkdir(out_dir)
        except FileExistsError:
            pass
    else:
        out_dir = output_folder

    out_path = os.path.join(out_dir, 'pv_data_lat_{}_long_{}.csv'.format(latitude, longitude))

    url = api_base + 'data/pv'

    args = {
        'lat': latitude,
        'lon': longitude,
        'date_from': '2020-01-01',
        'date_to': '2020-12-31',
        'dataset': 'merra2',
        'capacity': 1.0,
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': 35,
        'azim': 180,
        'format': 'json',
        'local_time': True,
        'raw': True
    }

    try:
        r = s.get(url, params=args)

        # Parse JSON to get a pandas.DataFrame of data and dict of metadata
        parsed_response = json.loads(r.text)

    except json.decoder.JSONDecodeError:
        print('API maximum hourly requests reached, waiting one hour', time.ctime())
        time.sleep(3700)
        print('Wait over, resuming API requests', time.ctime())
        r = s.get(url, params=args)

        # Parse JSON to get a pandas.DataFrame of data and dict of metadata
        parsed_response = json.loads(r.text)

    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')

    df_out = pd.DataFrame(columns=['time', 'ghi', 'temp'])
    df_out['ghi'] = (data['irradiance_direct'] + data['irradiance_diffuse']) * 1000
    df_out['temp'] = data['temperature']
    df_out['time'] = data['local_time']

    df_out.to_csv(out_path)


def read_environmental_data(path, skiprows=24, skipcols=1): # ToDo update skipcols or index in get_pv_data
    data = pd.read_csv(path, skiprows=skiprows)
    ghi_curve = data.iloc[:, 0 + skipcols].values
    temp = data.iloc[:, 1 + skipcols].values
    return ghi_curve, temp


@numba.njit
def self_discharge(battery_use, soc):
    # Battery self-discharge (0.02% per hour)
    return battery_use + 0.0002 * soc, soc - 0.0002 * soc


@numba.njit
def pv_generation(temp, ghi, pv_capacity, load, inv_eff):
    # Calculation of PV gen and net load
    k_t = 0.005  # temperature factor of PV panels
    t_cell = temp + 0.0256 * ghi  # PV cell temperature
    pv_gen = pv_capacity * 0.9 * ghi / 1000 * (1 - k_t * (t_cell - 25))  # PV generation in the hour
    net_load = load - pv_gen * inv_eff  # remaining load not met by PV panels
    return net_load, pv_gen


@numba.njit
def diesel_dispatch(hour, net_load, diesel_capacity, fuel_result, annual_diesel_gen, soc, inv_eff, n_dis, n_chg,
                    battery_size,
                    chg_max=1,  # Max share of battery capacity that can be charged in one hour
                    dschg_max=1,  # Max share of battery capacity that can be discharged in one hour
                    ):
    # Below is the dispatch strategy for the diesel generator as described in word document

    battery_dispatchable = soc * battery_size * n_dis * inv_eff
    max_discharge_simple = dschg_max * battery_size

    battery_dispatchable = min(battery_dispatchable, max_discharge_simple)

    battery_chargeable = (1 - soc) * battery_size / n_chg / inv_eff
    max_charge_simple = chg_max * battery_size

    battery_chargeable = min(battery_chargeable, max_charge_simple)

    if 4 < hour <= 17:
        # During the morning and day, the batteries are dispatched primarily.
        # The diesel generator, if needed, is run at the lowest possible capacity

        # Minimum diesel capacity to cover the net load after batteries.
        # Diesel generator limited by lowest possible capacity (40%) and rated capacity
        min_diesel = min(max(net_load - battery_dispatchable, 0.4 * diesel_capacity), diesel_capacity)

        if net_load > battery_dispatchable:
            diesel_gen = min_diesel
        else:
            diesel_gen = 0

    elif 17 > hour > 23:
        # During the evening, the diesel generator is dispatched primarily, at max_diesel.
        # Batteries are dispatched if diesel generation is insufficient.

        #  Maximum amount of diesel needed to supply load and charge battery
        # Diesel genrator limited by lowest possible capacity (40%) and rated capacity
        max_diesel = max(min(net_load + battery_chargeable, diesel_capacity), 0.4 * diesel_capacity)

        if net_load > 0:
            diesel_gen = max_diesel
        else:
            diesel_gen = 0

    else:
        # During night, batteries are dispatched primarily.
        # The diesel generator is used at max_diesel if load is larger than battery capacity

        # Maximum amount of diesel needed to supply load and charge battery
        # Diesel genrator limited by lowest possible capacity (40%) and rated capacity
        max_diesel = max(min(net_load + battery_chargeable, diesel_capacity), 0.4 * diesel_capacity)

        if net_load > battery_dispatchable:
            diesel_gen = max_diesel
        else:
            diesel_gen = 0

    if diesel_gen > 0:
        fuel_result = fuel_result + diesel_capacity * 0.08145 + diesel_gen * 0.246

    return fuel_result, annual_diesel_gen + diesel_gen, diesel_gen, net_load - diesel_gen


@numba.njit
def soc_and_battery_usage(net_load, diesel_gen, n_dis, inv_eff, battery_size, n_chg, battery_use, soc, hour, dod):

    hourly_battery_use = 0
    soc_prev = soc

    if net_load > 0:
        if diesel_gen > 0:
            # If diesel generation is used, but is smaller than load, battery is discharged
            soc = soc - net_load / n_dis / inv_eff / battery_size
        elif diesel_gen == 0:
            # If net load is positive and no diesel is used, battery is discharged
            soc = soc - net_load / n_dis / battery_size
    elif net_load < 0:
        if diesel_gen > 0:
            # If diesel generation is used, and is larger than load, battery is charged
            soc = soc - net_load * n_chg * inv_eff / battery_size
        if diesel_gen == 0:
            # If net load is negative, and no diesel has been used, excess PV gen is used to charge battery
            soc = soc - net_load * n_chg / battery_size

    # The amount of battery discharge in the hour is stored (measured in State Of Charge)
    if hour == 0:
        battery_use = 0
        dod = 0

    if net_load > 0:
        hourly_battery_use = min(net_load / n_dis / battery_size, soc_prev)
        battery_use = battery_use + min(net_load / n_dis / battery_size, soc_prev)
    else:
        battery_use = battery_use + min(0, soc)  # Unneccessary?

    return battery_use, soc, dod, hourly_battery_use


@numba.njit
def unmet_demand_and_excess_gen(unmet_demand, soc, n_dis, battery_size, n_chg, excess_gen, dod,
                                hour, dod_max, battery_use, remaining_load):

    if battery_size > 0:
        if soc < 0:
            # If State of charge is negative, that means there's demand that could not be met.
            unmet_demand = unmet_demand - soc / n_dis * battery_size
            soc = 0

        if soc > 1:
            # If State of Charge is larger than 1, that means there was excess PV/diesel generation
            excess_gen = excess_gen + (soc - 1) / n_chg * battery_size
            soc = 1
    else:
        if remaining_load > 0:
            unmet_demand = unmet_demand + remaining_load

        if remaining_load < 0:
            excess_gen = excess_gen - remaining_load

    # If he depth of discharge in the hour is lower than...
    if 1 - soc > dod:
        dod = 1 - soc

    return unmet_demand, soc, excess_gen, dod


@numba.njit
def hourly_optimization(battery_size, diesel_capacity, net_load, hour_numbers, inv_eff, n_dis, n_chg, dod_max,
                        energy_per_hh, full_life_cycles):
    fuel_result = 0
    battery_life = 0
    soc = 0.5
    unmet_demand = 0
    excess_gen = 0
    annual_diesel_gen = 0
    dod = 0
    battery_use = 0
    annual_battery_use = 0
    soc_array = []

    diesel_gen_curve = []
    battery_soc_curve = []

    for hour in hour_numbers:
        load = net_load[int(hour)]

        battery_use, soc = self_discharge(battery_use, soc)

        fuel_result, annual_diesel_gen, diesel_gen, load = diesel_dispatch(hour, load, diesel_capacity, fuel_result,
                                                                           annual_diesel_gen, soc, inv_eff, n_dis,
                                                                           n_chg, battery_size)
        if battery_size > 0:
            battery_use, soc, dod, hourly_battery_use = soc_and_battery_usage(load, diesel_gen, n_dis, inv_eff, battery_size, n_chg,
                                                                              battery_use, soc, hour, dod)
            annual_battery_use += hourly_battery_use

        unmet_demand, soc, excess_gen, dod = unmet_demand_and_excess_gen(unmet_demand, soc, n_dis,
                                                                                       battery_size, n_chg,
                                                                                       excess_gen, dod, hour,
                                                                                       dod_max, battery_use, load)

        soc_array.append(soc)
        diesel_gen_curve.append(diesel_gen)

        battery_soc_curve.append(soc)

    if (battery_size > 0) & (annual_battery_use > 0):
        battery_life_simple = round(full_life_cycles / annual_battery_use)  # Optimum case, 2500
        battery_life_simple = min(battery_life_simple, 20)
    else:
        battery_life_simple = 20

    condition = unmet_demand / energy_per_hh  # LPSP is calculated
    excess_gen = excess_gen / energy_per_hh
    diesel_share = annual_diesel_gen / energy_per_hh

    return diesel_share, battery_life_simple, condition, fuel_result, excess_gen, battery_soc_curve, diesel_gen_curve


@numba.njit
def calculate_hybrid_lcoe(diesel_price, end_year, start_year, energy_per_hh,
                          fuel_usage, pv_panel_size, pv_cost, charge_controller, pv_om, diesel_capacity, diesel_cost,
                          diesel_om, inverter_life, load_curve, inverter_cost, diesel_life, pv_life, battery_life,
                          battery_size, battery_cost, dod_max, discount_rate):

    # Necessary information for calculation of LCOE is defined
    project_life = end_year - start_year
    generation = np.ones(project_life) * energy_per_hh
    generation[0] = 0

    # Calculate LCOE
    sum_el_gen = 0
    investment = 0
    sum_costs = 0
    total_battery_investment = 0
    total_fuel_cost = 0
    total_om_cost = 0

    for year in prange(project_life + 1):
        salvage = 0
        inverter_investment = 0
        diesel_investment = 0
        pv_investment = 0
        battery_investment = 0

        fuel_costs = fuel_usage * diesel_price
        om_costs = (pv_panel_size * (pv_cost + charge_controller) * pv_om + diesel_capacity * diesel_cost * diesel_om)

        total_fuel_cost += fuel_costs / (1 + discount_rate) ** year
        total_om_cost += om_costs / (1 + discount_rate) ** year

        if year % inverter_life == 0:
            inverter_investment = max(load_curve) * inverter_cost  # Battery inverter
        if year % diesel_life == 0:
            diesel_investment = diesel_capacity * diesel_cost
        if year % pv_life == 0:
            pv_investment = pv_panel_size * (pv_cost + charge_controller + inverter_cost)  # PV inverter
        if year % battery_life == 0:
            battery_investment = battery_size * battery_cost / dod_max  # TODO Include dod_max here?

        if year == project_life:
            salvage = (1 - (project_life % battery_life) / battery_life) * battery_cost * battery_size / dod_max + \
                      (1 - (project_life % diesel_life) / diesel_life) * diesel_capacity * diesel_cost + \
                      (1 - (project_life % pv_life) / pv_life) * pv_panel_size * (pv_cost + charge_controller) + \
                      (1 - (project_life % inverter_life) / inverter_life) * max(load_curve) * inverter_cost

            total_battery_investment -= (1 - (project_life % battery_life) / battery_life) * battery_cost * battery_size / dod_max

        investment += diesel_investment + pv_investment + battery_investment + inverter_investment - salvage
        total_battery_investment += battery_investment

        sum_costs += (fuel_costs + om_costs + battery_investment + diesel_investment + pv_investment - salvage) / (
                (1 + discount_rate) ** year)

        if year > 0:
            sum_el_gen += energy_per_hh / ((1 + discount_rate) ** year)

    return sum_costs / sum_el_gen, investment, total_battery_investment, total_fuel_cost, total_om_cost


# @numba.njit
def find_least_cost_option(configuration, temp, ghi, hour_numbers, load_curve, inv_eff, n_dis, n_chg, dod_max,
                           energy_per_hh, diesel_price, end_year, start_year, pv_cost, charge_controller, pv_om,
                           diesel_cost, diesel_om, inverter_life, inverter_cost, diesel_life, pv_life, battery_cost,
                           discount_rate, lpsp_max, diesel_limit, full_life_cycles, simple=True, for_plots=False):

    pv = configuration[0]
    battery = configuration[1]
    diesel = configuration[2]

    net_load, pv_gen = pv_generation(temp, ghi, pv, load_curve, inv_eff)

    # For the number of diesel, pv and battery capacities the lpsp, battery lifetime, fuel usage and LPSP is calculated
    diesel_share, battery_life, lpsp, fuel_usage, excess_gen, battery_soc_curve, diesel_gen_curve = \
        hourly_optimization(battery, diesel, net_load, hour_numbers, inv_eff, n_dis, n_chg,
                            dod_max, energy_per_hh, full_life_cycles)
    if battery == 0:
        battery_life = 1
    else:
        battery_life = np.minimum(20, battery_life)

    if (battery_life == 0) or (lpsp > lpsp_max) or (diesel_share > diesel_limit):
        lcoe = 99
        investment = 0
        battery_investment = 0
        fuel_cost = 0
        om_cost = 0
    else:
        lcoe, investment, battery_investment, fuel_cost, om_cost = calculate_hybrid_lcoe(diesel_price, end_year, start_year, energy_per_hh,
                                                                     fuel_usage,
                                                                     pv, pv_cost, charge_controller, pv_om, diesel,
                                                                     diesel_cost, diesel_om, inverter_life, load_curve,
                                                                     inverter_cost, diesel_life, pv_life, battery_life,
                                                                     battery, battery_cost, dod_max, discount_rate)

    if simple:
        return lcoe
    elif for_plots:
        return load_curve, pv_gen, battery_soc_curve, diesel_gen_curve, battery, diesel_share
    else:
        return lcoe, lpsp, diesel_share, investment, battery_investment, fuel_cost, om_cost, battery, battery_life, pv + diesel, pv, diesel

@numba.njit
def calc_load_curve(tier, energy_per_hh):
    # the values below define the load curve for the five tiers. The values reflect the share of the daily demand
    # expected in each hour of the day (sum of all values for one tier = 1)
    tier5_load_curve = [0.021008403, 0.021008403, 0.021008403, 0.021008403, 0.027310924, 0.037815126,
                        0.042016807, 0.042016807, 0.042016807, 0.042016807, 0.042016807, 0.042016807,
                        0.042016807, 0.042016807, 0.042016807, 0.042016807, 0.046218487, 0.050420168,
                        0.067226891, 0.084033613, 0.073529412, 0.052521008, 0.033613445, 0.023109244]
    tier4_load_curve = [0.017167382, 0.017167382, 0.017167382, 0.017167382, 0.025751073, 0.038626609,
                        0.042918455, 0.042918455, 0.042918455, 0.042918455, 0.042918455, 0.042918455,
                        0.042918455, 0.042918455, 0.042918455, 0.042918455, 0.0472103, 0.051502146,
                        0.068669528, 0.08583691, 0.075107296, 0.053648069, 0.034334764, 0.021459227]
    tier3_load_curve = [0.013297872, 0.013297872, 0.013297872, 0.013297872, 0.019060284, 0.034574468,
                        0.044326241, 0.044326241, 0.044326241, 0.044326241, 0.044326241, 0.044326241,
                        0.044326241, 0.044326241, 0.044326241, 0.044326241, 0.048758865, 0.053191489,
                        0.070921986, 0.088652482, 0.077570922, 0.055407801, 0.035460993, 0.019946809]
    tier2_load_curve = [0.010224949, 0.010224949, 0.010224949, 0.010224949, 0.019427403, 0.034764826,
                        0.040899796, 0.040899796, 0.040899796, 0.040899796, 0.040899796, 0.040899796,
                        0.040899796, 0.040899796, 0.040899796, 0.040899796, 0.04601227, 0.056237219,
                        0.081799591, 0.102249489, 0.089468303, 0.06390593, 0.038343558, 0.017893661]
    tier1_load_curve = [0, 0, 0, 0, 0.012578616, 0.031446541, 0.037735849, 0.037735849, 0.037735849,
                        0.037735849, 0.037735849, 0.037735849, 0.037735849, 0.037735849, 0.037735849,
                        0.037735849, 0.044025157, 0.062893082, 0.100628931, 0.125786164, 0.110062893,
                        0.078616352, 0.044025157, 0.012578616]

    if tier == 1:
        load_curve = tier1_load_curve * 365
    elif tier == 2:
        load_curve = tier2_load_curve * 365
    elif tier == 3:
        load_curve = tier3_load_curve * 365
    elif tier == 4:
        load_curve = tier4_load_curve * 365
    else:
        load_curve = tier5_load_curve * 365

    return np.array(load_curve) * energy_per_hh / 365


def pv_diesel_hybrid(
        energy_per_hh,  # kWh/household/year as defined
        ghi,
        ghi_curve,
        temp,
        tier,
        start_year,
        end_year,
        diesel_price,
        max_cycles=950,  # cycles to failure at dod_max
        dod_max=0.9,  # maximum depth of discharge of battery
        diesel_cost=565,  # diesel generator capital cost, USD/kW rated power  # ToDo check
        pv_no=20,  # number of PV panel sizes simulated
        diesel_no=20,  # number of diesel generators simulated
        discount_rate=0.08,
        n_chg=0.93,  # charge efficiency of battery
        n_dis=1,  # discharge efficiency of battery
        lpsp_max=0.02,  # maximum loss of load allowed over the year, in share of kWh
        battery_cost=577, #314,  # battery capital capital cost, USD/kWh of storage capacity
        pv_cost=660, # 810,  # PV panel capital cost, USD/kW peak power
        pv_life=25,  # PV panel expected lifetime, years
        diesel_life=10,  # diesel generator expected lifetime, years
        pv_om=0.015,  # annual OM cost of PV panels
        diesel_om=0.1,  # annual OM cost of diesel generator
        inverter_cost=66, # 105,
        inverter_life=20,
        inv_eff=0.93, # 0.92  # inverter_efficiency
        charge_controller=142,
        battery_sizes=[0.5, 1, 2, 3],
        diesel_limit=0.5,
        array_output=False
):

    ghi = ghi_curve * ghi * 1000 / ghi_curve.sum()

    hour_numbers = np.empty(8760)
    for i in prange(365):
        for j in prange(24):
            hour_numbers[i * 24 + j] = j

    load_curve = calc_load_curve(tier, energy_per_hh)

    # This section creates the range of PV capacities, diesel capacities and battery sizes to be simulated
    ref = 5 * load_curve[19]
    pv_caps = []
    for i in prange(pv_no):
        pv_caps.append(ref * (i) / pv_no)

    if max(load_curve) < 0.5:
        diesel_caps = np.array([0.5])
    else:
        diesel_caps = np.linspace(0.5, max(load_curve), diesel_no).tolist()
        # step_size = math.ceil(max(load_curve) * 2 / diesel_no)
        # steps = math.ceil(max(load_curve) * 2 / step_size) + 1
        # diesel_caps = np.ones(steps) * step_size
        # for i in prange(steps):
        #     diesel_caps[i] = diesel_caps[i] * i * 0.5

    battery_sizes = np.array(battery_sizes) * energy_per_hh / 365  # [0.5 * energy_per_hh / 365, energy_per_hh / 365, 2 * energy_per_hh / 365]

    min_diesel_share = 0
    min_pv_capacity = 0
    min_diesel_capacity = 0
    min_lcoe = 99
    min_investment = 0
    min_battery_investment = 0
    min_fuel_cost = 0
    min_om_cost = 0

    if array_output:
        lcoe_array = np.zeros(shape=(len(battery_sizes), len(pv_caps), len(diesel_caps)), dtype=float)
        lpsp_array = np.ones(shape=(len(battery_sizes), len(pv_caps), len(diesel_caps)), dtype=float)

    p=-1
    b=-1
    d=-1

    for battery_capacity in battery_sizes:
        b += 1
        p = -1
        for pv_size in pv_caps:
            p+=1
            d = -1
            for diesel_size in diesel_caps:
                d+=1

                configuration = [pv_size, battery_capacity, diesel_size]

                lcoe, lpsp, diesel_share, investment, battery_investment, fuel_cost, om_cost,\
                    battery, battery_life, gen_capacity = find_least_cost_option(configuration,
                                                                              temp, ghi, hour_numbers,
                                                                              load_curve, inv_eff, n_dis, n_chg,
                                                                              dod_max, energy_per_hh, diesel_price,
                                                                              end_year, start_year, pv_cost,
                                                                              charge_controller, pv_om, diesel_cost,
                                                                              diesel_om, inverter_life, inverter_cost,
                                                                              diesel_life, pv_life, battery_cost,
                                                                              discount_rate, lpsp_max, diesel_limit,
                                                                              simple=False)

                if array_output & (lcoe < 99):  # ToDo check b, p, d
                    lcoe_array[b][p][d] = lcoe
                    lpsp_array[b][p][d] = lpsp

                if (lcoe < min_lcoe) & (lpsp < lpsp_max) & (diesel_share < diesel_limit):
                    min_battery_investment = battery_investment
                    min_diesel_share = diesel_share
                    min_lcoe = lcoe
                    min_investment = investment
                    min_pv_capacity = pv_size
                    min_diesel_capacity = diesel_size
                    min_battery = battery_capacity # * 365 / energy_per_hh
                    min_fuel_cost = fuel_cost
                    min_om_cost = om_cost

    if array_output:
        lcoe_array[lcoe_array == 0] = np.nan
        lpsp_array[lpsp_array == 1] = np.nan
        return min_lcoe, min_investment, min_pv_capacity, min_diesel_capacity, min_battery_investment, 1 - min_diesel_share, len(pv_caps) * len(battery_sizes) * len(diesel_caps), lcoe_array, pv_caps, diesel_caps, lpsp_array #battery_sizes
        # return min_lcoe, min_investment, min_pv_capacity, min_diesel_capacity, min_battery, 1 - min_diesel_share, len(pv_caps) * len(battery_sizes) * len(diesel_caps), lcoe_array, pv_caps, diesel_caps, battery_sizes
    else:
        return min_lcoe, min_investment, min_pv_capacity, min_diesel_capacity, min_battery_investment, 1 - min_diesel_share, len(pv_caps) * len(battery_sizes) * len(diesel_caps), min_fuel_cost, min_om_cost
        #return min_lcoe, min_investment, min_pv_capacity, min_diesel_capacity, min_battery, 1 - min_diesel_share, len(pv_caps) * len(battery_sizes) * len(diesel_caps)
