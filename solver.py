from collections import namedtuple
from parser import parse, Warehouse, Problem, Order
from sys import argv
import math
from models import ActionType, Drone, Action

def distance(x, y):
    return math.sqrt((y[0] - x[0])**2 + (y[1] - x[1])**2)

def order_score(t, T):
    return (T - t) / (T * 100)

def score(actions):
    data = parse(argv[1])
    drones = [Drone(data.warehouses[0].row, data.warehouses[0].col, 0) for i in range(data.n_drones)]

    next_turn = 0

    res = 0
    for i in range(data.deadline):
        to_remove = []
        for action in actions:
            drone = drones[action.drone]
            # if the drone for this action is busy
            if drone.busy <= i:
                # get action destination
                if action.type == ActionType.LOAD:
                    row = data.warehouses[action.dest].row
                    col = data.warehouses[action.dest].col
                elif action.type == ActionType.DELIVER:
                    row = data.orders[action.dest].row
                    col = data.warehouses[action.dest].col
                # if drone is at destination, execute action
                if drone.row == row and drone.col == col:
                    drone.busy += 1
                    if action.type == ActionType.LOAD:
                        data.warehouses[action.dest].products[action.item] -= 1
                    elif action.type == ActionType.DELIVER:
                        data.orders[action.dest].products.remove(action.item)
                        if len(data.orders[action.dest].products) == 0:
                            res += order_score(i, deadline)
                    to_remove.append(action)
                else: # if drone is not at destination, move it to destination and change availibility
                    drone.busy = i + distance((drone.row, drone.col), (row, col))
                    drone.row = row
                    drone.col = col
        for action in to_remove:
            actions.remove(action)
    return res

    