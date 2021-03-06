#!/usr/bin/env python
import random
import sys
from HTN import *
import argparse

try:
    import rospy
    from baxter_pickup_msgs.msg import Plan
    from baxter_pickup_msgs.msg import Step
except:
    print("Failed to Load ROS and ROS Messages")

try:
    import cmsc_tests
except:
    print("")

"""Each planning operator is a Python function. The 1st argument is
the current state, and the others are the planning operator's usual arguments.
This is analogous to how methods are defined for Python classes (where
the first argument is always the name of the class instance). For example,
the function pickup(state,b) implements the planning operator for the task
('pickup', b).

The Baxter World operators use two state variables:
- pos[b] = block b's position, which may be 'table', 'handL',  or 'handR'.
- holdingL and holdingR = name of the block being held in each hand, or False if the hand is empty.
"""


def pickup(state, b, hand):
    if hand == 'right' and (state.pos[b] == 't2' or state.pos[b] == 'center') and state.holdingR == False:
        if state.pos[b] == 't2':
            state.delete['t2'] = True
        state.holdingR = b
        state.pos[b] = 'right'
        return state
    elif hand == 'left' and (state.pos[b] == 't1' or state.pos[b] == 'center') and state.holdingL == False:
        if state.pos[b] == 't1':
            state.delete['t1'] = True
        state.holdingL = b
        state.pos[b] = 'left'
        return state
    else:
        return False
    

def place(state, b, dest, hand):
    if dest == 'center': 
        if state.pos[b] == 'right':
            state.holdingR = False
        elif state.pos[b] == 'left':
            state.holdingL = False
        state.pos[b] = dest
        return state
    elif dest == 't1':
        if state.pos[b] == 'left' and state.delete['t1']:
            state.holdingL = False
            state.pos[b] = dest
            state.delete['t1'] = False
            return state
    elif dest == 't2':
        if state.pos[b] == 'right' and state.delete['t2']:
            state.holdingR = False
            state.pos[b] = dest
            state.delete['t2'] = False
            return state
    else:
        return False


# methods for "move_blocks"
def moveb_m(state, goal):
    for b in state.pos:
        if state.pos[b] == goal.pos[b]:
            continue
        elif goal.pos[b] == 'center' and state.pos[b] == 't1':
            return [('move_one', ''+b, 'center', 'left'), ('move_blocks', goal)]
        elif goal.pos[b] == 'center' and state.pos[b] == 't2':
            return [('move_one', ''+b, 'center', 'right'), ('move_blocks', goal)]
        elif goal.pos[b] == 't1' and state.pos[b] == 't2':
            return [('move_one', ''+b, 'center', 'right'), ('move_blocks', goal)]
        elif goal.pos[b] == 't2' and state.pos[b] == 't1':
            return [('move_one', ''+b, 'center', 'left'), ('move_blocks', goal)]  
        elif goal.pos[b] == 't1' and state.pos[b] == 'center' and state.delete['t1']:
            return [('move_one', ''+b, 't1', 'left'), ('move_blocks', goal)]
        elif goal.pos[b] == 't2' and state.pos[b] == 'center'and state.delete['t2']:
            return [('move_one', ''+b, 't2', 'right'), ('move_blocks', goal)]      
        else:
            continue
    return []

    


# methods for "move_one"
def move1(state, b, dest, hand):
    """
    Generate subtasks to get b and put it at dest.
    """
    return [('get', b, hand), ('put', b, dest, hand)]

# methods for "get"
def get_m(state, b, hand):
    """
    Generate a pickup subtask for b.
    """
    return [('pickup', b, hand)]


# methods for "put"
def put_m(state, b, dest, hand):
    """
    Generate a place subtask for b.
    dest is b's destination: either center, t1, or t2.
    """
    if state.holdingL == b or state.holdingR == b:
        return [('place', b, dest, hand)]
    else:
        return False

def formulate_problem():
    """ 
    The variable sstate has already been initialized and sstate.holding has been set.

    """
    sstate = State('Start state')
    sstate.holdingL = False
    sstate.holdingR = False
    sstate.pos = {}
    sstate.pos['red'] = 'center'
    sstate.pos['blue'] = 't1'
    sstate.pos['green'] = 't2'
    sstate.delete = {'t1':False, 't2':False, 'center':False}

    goal = Goal('Goal') 	# Same as above but for goal instead of start state
    goal.holdingL = False
    goal.holdingR = False
    goal.pos = {'red':'center','blue':'t2', 'green':'t1'}
    goal.delete = {'t1':False, 't2':False, 'center':False}
    # Return planner and populated state and goal
    return (sstate, goal)

##
### Touch Nothing Below Here!
##

def file_input(argv):
    cmsc_tests.test(argv)

def main(argv):
    parser = argparse.ArgumentParser(description='HTN Planner')
    parser.add_argument('-r', action='store_true', help='Use ROS')
    parser.add_argument('-f', action='store_true', help='Tests for grading)')
    args = parser.parse_args()
    if args.f:
        file_input(argv)
        return
    (state, goal) = formulate_problem()
    HTNplanner = HTNPlanner("Baxter_World")
    HTNplanner.declare_operators(place, pickup)
    HTNplanner.declare_methods('put', put_m)
    HTNplanner.declare_methods('get', get_m)
    HTNplanner.declare_methods('move_one', move1)
    HTNplanner.declare_methods('move_blocks', moveb_m)
    HTNplanner.planner(state, [('move_blocks', goal)])
    plan = [p for p in HTNplanner.planningsteps.items() if p[1][0] == 'operator'] 
    num = []
    actions = []
    print("HTN Actions:")
    for cnt, elem in enumerate(plan):
        print("%s.  %s " % (cnt + 1, elem[1][1]))
        num.append(cnt+1)
        p = ' '.join(map(str,elem[1][1]))
        actions.append(p)
    if args.r:
        rospy.init_node('Planner', anonymous=True)
        pub_plan = rospy.Publisher('/plan', Plan, queue_size=100)
        p = Plan()
        for cnt, elem in enumerate(plan):
            s = Step()
            s.num.data = cnt+1
            s.step.data = ' '.join(map(str,elem[1][1]))
            p.plan.append(s)
        rospy.sleep(1)
        pub_plan.publish(p)
    return (state,goal,plan)

if __name__ == "__main__":
    main(sys.argv)
