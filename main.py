from policy_parser import *
from analyser import *
from aggressive_pruning import *
import os

#UR as set of (user, roles), also with users without roles
#Users as set of users
#Roles as set of roles
#CA set of 4-tuple -> (ra, Rp, Rn, rt)
#CR set of pairs -> (ra, rt)

path = "C:\\Users\loren\Desktop\ARBAC-analyser\Policies\policy8.arbac"

def main():
    problem = read_policy(path, " ")
    print(problem)
    print("\n\n")


    roles = problem["Roles"]
    users = problem["Users"]
    UR = problem["UA"]
    CR = problem["CR"]
    CA = problem["CA"]
    goal = problem["Goal"][0]

    roles, users, UR, CA, CR, goal = backward_slicing(roles, users, UR, CA, CR, goal)

    print(roles)
    print(users)
    print(UR)
    print(CA)
    print(CR)
    print(goal)
    print(check_reachability(roles, users, UR, CA, CR, goal))

if __name__ == '__main__':
    main()