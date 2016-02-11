#!/usr/bin/env python2

from sys import argv
from collections import namedtuple

from models import Action, Warehouse, Order, Problem 

def parse(filename):
    with open(filename) as f:
        r = lambda: f.readline().strip()

        rows, cols, drones, deadline, max_payload = map(int, r().split())
        n_products = int(r())
        Products = map(int, r().split())

        assert n_products == len(Products)

        n_warehouses = int(r())
        warehouses = []
        for w in range(n_warehouses):
            row, col = map(int, r().split())
            products = map(int, r().split())
            warehouses.append(Warehouse(w, row, col, products))

        n_orders = int(r())
        orders = []
        for i in range(n_orders):
            row, col = map(int, r().split())
            _ = int(r())
            products = map(int, r().split())
            orders.append(Order(i, row, col, products))

        return Problem(Products, warehouses, orders, rows, cols,
                       drones, deadline, max_payload)

if __name__ == "__main__":
    print parse(argv[1])
