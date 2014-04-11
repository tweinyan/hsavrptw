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
from pyharmonysearch import ObjectiveFunctionInterface, harmony_search
import random
from bisect import bisect_left
from multiprocessing import cpu_count

class VRPTWObjectiveFunction(ObjectiveFunctionInterface):
    def __init__(self, arguments, problem_instance):

        #this will be 0 or 1, depending on vehicle n travelled directly from a to b
        self._lower_bounds = [-100, -100, -100, -100, -100]
        self._upper_bounds = [100, 100, 100, 100, 100]
        self._variable = [True, True, True, True, True]

        #define all input parameters
        self._maximize = False #minimize
        self._max_imp = int(arguments['--ni']) #maximum number of improvisations
        self._hms = int(arguments['--hms']) #harmony memory size
        self._hmcr = float(arguments['--hmcr']) #harmony memory considering rate
        self._parmin = float(arguments['--parmin'])
        self._parmax = float(arguments['--parmax'])

        #TODO check, if par is used directly or via function
        self._par = 0.5 #pitch adjusting rate

    def get_fitness(self, vector):
        #TODO write vectorize solution
        #TODO unvectorize
        #TODO implement fitness
        return abs(vector[0] + 2*vector[1] + 3*vector[2] + 2*vector[3]             - 19.968) + \
               abs(          -   vector[1] +   vector[2]                           + 1.15) + \
               abs(            2*vector[1] - 3*vector[2] +   vector[3]             - 4.624) + \
               abs(            3*vector[1] +   vector[2] + 2*vector[3] + vector[4] - 22.312) + \
               abs(                                        2*vector[3] + vector[4] - 15.882)

    def get_value(self, i, j=None):
        #TODO check, what does get_value do
        return random.uniform(self._lower_bounds[i], self._upper_bounds[i])

    def get_lower_bound(self, i):
        return 0

    def get_upper_bound(self, i):
        return 1

    def is_variable(self, i):
        #TODO check strange is_variable
        return self._variable[i]

    def is_discrete(self, i):
        #TODO change is_discrete to True, when it runs
        return False

    def get_num_parameters(self):
        #TODO compute number of parameters
        return len(self._lower_bounds)

    def use_random_seed(self):
        return False

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
    num_iterations = num_processes #each process does 1 iterations
    print(harmony_search(obj_fun, num_processes, num_iterations))
