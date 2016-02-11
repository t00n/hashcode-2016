from solver import *
from parser import *
from models import *
from itertools import chain
from copy import deepcopy
from math import sqrt, ceil

Drone = namedtuple('Drone', ['id', 'row', 'col', 'busy'])


def distance(x1, y1, x2, y2):
    return ceil(sqrt((x1-x2)**2 + (y1-y2)**2))


def simulate(P):
    actions = []

    r, c = P.warehouses[0].col, P.warehouses[0].row
    W = deepcopy(P.warehouses)
    drones = [Drone(i, r, c, 0) for i in range(P.n_drones)]
    products = []
    for o in P.orders:
        for p in o.products:
            products.append((o, p))

    def where(product_id, r, c):
        """Return the nearest warehouse with product_id available"""
        has_prod = filter(lambda w: w.products[product_id] > 0, W)
        return sorted(has_prod, key=lambda w: distance(r, c, w.row, w.col))[0]

    for i in range(P.deadline):
        avail = filter(lambda x: x.busy <= i, drones)
        for d in avail:
            if len(products) == 0:
                break
            # find nearest WH with product
            order, p = products.pop(0)
            w = where(p, d.row, d.col)

            # goto warehouse
            busy = d.busy + distance(w.row, w.col, d.row, d.col)
            actions.append(Action(d.id, ActionType.LOAD, p, w.id, 1))

            # goto dest
            busy += distance(w.row, w.col, o.row, o.col)
            actions.append(Action(d.id, ActionType.DELIVER, p, o.id, 1))

            drones[d.id] = Drone(d.id, o.row, o.col, busy)

            wp = w.products
            wp[p] -= 1
            W[w.id] = Warehouse(w.id, w.row, w.col, wp)

    return actions

if __name__ == "__main__":
    from sys import argv
    print simulate(parse(argv[1]))