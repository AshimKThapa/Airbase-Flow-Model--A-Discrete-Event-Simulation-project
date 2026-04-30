import numpy as np
import matplotlib.pyplot as plt
from airbase import Airbase
from env_vars import EnvVars
from scipy import stats

refuel_crew_util = []
maintenance_crew_util = []
total_eng_working_time = []
refueling_station_wait_time_means = []
mean_escort_delay_times = []
mean_deterrence_delay_times = []
mean_recon_delay_times = []
max_escort_delay_times = []
max_deterrence_delay_times = []
max_recon_delay_times = []

alpha = 0.05
n = EnvVars.reps
t_stat = stats.t.ppf(1-(alpha/2), n-1)

for rep in range(EnvVars.reps):
    print("rep: ", rep + 1, " / ", EnvVars.reps)
    airbase = Airbase(number_of_runways=1, num_refueling_stations=2, number_of_fighters=10, number_of_bombers=6,
                      number_of_uavs=8, fighter_engineer_team=2, bomber_engineer_team=2, uav_engineer_team=2)
    airbase.run()

    refuel_crew_utilization = airbase.refueling_station_time/(EnvVars.num_refueling_stations*EnvVars.sim_duration)
    refuel_crew_util.append(refuel_crew_utilization)
    print(f'Refueling Crew Utilization: '
          f'{airbase.refueling_station_time/(EnvVars.num_refueling_stations*EnvVars.sim_duration)}')

    engineer_teams = EnvVars.fighter_engineer_team + EnvVars.bomber_engineer_team + EnvVars.uav_engineer_team
    maintenance_crew_utilization = airbase.collective_engineer_working_time/(engineer_teams*EnvVars.sim_duration)
    maintenance_crew_util.append(maintenance_crew_utilization)
    print(f'Maintenance Crew Utilization: '
          f'{airbase.collective_engineer_working_time/(engineer_teams*EnvVars.sim_duration)}')
    total_eng_working_time.append(airbase.collective_engineer_working_time)
    print(airbase.collective_engineer_working_time)

    mean_refueling_station_wait_time = np.mean(airbase.refueling_station_delays)
    refueling_station_wait_time_means.append(mean_refueling_station_wait_time)
    print(f'Average time waiting for refueling station: {mean_refueling_station_wait_time}')

    mean_escort_delay_times.append(np.mean(airbase.escort_delay_times))
    mean_deterrence_delay_times.append(np.mean(airbase.deterrence_delay_times))
    mean_recon_delay_times.append(np.mean(airbase.recon_delay_times))

    max_escort_delay_times.append(np.max(airbase.escort_delay_times))
    max_deterrence_delay_times.append(np.max(airbase.deterrence_delay_times))
    max_recon_delay_times.append(np.mean(airbase.recon_delay_times))

    print("runways used for", airbase.runway_utilization, "hours")
    print("average runway delay:", np.average(airbase.runway_delays))

print(f'Mean deterrence mission delay time = {np.mean(mean_deterrence_delay_times)} (half-width = {t_stat*np.sqrt(np.var(mean_deterrence_delay_times)/n)})')
plt.hist(mean_deterrence_delay_times)
plt.show()
