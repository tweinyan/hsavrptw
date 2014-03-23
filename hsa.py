"""hsa

Usage:
    hsa.py <problem_instance>

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
    #naming as in "Harmony Search Algorith for Vehicle Rougint Problem with Time Windows
    #Esam Taha Yassen et al.
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

    return problem_instance

def parse_problem(path_to_file):
    """read file and return dictionary containing problem variables"""
    with open(path_to_file, 'r') as f:
        lines = f.readlines()
        return parse_problem_lines(lines)

from docopt import docopt
if __name__ == "__main__":
    arguments = docopt(__doc__)
    problem_instance = parse_problem(arguments['<problem_instance>'])
    print problem_instance

