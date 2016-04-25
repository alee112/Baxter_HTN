from __future__ import print_function
import copy
import sys
import pprint


class State():

    """A state is just a collection of variable bindings."""

    def __init__(self, name):
        self.__name__ = name


class Goal():

    """A goal is just a collection of variable bindings."""

    def __init__(self, name):
        self.__name__ = name

# Helper Function


def forall(seq, cond):
    for x in seq:
        if not cond(x):
            return False
    return True

# Helper Function


def find_if(cond, seq):
    for x in seq:
        if cond(x):
            return x
    return None

def find_all(cond, seq):
    matches = []
    for x in seq:
        if cond(x):
            matches.append[x]
    if len(matches) > 0:
        return matches
    else:
        return None

# Main planning class


class HTNPlanner():
    operators = {}
    methods = {}
    planningsteps = dict()
    result = []

    def __init__(self, name):
        self.__name__ = name

    def declare_operators(self, *op_list):
        self.operators.update({op.__name__: op for op in op_list})
        return self.operators

    def declare_methods(self, task_name, *method_list):
        self.methods.update({task_name: list(method_list)})
        return self.methods[task_name]

    def planner(self, state, tasks):
        self.result = self.seek_plan(state, tasks, [], 0)

    def seek_plan(self, state, tasks, plan, depth):
        if depth>50:
            return False
        if tasks == []:
            return plan
        task = tasks[0]
        if task[0] in self.operators:
            self.planningsteps[depth] = ['operator', task]
            #print('depth {} action {}'.format(depth,task))
            operator = self.operators[task[0]]
            newstate = operator(copy.deepcopy(state), *task[1:])
            if newstate:
                solution = self.seek_plan(
                    newstate, tasks[1:], plan + [task], depth + 1)
                if solution != False:
                    return solution
        if task[0] in self.methods:
            self.planningsteps[depth] = ['method', task]
            #print('depth {} method instance {}'.format(depth,task))
            relevant = self.methods[task[0]]
            for method in relevant:
                subtasks = method(state, *task[1:])
                if subtasks != False:
                    solution = self.seek_plan(
                        state, subtasks + tasks[1:], plan, depth + 1)
                    if solution != False:
                        return solution
        return False
