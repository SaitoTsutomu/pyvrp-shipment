# flake8: noqa: S101
import pytest

from pyvrp_shipment import Order, Param, VehicleType_, solve


@pytest.fixture
def param():
    # position of node_xy is (x, y)
    duration = {
        "node00_node01": 2,
        "node00_node10": 2,
        "node01_node00": 2,
        "node01_node11": 2,
        "node01_node12": 3,
        "node10_node00": 2,
        "node10_node11": 2,
        "node10_node21": 3,
        "node11_node01": 2,
        "node11_node10": 2,
        "node11_node12": 2,
        "node11_node21": 2,
        "node12_node01": 3,
        "node12_node11": 2,
        "node12_node22": 2,
        "node21_node10": 3,
        "node21_node11": 2,
        "node21_node22": 2,
        "node22_node12": 2,
        "node22_node21": 2,
    }
    vehicle_type = VehicleType_(num_available=2, capacity=30, max_duration=36)
    orders = [
        Order("node00", "node10", 10, 5),
        Order("node11", "node01", 10, 5),
        Order("node21", "node22", 10, 5),
        Order("node01", "node00", 10, 5),
        Order("node11", "node21", 10, 5),
        Order("node22", "node12", 10, 5),
    ]
    return Param(duration, vehicle_type, orders)


def test_solve_success(param):
    result = solve(param, max_iterations=10, display=False)
    assert result.is_feasible()
    assert result.order_indexes == [[4, 2, 5], [1, 3, 0]]


def test_solve_lack_capacity(param):
    param.vehicle_type.capacity -= 1
    result = solve(param, max_iterations=10, display=False)
    assert not result.is_feasible()


def test_solve_lack_max_duration(param):
    param.vehicle_type.max_duration -= 1
    result = solve(param, max_iterations=10, display=False)
    assert not result.is_feasible()
