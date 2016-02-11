from collections import namedtuple
from parser import parse, Warehouse, Problem, Order
from sys import argv

class Load: pass
class Deliver: pass
class Unload: pass
class Wait: pass

# = parse(argv[1])

Action = namedtuple('Action', ['drone', 'type', 'item', 'dest'])
#Drones = [(data.warehouses[0].row, data.warehouses[0].col) for i in range(data.n_drones)]

def main():
    commands = []
    prob = parse("data/busy_day.in")
    orders = prob.orders
    i=0
    while i < (prob.deadline/1000):
        order = orders.pop()
        ordernbr = len(orders)
        prod = order.products
        while len(prod) < 1:
            order = orders.pop()
            ordernbr = len(orders)
            prod = order.products

        wareNbr = -1

        j = 0
        for w in prob.warehouses:
            if w.products[prod[0]] > 0:
                wareNbr = j
                w.products[prod[0]] -=1
            j+=1
        if wareNbr == -1:
            break
        commands.append("0 L "+str(wareNbr)+" "+str(prod[0])+" 1")
        commands.append("0 D "+str(ordernbr)+" "+str(prod[0])+" 1")
        i+=1


    f = open("busy.txt", "w")
    f.write(str(len(commands)) + "\n")
    for c in commands:
        f.write(c+ "\n")


if __name__ == '__main__':
    main()