class ActionType:
    LOAD=0
    DELIVER=1
    UNLOAD=2
    WAIT=3

class Action:
    def __init__(self, drone, type, item, dest, time):
        self.drone = drone
        self.type = type
        self.item = item
        self.dest = dest
        self.time = time

class Drone:
    def __init__(self, row, col, busy):
        self.row = row
        self.col = col
        self.busy = busy

class Warehouse:
    def __init__(self, id, row, col, products):
        self.id = id
        self.row = row
        self.col = col
        self.products = products

class Order:
    def __init__(self, id, row, col, products):
        self.id = id
        self.row = row
        self.col = col
        self.products = products

class Problem:
    def __init__(self, *args):
        self.products, self.warehouses, self.orders, self.rows, self.cols, self.n_drones, self.deadline, self.max_payload = args