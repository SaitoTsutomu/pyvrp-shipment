from dataclasses import dataclass

from pyvrp import Model, Result
from pyvrp.stop import MaxIterations, MaxRuntime, MultipleCriteria


@dataclass
class VehicleType_:
    num_available: int
    capacity: int
    max_duration: int


@dataclass
class Order:
    from_: str
    to: str
    delivery: int
    service_duration: int


@dataclass
class Param:
    duration: dict[tuple[str, str], int]
    vehicle_type: VehicleType_
    orders: list[Order]
    big_duration: int = 2**52


@dataclass
class Result_:
    model: Model
    order_indexes: list[list[int]]
    result: Result

    def is_feasible(self) -> bool:
        return self.result.is_feasible()


def solve(param: Param, max_runtime=60, max_iterations=10000, **kwargs) -> Result_:
    duration = param.duration
    m = Model()
    xy = {"x": 0, "y": 0}
    depot = m.add_depot(**xy, name="depot")
    vt = param.vehicle_type
    m.add_vehicle_type(vt.num_available, vt.capacity, depot, max_duration=vt.max_duration)
    for od in param.orders:
        xy_sd = xy | {"service_duration": od.service_duration}
        fr = m.add_client(**xy_sd, name=od.from_)
        to = m.add_client(**xy_sd, delivery=od.delivery, name=od.to)
        m.add_edge(depot, fr, 0)
        _d = duration[f"{od.from_}_{od.to}"]
        m.add_edge(fr, to, _d, _d)
        m.add_edge(to, depot, 0)
    for to in m.locations[2::2]:
        for fr in m.locations[1::2]:
            _d = 0
            if to.name != fr.name:
                _d = duration.get(f"{to.name}_{fr.name}", param.big_duration)
            m.add_edge(to, fr, _d, _d)
    stop = MultipleCriteria([MaxRuntime(max_runtime), MaxIterations(max_iterations)])
    result = m.solve(stop, **kwargs)
    routes = []
    for route in result.best.routes():
        routes.append([i // 2 for i in route if i % 2])
    return Result_(m, routes, result)
