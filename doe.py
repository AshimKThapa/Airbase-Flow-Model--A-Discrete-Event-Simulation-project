from itertools import product
import numpy as np
import pandas as pd
from env_vars import *
from scipy import stats
from airbase import Airbase
import matplotlib.pyplot as plt
import seaborn as sns
import time

runways = [1]
refueling_stations = [1,2]
fighters = [6, 8,10]
bombers = [4,6,8]
uavs = [8,10,12]
fighter_engineers = [1,2]
bomber_engineers = [1,2]
uav_engineers = [1,2]

design_list = [runways, refueling_stations, fighters, bombers, uavs, fighter_engineers, bomber_engineers, uav_engineers]
design = list(product(*design_list))
print(len(design))

alpha = 0.05
n = EnvVars.reps
t_stat = stats.t.ppf(1-(alpha/2), n-1)

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
runway_delays = []
runway_utilization = []
deterrence_delay_half_width = []
escort_delay_half_width = []
recon_delay_half_width = []

start = time.time()
for i in range(len(design)):
    print(f"{i + 1} / {len(design)}")

    number_of_runways = design[i][0]
    num_refueling_stations = design[i][1]
    number_of_fighters = design[i][2]
    number_of_bombers = design[i][3]
    number_of_uavs = design[i][4]
    fighter_engineer_team = design[i][5]
    bomber_engineer_team = design[i][6]
    uav_engineer_team = design[i][7]

    design_refuel_crew_util = []
    design_maintenance_crew_util = []
    design_total_eng_working_time = []
    design_refueling_station_wait_time_means = []
    design_mean_escort_delay_times = []
    design_mean_deterrence_delay_times = []
    design_mean_recon_delay_times = []
    design_max_escort_delay_times = []
    design_max_deterrence_delay_times = []
    design_max_recon_delay_times = []
    design_runway_delays = []
    design_runway_utilization = []

    for j in range(n):

        airbase = Airbase(number_of_runways,
                          num_refueling_stations,
                          number_of_fighters,
                          number_of_bombers,
                          number_of_uavs,
                          fighter_engineer_team,
                          bomber_engineer_team,
                          uav_engineer_team)
        airbase.run()
        # refueling crew stats
        design_refuel_crew_utilization = airbase.refueling_station_time / (
                EnvVars.num_refueling_stations * EnvVars.sim_duration)
        design_refuel_crew_util.append(design_refuel_crew_utilization)
        # engineer teams stats
        design_engineer_teams = fighter_engineer_team + bomber_engineer_team + uav_engineer_team
        maintenance_crew_utilization = airbase.collective_engineer_working_time / (
                design_engineer_teams * EnvVars.sim_duration)
        design_maintenance_crew_util.append(maintenance_crew_utilization)
        design_total_eng_working_time.append(airbase.collective_engineer_working_time)
        # refueling wait times
        if len(airbase.refueling_station_delays) == 0:
            refueling_wait = 0
        else:
            refueling_wait = np.mean(airbase.refueling_station_delays)
        if np.isnan(refueling_wait):
            refueling_wait = 0
        design_refueling_station_wait_time_means.append(refueling_wait)
        # mission wait times
        if len(airbase.escort_delay_times) == 0:
            escort_delay = 0
        else:
            escort_delay = np.mean(airbase.escort_delay_times)
        if np.isnan(escort_delay):
            escort_delay = 0
        design_mean_escort_delay_times.append(escort_delay)
        # print(f'{airbase.escort_delay_times} = escort mission delay times')
        if len(airbase.deterrence_delay_times) == 0:
            deterrence_delay_time = 0
        else:
            deterrence_delay_time = np.mean(airbase.deterrence_delay_times)
        if np.isnan(deterrence_delay_time):
            deterrence_delay_time = 0
        design_mean_deterrence_delay_times.append(deterrence_delay_time)
        if len(airbase.recon_delay_times) == 0:
            recon_delay_time = 0
        else:
            recon_delay_time = np.mean(airbase.recon_delay_times)
        if np.isnan(recon_delay_time):
            recon_delay_time = 0
        design_mean_recon_delay_times.append(recon_delay_time)
        # runway statistics
        if len(airbase.runway_delays) == 0:
            runway_delay = 0
        else:
            runway_delay = np.mean(airbase.runway_delays)
        if np.isnan(runway_delay):
            runway_delay = 0
        design_runway_delays.append(runway_delay)
        runway_utilization_rate = airbase.runway_utilization / EnvVars.sim_duration
        design_runway_utilization.append(runway_utilization_rate)

    if np.isnan(np.mean(design_refuel_crew_util)):
        design_refuel_crew_util = 0
        refuel_crew_util.append(design_refuel_crew_util)
    else:
        refuel_crew_util.append(np.mean(design_refuel_crew_util))

    if np.isnan(np.mean(design_maintenance_crew_util)):
        design_maintenance_crew_util = 0
        maintenance_crew_util.append(design_maintenance_crew_util)
    else:
        maintenance_crew_util.append(np.mean(design_maintenance_crew_util))

    if np.isnan(np.mean(design_total_eng_working_time)):
        design_total_eng_working_time = 0
        total_eng_working_time.append(design_total_eng_working_time)
    else:
        total_eng_working_time.append(np.mean(design_total_eng_working_time))

    if np.isnan(np.mean(design_refueling_station_wait_time_means)):
        design_refueling_station_wait_time_means = 0
        refueling_station_wait_time_means.append(design_refueling_station_wait_time_means)
    else:
        refueling_station_wait_time_means.append(np.mean(design_refueling_station_wait_time_means))

    if np.isnan(np.mean(design_mean_escort_delay_times)):
        design_mean_escort_delay_times = 0
        mean_escort_delay_times.append(design_mean_escort_delay_times)
    else:
        mean_escort_delay_times.append(np.mean(design_mean_escort_delay_times))

    if np.isnan(np.mean(design_mean_deterrence_delay_times)):
        design_mean_deterrence_delay_times = 0
        mean_deterrence_delay_times.append(design_mean_deterrence_delay_times)
    else:
        mean_deterrence_delay_times.append(np.mean(design_mean_deterrence_delay_times))

    if np.isnan(np.mean(design_mean_recon_delay_times)):
        design_mean_recon_delay_times = 0
        mean_recon_delay_times.append(design_mean_recon_delay_times)
    else:
        mean_recon_delay_times.append(np.mean(design_mean_recon_delay_times))

    if np.isnan(np.mean(design_max_escort_delay_times)):
        design_max_escort_delay_times = 0
        max_escort_delay_times.append(design_max_escort_delay_times)
    else:
        max_escort_delay_times.append(np.mean(design_max_escort_delay_times))

    if np.isnan(np.mean(design_max_deterrence_delay_times)):
        design_max_deterrence_delay_times = 0
        max_deterrence_delay_times.append(design_max_deterrence_delay_times)
    else:
        max_deterrence_delay_times.append(np.mean(design_max_deterrence_delay_times))

    if np.isnan(np.mean(design_max_recon_delay_times)):
        design_max_recon_delay_times = 0
        max_recon_delay_times.append(design_max_recon_delay_times)
    else:
        max_recon_delay_times.append(np.mean(design_max_recon_delay_times))

    if np.isnan(np.mean(design_runway_delays)):
        design_runway_delays = 0
        runway_delays.append(design_runway_delays)
    else:
        runway_delays.append(np.mean(design_runway_delays))

    if np.isnan(np.mean(design_runway_utilization)):
        design_runway_utilization = 0
        runway_utilization.append(design_runway_utilization)
    else:
        runway_utilization.append(np.mean(design_runway_utilization))

    dd_hw = t_stat * (np.std(design_mean_deterrence_delay_times) / np.sqrt(n))
    deterrence_delay_half_width.append(dd_hw)
    # print(f"Deterrence delay half-width = {dd_hw}")

    escort_hw = t_stat * (np.std(design_mean_escort_delay_times) / np.sqrt(n))
    escort_delay_half_width.append(escort_hw)
    # print(f"Escort delay half-width = {escort_hw}")

    recon_hw = t_stat * (np.std(design_mean_recon_delay_times) / np.sqrt(n))
    recon_delay_half_width.append(recon_hw)
    # print(f"Recon delay half-width = {recon_hw}")

end = time.time()
print(f"Simulation complete (runtime: {(end - start) / 60 / 60})")

print(f"Maximum refueling crew utilization design: {np.argmax(refuel_crew_util)}")

print(f"Maximum maintenance crew utilization design: {np.argmax(maintenance_crew_util)}")

print(f"Minimum refueling station wait time design: {np.argmin(refueling_station_wait_time_means)}")

print(f"Minimum escort mission delay design: {np.argmin(mean_escort_delay_times)}")

print(f"Minimum deterrence mission delay design: {np.argmin(mean_deterrence_delay_times)}")

print(f"Minimum recon mission delay design: {np.argmin(mean_recon_delay_times)}")

print(f"Minimum runway utilization design: {np.argmin(runway_delays)}")

print(f"Maximum runway utilization design: {np.argmax(runway_utilization)}")

# Create a grouped boxplot
plt.scatter(refuel_crew_util, mean_deterrence_delay_times)
plt.xlabel('Refueling Crew Utilization', fontsize=16)
plt.ylabel('Deterrence Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
plt.scatter(refuel_crew_util, mean_escort_delay_times)
plt.xlabel('Refueling Crew Utilization', fontsize=16)
plt.ylabel('Escort Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
plt.scatter(refuel_crew_util, mean_recon_delay_times)
plt.xlabel('Refueling Crew Utilization', fontsize=16)
plt.ylabel('Recon Delays', fontsize=16)
plt.show()

engineer_crews = [design[i][5] + design[i][6] + design[i][7] for i in range(len(design))]

engineer_util = [i/EnvVars.sim_duration/engineer_crews[i] for i in range(len(total_eng_working_time))]

# Create a grouped boxplot
plt.scatter(engineer_util, mean_deterrence_delay_times)
plt.xlabel('Engineer Crew Utilization', fontsize=16)
plt.ylabel('Deterrence Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
plt.scatter(engineer_util, mean_escort_delay_times)
plt.xlabel('Engineer Crew Utilization', fontsize=16)
plt.ylabel('Escort Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
plt.scatter(engineer_util, mean_recon_delay_times)
plt.xlabel('Engineer Crew Utilization', fontsize=16)
plt.ylabel('Recon Delays', fontsize=16)
plt.show()

fighter_designs = [design[i][2] for i in range(len(design))]
bomber_designs = [design[i][3] for i in range(len(design))]
uav_designs = [design[i][4] for i in range(len(design))]

design_df = pd.DataFrame(list(zip(bomber_designs, fighter_designs, uav_designs, mean_deterrence_delay_times, mean_escort_delay_times, mean_recon_delay_times)),
                        columns=['No. of bombers', 'No. of fighters', 'No. of UAVs','Deterrence Mission Delays', 'Escort Mission Delays', 'Recon Mission Delays'])
design_df.to_csv('doe_results.csv')

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Create a grouped boxplot
sns.boxplot(x=design_df['No. of fighters'], y=design_df['Escort Mission Delays'])
plt.xlabel('Fighters', fontsize=16)
plt.ylabel('Escort Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
sns.boxplot(x=design_df['No. of bombers'], y=design_df['Escort Mission Delays'])
plt.xlabel('Bombers', fontsize=16)
plt.ylabel('Escort Delays', fontsize=16)
plt.show()

# Create a grouped boxplot
sns.boxplot(x=design_df['No. of UAVs'], y=design_df['Escort Mission Delays'])
plt.xlabel('UAVs', fontsize=16)
plt.ylabel('Escort Delays', fontsize=16)
plt.show()



