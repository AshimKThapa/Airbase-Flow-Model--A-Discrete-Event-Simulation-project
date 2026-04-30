# global environment variables:

class EnvVars:
    # times in hours
    escort_mission_interval = 8
    deterrence_mission_interval = 12
    escort_flight_time = 8
    deterrence_flight_time = 12
    recon_flight_time = 12

    number_of_fighters = 8
    number_of_bombers = 6
    number_of_uavs = 10

    fighter_refuel_time = 1
    bomber_refuel_time = 1.5
    uav_refuel_time = 1

    escort_num_fighters = 2
    escort_num_bombers = 1
    escort_num_uavs = 1

    deterrence_num_fighters = 2
    deterrence_num_bombers = 4
    deterrence_num_uavs = 0

    recon_num_fighters = 0
    recon_num_bombers = 0
    recon_num_uavs = 3

    # num_refueling_crews = 2
    num_maintenance_crews = 2

    fighter_engineer_team = 1
    bomber_engineer_team = 1
    uav_engineer_team = 1

    num_refueling_stations = 1
    num_maintenance_stations = 1

    number_of_runways = 2
    takeoff_time = 0.25  # 15 minutes
    landing_time = 0.25  # 15 minutes

    # maintenance_intervals = {'fighter': 25,
    #                          'bomber': 20,
    #                          'uav': 50}

    regular_maintenance_intervals = {'fighter': 40,
                                     'bomber': 30,
                                     'uav': 50}

    regular_maintenance_times = {'fighter': 5,
                                 'bomber': 8,
                                 'uav': 3}

    extended_maintenance_intervals = {'fighter': 300,
                                      'bomber': 250,
                                      'uav': 500}

    extended_maintenance_times = {'fighter': 15,
                                  'bomber': 24,
                                  'uav': 10}

    mission_priority = {'recon': 5,
                        'escort': 4,
                        'deterrence': 3}

    wing_break_rates = {'fighter': 150,
                        'bomber': 125,
                        'uav': 100}

    # sim_duration = 24 * 30 * 12
    reps = 100
    sim_duration = 24*30*12
