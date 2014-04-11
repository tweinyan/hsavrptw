#!/usr/bin/python
"""hsa

Usage:
    hsa.py <problem_instance> --hms=<hms> --hmcr=<hmcr> --parmax=<par> --parmin=<parmin> --ni=<ni>

Options:
    --hms=<hms>     Harmony memory size e.g. 10, 20, 30...
    --hmcr=<hmcr>   Harmony memory consideration rate e.g. 0.6, 0.7, 0.8
    --ni=<ni>       Number of improvisations e.g. 500, 1000, 2000
    --parxmax=<parmax>  Maximal pitch adjustment rate e.g. 0.9
    --parxmin=<parmin>  Minimal pitch adjustment rate e.g. 0.3

"""

def parse_line(line):
    return [int(item) for item in line.split()]

def get_problem_name(lines):
    return lines[0].rstrip()

def get_vehicle_number_and_capacity(lines):
    #in Solomon problems all the vehicles have the same capacity
    return parse_line(lines[4])

def not_empty_line(line):
    return line.split() != []

def get_customers(lines):
    return [parse_line(customer_line) for customer_line in lines[9:] if not_empty_line(customer_line)]

from math import sqrt
def distance(coords1, coords2):
    (x1, y1) = coords1
    (x2, y2) = coords2
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def parse_problem_lines(lines):
    """return dictionary containing problem variables"""
    problem_instance = {}
    [vehicle_number, capacity] = get_vehicle_number_and_capacity(lines)
    problem_instance['name'] = get_problem_name(lines)
    problem_instance['vehicle_number'] = vehicle_number
    problem_instance['capacity'] = capacity
    #naming as in "Harmony Search Algorith for Vehicle Rougint Problem with Time Windows"
    #Esam Taha Yassen et al.
    #http://scialert.net/qredirect.php?doi=jas.2013.633.638&linkid=pdf
    #t is travel time matrix t[0..customer_number][0..customer_number]
    #denoting travel time between t[i][j] (it is symmetric)
    #n is customer number (fixed to 100 in Solomon problem set)
    n = 100
    #q[i] is demand of customer c[i]
    #Q[k] is capacity of k th vevicle
    #s[i] is service duration of consumer c[i]
    #e[i] is starting time window for customer c[i]
    #l[i] is end time window for customer c[i]
    customer_list = []
    for customer in get_customers(lines):
        [number, xcoord, ycoord, demand, ready, due, servicetime] = customer
        customer_dict = {'number': number, 'coords': (xcoord, ycoord),\
                'demand': demand, 'ready': ready, 'due': due, 'servicetime': servicetime}
        customer_list.append(customer_dict)
    #initialize variables
    q = s = e = l = range(n+1)
    t = []
    for i in range(n+1):
        t.append(range(n+1))
    for i in range(n+1):
        q[i] = customer_list[i]['demand']
        s[i] = customer_list[i]['servicetime']
        e[i] = customer_list[i]['ready']
        l[i] = customer_list[i]['due']
        for j in range(n+1):
            t[i][j] = t[j][i] = distance(customer_list[i]['coords'], customer_list[j]['coords'])
    problem_instance['q'] = q
    problem_instance['s'] = s
    problem_instance['e'] = e
    problem_instance['l'] = l
    problem_instance['t'] = t
    problem_instance['n'] = n

    return problem_instance

def parse_problem(path_to_file):
    """read file and return dictionary containing problem variables"""
    with open(path_to_file, 'r') as f:
        lines = f.readlines()
        return parse_problem_lines(lines)

#create random solution
from random import shuffle
def pfih(problem_instance):
    n = problem_instance['n']
    v = problem_instance['vehicle_number']
    x = []
    for i in range(n+1):
        tmp1 = []
        for j in range(n+1):
            tmp2 = []
            for k in range(v):
                tmp2.append(0)
            tmp1.append(tmp2)
        x.append(tmp1)

    y = []
    for i in range(n+1):
        tmp1 = []
        for k in range(v):
            tmp1.append(0)
        y.append(tmp1)

    customers_to_serve = range(n+1)
    customers_to_serve.pop(0)
    shuffle(customers_to_serve)

    #take first customer and add to first route
    k = 0
    c = customers_to_serve.pop(0)
    x[0][c][k] = 1
    while customers_to_serve:
        #put c in the first route
        pass


    print customers_to_serve
    print n

def check_constraints(x, problem_instance):
    n = problem_instance['n']
    #(2) if vehicle travelled from i to j, it also served j
    for k in range(v):
        for j in range(n+1):
            total = 0
            for i in range(n+1):
                total = total + x[i][j][k]
            if total != y[j][k]:
                print "2"
                return False

    #(3) if vehicle travelled from i to j, it served i
    for k in range(v):
        for i in range(n+1):
            total = 0
            for j in range(n+1):
                total = total + x[i][j][k]
            if total != y[i][k]:
                print "3"
                return False

    #(4) vehicle capacity is not exceeded
    for k in range(v):
        total = 0
        for i in range(n+1):
            total = total + y[i][k] * q[i]
        if total > problem_instance['capacity']:
            print "4"
            return False
    #(5) each customer is served only once
    for i in range(n+1):
        total = 0
        for i in range(v):
            total = total + y[i][k]
        if total != 1:
            print "5"
            return False
    #(6) every vehicle starts from depot
    for k in range(v):
        if y[0][k] != v:
            print "6"
            return False
    #(7) next town is visited after first one is served
    for i in range(n+1):
        for j in range(n+1):
            if i != j:
                if a[i] + W[i] + s[i] + t[i][j] != a[j]:
                    print "7"
                    return False
    #(8) sevice is started in time window
    for i in range(n+1):
        if t[i] > e[i] or l[i] > t[i]:
            print "8"
            return False
    #(9) waiting time is either service start time - arriving time or 0
    for i in range(n+1):
        if W[i] != max(e[i] - a[i], 0):
            print "9"
            return False

    return True

#not finished
def f(t, x, n, v):
    """quality function, that we want to minimize - total travelled distance"""
    total = 0
    for i in range(n+1):
        for j in range(n+1):
            for k in range(v):
                total = t[i][j] * x[i][j][k]



from docopt import docopt
if __name__ == "__main__":
    arguments = docopt(__doc__)
    problem_instance = parse_problem(arguments['<problem_instance>'])
    hms = int(arguments['--hms'])
    hmcr = float(arguments['--hmcr'])
    parmax = float(arguments['--parmax'])
    parmin = float(arguments['--parmin'])
    ni = int(arguments['--ni'])
    generation = 0
    print parmax, parmin, ni
    #steps defined in "Harmony Search Algorith for Vehicle Rougint Problem with Time Windows"
    #Esam Taha Yassen et al.
    #http://scialert.net/qredirect.php?doi=jas.2013.633.638&linkid=pdf
    print pfih(problem_instance)
