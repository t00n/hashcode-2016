from solver import *
from parser import *
from models import *
from itertools import chain
from copy import deepcopy
from math import sqrt, ceil
from sys import stderr
from solver import score

Drone = namedtuple('Drone', ['id', 'row', 'col', 'busy'])


def distance(x1, y1, x2, y2):
    return ceil(sqrt((x1-x2)**2 + (y1-y2)**2))


def simulate(P):
    print >>stderr, len(P.orders), "orders"

    r, c = P.warehouses[0].col, P.warehouses[0].row
    W = deepcopy(P.warehouses)
    drones = [Drone(i, r, c, 0) for i in range(P.n_drones)]
    products = []
    for o in P.orders:
        for p in o.products:
            products.append((o, p))

    actions = {}

    def warehouse_with_prods(list_of_products):
        grouped = {}
        for p in list_of_products:
            grouped[p] = grouped.get(p, 0) + 1

        def f(w):
            for p, num in grouped.iteritems():
                if w.products[p] < num:
                    return False
            return True
        return filter(f, W)

    def products_in_order(order_id):
        def f():
            for p in products:
                if p[0].id == order_id:
                    yield p[1]
        return list(f())

    def where(product_id, r, c):
        """Return the nearest warehouse with product_id available"""
        has_prod = filter(lambda w: w.products[product_id] > 0, W)
        return sorted(has_prod, key=lambda w: distance(r, c, w.row, w.col))[0]

    for i in range(P.deadline):
        avail = list(filter(lambda x: x.busy <= i, drones))
        for d in avail:
            if len(products) == 0:
                break

            # find nearest WH with product
            o, first_prod = products.pop(0)

            # Find other products in the same order, and their weights
            in_order = products_in_order(o.id)
            weights = map(P.products.__getitem__, in_order)

            # Take all products the drone can carry
            while weights and P.products[first_prod] + sum(weights) >= P.max_payload:
                weights.pop()
            in_order = in_order[:len(weights)]

            # find a warehouse that has all the products
            while in_order and len(warehouse_with_prods([first_prod] + in_order)) == 0:
                in_order.pop()

            this_payload = [first_prod] + in_order

            w = warehouse_with_prods(this_payload)[0]

            products = products[len(in_order):]

            # goto warehouse
            b = d.busy + distance(w.row, w.col, d.row, d.col)
            for p in this_payload:
                actions[i] = actions.get(i, []) + [Action(d.id, ActionType.LOAD, p, w.id, 1)]
                W[w.id].products[p] -= 1
                assert W[w.id].products[p] >= 0

            # goto dest
            busy = b + distance(w.row, w.col, o.row, o.col)
            for p in this_payload:
                actions[b] = actions.get(b, []) + [Action(d.id, ActionType.DELIVER, p, o.id, 1)]

            drones[d.id] = Drone(d.id, o.row, o.col, busy)

    return list(chain(*map(actions.__getitem__, sorted(actions.keys()))))

if __name__ == "__main__":
    from sys import argv
    r = simulate(parse(argv[1]))
    print len(r)
    print "\n".join(map(str, r))
    # print >>stderr, score(r)
