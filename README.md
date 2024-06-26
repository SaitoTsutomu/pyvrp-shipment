# pyvrp-shipment

`pyvrp-shipment` is a package for wrapper for solving shipment in PyVRP.
https://pyvrp.org/

## Installation

```
pip install pyvrp-shipment
```

## Example

```python
from pyvrp_shipment import Order, Param, VehicleType_, solve

duration = {"nd1_nd2": 16}
vehicle_type = VehicleType_(num_available=1, capacity=10, max_duration=16 + 3 * 2)
orders = [Order("nd1", "nd2", delivery=10, service_duration=3)]
param = Param(duration, vehicle_type, orders)
result = solve(param, max_iterations=100, display=False)
if result.is_feasible():
    print(result.result)
    print("route =", result.order_indexes)
```

```
Solution results
================
    # routes: 1
   # clients: 2
   objective: 16.00
# iterations: 100
    run-time: 0.06 seconds

Routes
------
Route #1: 1 2 

route = [[0]]
```
