import simpy
import numpy
import scipy
from scipy import stats
from env_vars import *
from resources import *


class Airbase():
    def __init__(self, number_of_runways, num_refueling_stations, number_of_fighters, number_of_bombers, number_of_uavs, fighter_engineer_team, bomber_engineer_team, uav_engineer_team):
        self.uav_engineer_team = uav_engineer_team
        self.bomber_engineer_team = bomber_engineer_team
        self.fighter_engineer_team = fighter_engineer_team
        self.num_refueling_stations = num_refueling_stations
        self.number_of_uavs = number_of_uavs
        self.number_of_bombers = number_of_bombers
        self.number_of_fighters = number_of_fighters
        self.number_of_runways = number_of_runways
        self.escort_mission_counter = 0
        self.det_mission_counter = 0
        self.recon_mission_counter = 0
        self.env = simpy.Environment()
        self.escort_delay_times = []
        self.deterrence_delay_times = []
        self.recon_delay_times = []

        self.collective_engineer_working_time = 0
        self.collective_engineer_delays = []

        self.refueling_station_time = 0
        self.refueling_station_delays = []

        self.runway_utilization = 0
        self.runway_delays = []
        self.runway_store = simpy.Store(self.env, self.number_of_runways)  # Runway represented as a Store
        for uid in range(self.number_of_runways):
            self.runway_store.items.append(Runway(uid + 1))

        # max number of fighters per refuel and maintenance is the number_of_fighters global variable
        self.fighters_maintenance_store = simpy.Store(self.env, self.number_of_fighters)
        self.fighters_store = PriorityBaseStore(self.env, self.number_of_fighters)
        for uid in range(self.number_of_fighters):
            self.fighters_store.items.append(Fighter(uid + 1))

        # max number of bombers per refuel and maintenance is the number_of_bombers global variable
        self.bombers_maintenance_store = simpy.Store(self.env, self.number_of_bombers)
        self.bombers_store = PriorityBaseStore(self.env, self.number_of_bombers)
        for uid in range(self.number_of_bombers):
            self.bombers_store.items.append(Bomber(uid + 1))

        # max number of uavs per refuel and maintenance is the number_of_bombers global variable
        self.uavs_maintenance_store = simpy.Store(self.env, self.number_of_uavs)
        self.uavs_store = PriorityBaseStore(self.env, self.number_of_uavs)
        for uid in range(self.number_of_uavs):
            self.uavs_store.items.append(UAV(uid + 1))

        plane_count = self.number_of_fighters + self.number_of_bombers + self.number_of_uavs
        self.plane_refuel_store = simpy.Store(self.env, plane_count)
        self.refuel_stations = simpy.Store(self.env, self.num_refueling_stations)
        for uid in range(self.num_refueling_stations):
            self.refuel_stations.items.append(uid + 1)

        # each engineer store holds one team of engineers
        self.fighter_engineer_store = simpy.Store(self.env, self.fighter_engineer_team)
        self.bomber_engineer_store = simpy.Store(self.env, self.bomber_engineer_team)
        self.uav_engineer_store = simpy.Store(self.env, self.uav_engineer_team)
        self.fighter_engineer_store.items.append(self.fighter_engineer_team)
        self.bomber_engineer_store.items.append(self.bomber_engineer_team)
        self.uav_engineer_store.items.append(self.uav_engineer_team)

    def command_and_control_escort_mission(self):
        while True:
            self.escort_mission_counter += 1

            mission = Mission(self.escort_mission_counter,
                              name='escort',
                              fighters=EnvVars.escort_num_fighters,
                              bombers=EnvVars.escort_num_bombers,
                              uavs=EnvVars.escort_num_uavs,
                              flight=EnvVars.escort_flight_time)

            yield self.env.process(self.process_mission(mission))

    def command_and_control_deterrence_mission(self):
        while True:
            self.det_mission_counter += 1

            mission = Mission(self.det_mission_counter,
                              name='deterrence',
                              fighters=EnvVars.deterrence_num_fighters,
                              bombers=EnvVars.deterrence_num_bombers,
                              uavs=EnvVars.deterrence_num_uavs,
                              flight=EnvVars.deterrence_flight_time)

            yield self.env.process(self.process_mission(mission))

    def command_and_control_recon_mission(self):
        while True:
            self.recon_mission_counter += 1

            mission = Mission(self.det_mission_counter,
                              name='recon',
                              fighters=EnvVars.recon_num_fighters,
                              bombers=EnvVars.recon_num_bombers,
                              uavs=EnvVars.recon_num_uavs,
                              flight=EnvVars.recon_flight_time)

            yield self.env.process(self.process_mission(mission))

    def process_mission(self, mission):
        request_time = self.env.now
        #print(self.simtime(), "| aircraft requested for ", mission)

        fighters = self.get_planes(mission.fighters_needed, self.fighters_store, mission.type)
        bombers = self.get_planes(mission.bombers_needed, self.bombers_store, mission.type)
        uavs = self.get_planes(mission.uavs_needed, self.uavs_store, mission.type)
        planes = sum([fighters, bombers, uavs], [])
        plane_objects = yield simpy.events.AllOf(self.env, planes)

        received_time = self.env.now
        #print(self.simtime(), "| aircraft received for ", mission)

        if mission.type == "escort":
            self.escort_delay_times.append(received_time - request_time)
        elif mission.type == "deterrence":
            self.deterrence_delay_times.append(received_time - request_time)
        elif mission.type == "recon":
            self.recon_delay_times.append(received_time - request_time)

        flight_time = mission.flight_time

        mission_failure = self.plane_breakdown(plane_objects, self.env.now, flight_time)
        #print(f"mission failed? {mission_failure}")
        #print(f'planes object has length {len(planes)} and is of type {type(planes)}')
        if mission_failure == True:
            for i in range(len(planes)):
                aircraft = planes[i].value
                if aircraft.broken == True:
                    if aircraft.type == 'fighter':
                        self.fighters_maintenance_store.put(aircraft)
                    elif aircraft.type == 'bomber':
                        self.bombers_maintenance_store.put(aircraft)
                    elif aircraft.type == 'uav':
                        self.uavs_maintenance_store.put(aircraft)

                elif aircraft.broken == False:
                    if aircraft.type == 'fighter':
                        self.fighters_store.put(aircraft)
                    elif aircraft.type == 'bomber':
                        self.bombers_store.put(aircraft)
                    elif aircraft.type == 'uav':
                        self.uavs_store.put(aircraft)
        else:
            #print(self.simtime(), "| started flying", mission, "sending planes to take off")

            # takeoff all planes
            for plane in plane_objects:
                # Request a runway for each plane
                runway = yield self.runway_store.get()
                self.env.process(self.takeoff(plane.value, runway, self.runway_store, EnvVars.takeoff_time))

            yield self.env.timeout(flight_time)

            # land all planes
            for plane in plane_objects:
                # Request a runway for each plane
                runway = yield self.runway_store.get()
                self.env.process(self.landing(plane.value, runway, self.runway_store, EnvVars.landing_time))

            #print(self.simtime(), "| finished flying", mission, ". Sending to be refueled")
            for plane in plane_objects:
                plane.value.hours_flown += flight_time
                self.plane_refuel_store.put(plane.value)

    def takeoff(self, aircraft, runway, runway_store, takeoff_time):
        #print(self.simtime(), '|', aircraft, 'requesting to take off at ', runway)
        runway_request = self.simtime()
        runway_usage = numpy.random.exponential(takeoff_time)
        yield self.env.timeout(runway_usage)  # Simulate the takeoff process
        runway_received = self.simtime()
        #print(self.simtime(), '|', aircraft, ' taking off at ', runway)
        self.runway_utilization += 1
        self.runway_delays.append(runway_received - runway_request)
        runway_store.put(runway)

    def landing(self, aircraft, runway, runway_store, landing_time):
        #print(self.simtime(), '|', aircraft, 'requesting to land at ', runway)
        runway_request = self.simtime()
        runway_usage = numpy.random.exponential(landing_time)
        yield self.env.timeout(runway_usage)  # Simulate the landing process
        runway_received = self.simtime()
        #print(self.simtime(), '|', aircraft, ' landing at ', runway)
        self.runway_utilization += 1
        self.runway_delays.append(runway_received - runway_request)
        runway_store.put(runway)

    def command_and_control_refuel(self, aircraft_store, maintenance_store, refuel_time):
        while True:
            # get aircraft
            aircraft = yield self.plane_refuel_store.get()
            station_request = self.env.now

            # get refueling station
            #print(self.simtime(), "|", aircraft, 'requested refueling crew')
            station = yield self.refuel_stations.get()
            station_received = self.env.now
            self.refueling_station_delays.append(station_received - station_request)
            #print(self.simtime(), "|", aircraft, 'received refueling crew. Starting refuel')

            refuel_length = numpy.random.exponential(refuel_time)
            yield self.env.timeout(refuel_length)
            #print(self.simtime(), "|", aircraft, "finished refueling")
            self.refueling_station_time += refuel_length
            self.refuel_stations.put(station)

            if self.needs_maintenance(aircraft):
                #print(self.simtime(), '| sending', aircraft, 'to maintenance')
                maintenance_store.put(aircraft)
            else:
                #print(self.simtime(), '| sending', aircraft, 'back to fly')
                aircraft_store.put(aircraft)

    @staticmethod
    def needs_maintenance(aircraft):
        current_regular_repair_count = aircraft.hours_flown // EnvVars.regular_maintenance_intervals[aircraft.type]
        current_extended_repair_count = aircraft.hours_flown // EnvVars.extended_maintenance_intervals[aircraft.type]
        if (current_regular_repair_count > aircraft.regular_maintenance_events) and (
                current_extended_repair_count < aircraft.extended_maintenance_events):
            ## need regular maintenance but not extended maintenance - just do regular maintenance
            aircraft.regular_maintenance_events += 1
            aircraft.next_maintenance_time = EnvVars.regular_maintenance_times[aircraft.type]
            aircraft.maintenance_type = 'regular'
            return True
        elif current_extended_repair_count > aircraft.extended_maintenance_events:
            ## need extended maintenance (regardless of regular maintenance need) - do extended mainteance
            aircraft.regular_maintenance_events += 1
            aircraft.extended_maintenance_events += 1
            aircraft.next_maintenance_time = EnvVars.extended_maintenance_times[aircraft.type]
            aircraft.maintenance_type = 'extended'
            return True
        else:
            return False

    def command_and_control_maintenance(self, maintenance_store, aircraft_store, engineer_store):
        while True:
            aircraft = yield maintenance_store.get()

            #print(self.simtime(), "| requesting engineer team for", aircraft)
            request_time = self.env.now
            engineer = yield engineer_store.get()
            received_time = self.env.now
            #print(self.simtime(), "| received engineer team for", aircraft, ". starting repair")

            self.collective_engineer_delays.append(received_time - request_time)
            maintenance_length = numpy.random.exponential(aircraft.next_maintenance_time)
            yield self.env.timeout(maintenance_length)
            #print(self.simtime(), "| finished repair for", aircraft)

            self.collective_engineer_working_time += maintenance_length
            engineer_store.put(engineer)

            if aircraft.maintenance_type == 'extended':
                aircraft.last_extended_maintenance_time = self.env.now

            aircraft.broken = False
            aircraft_store.put(aircraft)

    @staticmethod
    def get_planes(plane_count, store, mission_type):
        planes = []
        for _ in range(plane_count):
            planes.append(store.get(priority=EnvVars.mission_priority[mission_type]))
        return planes

    @staticmethod
    def plane_breakdown(planes, time, flight_time):
        broken_planes = 0
        for i in planes:
            aircraft = planes[i]
            time_since_maintenance = time - aircraft.last_extended_maintenance_time
            time_till_end_of_flight = time + flight_time
            break_probability = stats.expon.cdf(x=time_till_end_of_flight, scale=EnvVars.wing_break_rates[aircraft.type]) \
                                - stats.expon.cdf(x=time_since_maintenance, scale=EnvVars.wing_break_rates[aircraft.type])
            #print(f'break probability = {break_probability}')
            broken = stats.bernoulli.rvs(break_probability, size=1).item()
            if broken == 1:
                broken_planes += 1
                aircraft.broken = True
        if broken_planes >= 1:
            return True
        else:
            return False

    def simtime(self):
        return round(self.env.now, 3)

    def run(self):

        self.env.process(self.command_and_control_deterrence_mission())

        self.env.process(self.command_and_control_escort_mission())

        self.env.process(self.command_and_control_recon_mission())

        # create refuelling processes for each aircraft type
        for _ in range(EnvVars.num_refueling_stations):
            # fighter refueling process
            self.env.process(self.command_and_control_refuel(self.fighters_store,
                                                             self.fighters_maintenance_store,
                                                             EnvVars.fighter_refuel_time))
            # bomber refueling process
            self.env.process(self.command_and_control_refuel(self.bombers_store,
                                                             self.bombers_maintenance_store,
                                                             EnvVars.bomber_refuel_time))
            # UAV refueling process
            self.env.process(self.command_and_control_refuel(self.uavs_store,
                                                             self.uavs_maintenance_store,
                                                             EnvVars.uav_refuel_time))

        # create maintenance processes for each aircraft type
        for _ in range(EnvVars.num_maintenance_stations):
            # fighter maintenance process
            self.env.process(self.command_and_control_maintenance(self.fighters_maintenance_store,
                                                                  self.fighters_store,
                                                                  self.fighter_engineer_store))
            # bomber maintenance process
            self.env.process(self.command_and_control_maintenance(self.bombers_maintenance_store,
                                                                  self.bombers_store,
                                                                  self.bomber_engineer_store))
            # UAV maintenance process
            self.env.process(self.command_and_control_maintenance(self.uavs_maintenance_store,
                                                                  self.uavs_store,
                                                                  self.uav_engineer_store))

        self.env.run(until=EnvVars.sim_duration)
