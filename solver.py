from collections import namedtuple
from parser import parse, Warehouse, Problem, Order
from sys import argv

class Load: pass
class Deliver: pass
class Unload: pass
class Wait: pass

data = parse(argv[1])

Action = namedtuple('Action', ['drone', 'type', 'item', 'dest'])
Drones = [(data.warehouses[0].row, data.warehouses[0].col) for i in range(data.n_drones)]

def score(actions):
    pass
    