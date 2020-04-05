from policy_parser import read_policy
from analyser import check_reachability
from aggressive_pruning import backward_slicing, forward_slicing
import os

#UR as set of (user, role) tuples
#Users as set of users (strings)
#Roles as set of roles (strings)
#CA set of 4-tuple -> (ra, Rp, Rn, rt), ra and rt string, Rp and Rn forzenset of roles (strings)
#CR set of pairs -> (ra, rt), ra and rt strings

path = "C:\\Users\loren\Desktop\ARBAC-analyser\Policies\policy8.arbac"

def main():
    #read the problem
    problem = read_policy(path, " ")
    print(problem)
    print("\n\n")

    #unzip the problem instance
    roles = problem["Roles"]
    users = problem["Users"]
    UR = problem["UA"]
    CR = problem["CR"]
    CA = problem["CA"]
    goal = problem["Goal"][0]

    #apply aggressive pruning
    roles, users, UR, CA, CR, goal = backward_slicing(roles, users, UR, CA, CR, goal)
    #roles, users, UR, CA, CR, goal = forward_slicing(roles, users, UR, CA, CR, goal)

    #print(roles)
    #print(users)
    #print(UR)
    #print(CA)
    #print(CR)
    #print(goal)

    print(check_reachability(roles, users, UR, CA, CR, goal))

if __name__ == '__main__':
    main()