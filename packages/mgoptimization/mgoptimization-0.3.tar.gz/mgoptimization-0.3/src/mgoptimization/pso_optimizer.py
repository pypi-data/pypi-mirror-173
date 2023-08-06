from hybrids_pv import *
import pyswarms as ps
import numpy as np

def pso_optimizer(demand,
                  diesel_price,
                  hourly_ghi,
                  hourly_temp,
                  load_curve,
                  diesel_cost=261,  # diesel generator capital cost, USD/kW rated power
                  discount_rate=0.08,
                  n_chg=0.93,  # charge efficiency of battery
                  n_dis=1,  # discharge efficiency of battery
                  battery_cost=314, # battery capital capital cost, USD/kWh of storage capacity
                  pv_cost=660,  # PV panel capital cost, USD/kW peak power
                  pv_life=25,  # PV panel expected lifetime, years
                  diesel_life=10,  # diesel generator expected lifetime, years
                  pv_om=0.015,  # annual OM cost of PV panels
                  diesel_om=0.1,  # annual OM cost of diesel generator
                  inverter_cost=66,
                  inverter_life=20,
                  dod_max=0.9,  # maximum depth of discharge of battery
                  inv_eff=0.93,  # inverter_efficiency
                  charge_controller=142,
                  lpsp_max=0.02,  # maximum loss of load allowed over the year, in share of kWh
                  diesel_limit=0.5,
                  full_life_cycles=2500,
                  start_year=2020,
                  end_year=2030):

    # The following lines defines the solution space for the Particle Swarm Optimization (PSO) algorithm
    battery_bounds = [0, 5 * demand / 365]
    pv_bounds = [0, 5 * max(load_curve)]
    diesel_bounds = [0.5, max(load_curve)]
    min_bounds = np.array([pv_bounds[0], battery_bounds[0], diesel_bounds[0]])
    max_bounds = np.array([pv_bounds[1], battery_bounds[1], diesel_bounds[1]])
    bounds = (min_bounds, max_bounds)

    # The following lines set the search parameters for the PSO algorithm
    options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=3, options=options, bounds=bounds)

    #  This creates a series of the hour numbers (0-24) for one year
    hour_numbers = np.empty(8760)
    for i in prange(365):
        for j in prange(24):
            hour_numbers[i * 24 + j] = j

    def opt_func(X):
        n_particles = X.shape[0]
        lcoe = [find_least_cost_option(X[i], hourly_temp, hourly_ghi, hour_numbers,
                                       load_curve, inv_eff, n_dis, n_chg, dod_max, demand,
                                       diesel_price, end_year, start_year, pv_cost, charge_controller, pv_om,
                                       diesel_cost, diesel_om, inverter_life, inverter_cost, diesel_life, pv_life,
                                       battery_cost, discount_rate, lpsp_max, diesel_limit, full_life_cycles)
                                       for i in range(n_particles)]
        return np.array(lcoe)

    cost, pos = optimizer.optimize(opt_func, iters=1000)

    swarm_out = find_least_cost_option(pos, hourly_temp, hourly_ghi, hour_numbers,
                                         load_curve, inv_eff, n_dis, n_chg, dod_max, demand,
                                         diesel_price, end_year, start_year, pv_cost, charge_controller, pv_om,
                                         diesel_cost, diesel_om, inverter_life, inverter_cost, diesel_life, pv_life,
                                         battery_cost, discount_rate, lpsp_max, diesel_limit, full_life_cycles,
                                         simple=False, for_plots=True)

    return cost, pos, swarm_out


