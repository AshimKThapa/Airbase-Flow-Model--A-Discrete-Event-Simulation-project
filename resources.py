import simpy
from simpy.core import BoundClass
from simpy.resources.resource import Resource, PriorityResource, PreemptiveResource

class Mission:
    def __init__(self, uid, name, fighters, bombers, uavs, flight):
        self.id = uid
        self.type = name
        self.fighters_needed = fighters
        self.bombers_needed = bombers
        self.uavs_needed = uavs
        self.flight_time = flight
        self.delay_times = []

    def __repr__(self):
        return f'{self.type} {self.id}'


class Fighter:
    def __init__(self, uid):
        self.id = uid
        self.hours_flown = 0
        self.type = "fighter"
        self.regular_maintenance_events = 0
        self.extended_maintenance_events = 0
        self.last_extended_maintenance_time = 0
        self.next_maintenance_time = 0
        self.maintenance_type = ""
        self.flight_times = []
        self.broken = False

    def __repr__(self):
        return f'fighter {self.id}'


class Bomber:
    def __init__(self, uid):
        self.id = uid
        self.hours_flown = 0
        self.type = "bomber"
        self.regular_maintenance_events = 0
        self.extended_maintenance_events = 0
        self.last_extended_maintenance_time = 0
        self.next_maintenance_time = 0
        self.maintenance_type = ""
        self.flight_times = []
        self.broken = False

    def __repr__(self):
        return f'bomber {self.id}'


class UAV:
    def __init__(self, uid):
        self.id = uid
        self.hours_flown = 0
        self.type = "uav"
        self.regular_maintenance_events = 0
        self.extended_maintenance_events = 0
        self.last_extended_maintenance_time = 0
        self.next_maintenance_time = 0
        self.maintenance_type = ""
        self.flight_times = []
        self.broken = False

    def __repr__(self):
        return f'UAV {self.id}'


class PriorityGet(simpy.resources.base.Get):

    def __init__(self, resource, priority=10, preempt=True):
        self.priority = priority
        """The priority of this request. A smaller number means higher
        priority."""

        self.preempt = preempt
        """Indicates whether the request should preempt a resource user or not
        (:class:`PriorityResource` ignores this flag)."""

        self.time = resource._env.now
        """The time at which the request was made."""

        self.usage_since = None
        """The time at which the request succeeded."""

        self.key = (self.priority, self.time, not self.preempt)
        """Key for sorting events. Consists of the priority (lower value is
        more important), the time at which the request was made (earlier
        requests are more important) and finally the preemption flag (preempt
        requests are more important)."""

        super().__init__(resource)


class PriorityBaseStore(simpy.resources.store.Store):
    GetQueue = simpy.resources.resource.SortedQueue

    get = BoundClass(PriorityGet)


class Runway:
    def __init__(self, uid):
        self.id = uid
        self.utilization = 0

    def __repr__(self):
        return f'runway {self.id}'
