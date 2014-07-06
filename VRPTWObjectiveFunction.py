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
from problemParser import parse_problem
from pyharmonysearch import ObjectiveFunctionInterface, harmony_search
import random
from bisect import bisect_left
from multiprocessing import cpu_count

class VRPTWObjectiveFunction(ObjectiveFunctionInterface):
    def __init__(self, arguments, problem_instance):
        self.problem_instance = problem_instance
        self.customer_number = problem_instance['customer_number']
        self.vehicle_number = problem_instance['vehicle_number']
        # x[i][j][k] = 1 iff vehicle k traveled from i to j
        # 0 otherwise
        number_of_variables = (self.customer_number + 1)**2 \
                * self.vehicle_number
        self._discrete_values = []
        self._variable = []
        for i in range(number_of_variables):
            self._discrete_values.append([0, 1])
            self._variable.append(True)

        #define all input parameters
        self._maximize = False #minimize
        self._max_imp = int(arguments['--ni']) #maximum number of improvisations
        self._hms = int(arguments['--hms']) #harmony memory size
        self._hmcr = float(arguments['--hmcr']) #harmony memory considering rate
        self._parmin = float(arguments['--parmin'])
        self._parmax = float(arguments['--parmax'])
        self._mpai = 1

        #TODO check, if par is used directly or via function
        self._par = 0.5 #pitch adjusting rate

    def ijk_to_index(self, i, j, k):
        index = i * self.vehicle_number * (self.customer_number + 1) + j * self.vehicle_number + k
        return index

    def index_to_ijk(index):
        pass

    def make_x_from_vector(self, vector):
        x = [[[0 for k in xrange(self.vehicle_number)] for j in xrange(self.customer_number + 1)] for i in xrange(self.customer_number + 1)]
        for i in range(self.customer_number + 1):
            for j in range(self.customer_number + 1):
                for k in range(self.vehicle_number):
                    x[i][j][k] = vector[self.ijk_to_index(i, j, k)]
        return x

    def get_fitness(self, vector):
        x = [[[0 for k in xrange(self.vehicle_number)] for j in xrange(self.customer_number + 1)] for i in xrange(self.customer_number + 1)]
        for i in range(self.customer_number + 1):
            for j in range(self.customer_number + 1):
                for k in range(self.vehicle_number):
                    x[i][j][k] = vector[self.ijk_to_index(i, j, k)]

        # check, if cars were in the same town
        for j in range(self.customer_number + 1):
            visited = False
            for i in range(self.customer_number + 1):
                for k in range(self.vehicle_number):
                    if x[i][j][k] == 1 and not visited:
                        visited = True
                    elif x[i][j][k] == 1 and visited:
                        # two cars visited city or one car visited city twice
                        return float("inf")
        # check, if all vechicles started from depot
        for k in range(self.vehicle_number):
            car_starts_from_depot = False
            for j in range(self.customer_number + 1):
                if x[0][j][k] == 1:
                    car_starts_from_depot = True
                    break
            if not car_starts_from_depot:
                return float("inf")

        max_time = 0
        for k in range(self.vehicle_number):
            time = 0
            for i in range(self.customer_number + 1):
                for j in range(self.customer_number + 1):
                    if x[i][j][k] == 1:
                        time += self.problem_instance['t'][i][j]
            if time > max_time:
                max_time = time

        return max_time




        #TODO write vectorize solution
        #TODO unvectorize
        #TODO implement fitness


        return 5.0

    def get_value(self, i, j=None):
        return random.randrange(2)

    def get_num_discrete_values(self, i):
        # there will be always 0 or 1
        return 2

    def get_index(self, i, v):
        # index of 0 is 0 and index of 1 is 1 in [0, 1]
        return v

    def is_variable(self, i):
        return self._variable[i]

    def is_discrete(self, i):
        # All variables are discrete
        return True

    def get_num_parameters(self):
        # compute number of parameters
        return len(self._discrete_values)

    def use_random_seed(self):
        # What ever that means :D
        return hasattr(self, '_random_seed') and self._random_seed

    def get_max_imp(self):
        return self._max_imp

    def get_hmcr(self):
        return self._hmcr

    def get_par(self):
        #TODO implement pitch adjustment rate accroding to http://scialert.net/qredirect.php?doi=jas.2013.633.638&linkid=pdf
        return self._par

    def get_hms(self):
        return self._hms

    def get_mpai(self):
        return self._mpai

    def get_mpap(self):
        #TODO remove, when it runs
        return 0.5

    def maximize(self):
        return self._maximize

from problemParser import parse_problem
from docopt import docopt
if __name__ == '__main__':
    arguments = docopt(__doc__)
    problem_instance = parse_problem(arguments['<problem_instance>'])
    obj_fun = VRPTWObjectiveFunction(arguments, problem_instance)
    num_processes = cpu_count() - 1 #use number of logical CPUs - 1 so that I have one available for use
    num_processes = 1
    num_iterations = 100
    (result, value) = (harmony_search(obj_fun, num_processes, num_iterations))
    print obj_fun.make_x_from_vector(result)
    print value
