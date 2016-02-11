from collections import namedtuple
from parser import parse, Warehouse, Problem, Order
from sys import argv, stderr
import math
from models import ActionType, Drone, Action

def distance(x, y):
    return math.sqrt((y[0] - x[0])**2 + (y[1] - x[1])**2)

def order_score(t, T):
    return ((T - t) / T) * 100

def score(actions):
    data = parse(argv[1])
    drones = [Drone(i, data.warehouses[0].row, data.warehouses[0].col, 0) for i in range(data.n_drones)]

    next_turn = 0

    res = 0
    i = 0
    for action in actions:
        if i > data.deadline:
            break
        drone = drones[action.drone]
        # if the drone for this action is not busy
        # get action destination
        if action.type == ActionType.LOAD:
            row = data.warehouses[action.dest].row
            col = data.warehouses[action.dest].col
        elif action.type == ActionType.DELIVER:
            row = data.orders[action.dest].row
            col = data.orders[action.dest].col
        if action.type == ActionType.DELIVER:
            data.orders[action.dest].products.remove(action.item)
            if len(data.orders[action.dest].products) == 0:
                res += order_score(i, data.deadline)
        drone.busy += distance((drone.row, drone.col), (row, col)) + 1
        i = min([d.busy for d in drones])
    return res

    