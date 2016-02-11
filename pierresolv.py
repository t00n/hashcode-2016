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

def main(file):
    commands = []
    prob = parse("data/" + file)
    orders = prob.orders
    i=0
    drone = 0
    while i < (prob.deadline/10):
        order = orders.pop()
        ordernbr = len(orders)
        prods = order.products
        if len(orders) < 1:
            break
        for prod in prods:

            wareNbr = -1

            j = 0
            for w in prob.warehouses:
                if w.products[prod] > 0:
                    wareNbr = j
                    w.products[prod] -=1
                j+=1
            if wareNbr == -1:
                break
            commands.append(str(drone) + " L "+str(wareNbr)+" "+str(prod)+" 1")
            commands.append(str(drone) + " D "+str(ordernbr)+" "+str(prod)+" 1")
            drone = (drone +1) % prob.n_drones
        i += 2


    f = open("sol"+file, "w")
    f.write(str(len(commands)) + "\n")
    for c in commands:
        f.write(c+ "\n")


if __name__ == '__main__':
    main("busy_day.in")
    main("mother_of_all_warehouses.in")
    main("redundancy.in")