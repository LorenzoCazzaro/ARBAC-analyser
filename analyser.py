#implementation of the analyser -> a function ;)

from node import *

#UR as set of (user, role) tuples
#Users as set of users (strings)
#Roles as set of roles (strings)
#CA set of 4-tuple -> (ra, Rp, Rn, rt), ra and rt string, Rp and Rn forzenset of roles (strings)
#CR set of pairs -> (ra, rt), ra and rt strings

#The analyser use a breadth first search approach in order to explore all the space state tree
#from the root of the tree, the initial user-to-role assignments.

#Every node of the state space tree is a user-to-role assignments set.
#From one UR it's possible to find other nodes of the tree by appling CA and CR rules,
#that remains static during the execution

#INPUT: description of the problem: roles, users, user-to-role assignments, can-assign rules,
#can-revoke rules, goal role
#OUTPUT: True if the goal is reachable, False otherwise
def check_reachability(roles, users, UR, CA, CR, target):
    #start to check if the initial nodes contains a user-to-role assignment with the target role
    nodes_to_check = [Node(UR)]
    nodes_seen = [] #nodes already visited
    
    while len(nodes_to_check) != 0:
        #select next node to check
        node_visited = nodes_to_check.pop(0)

        #the node is visited, add it to the nodes already seen
        nodes_seen += [node_visited]

        #if the target role is assigned, the problem is solved and the target is reachable
        if node_visited.role_is_present(target):
            return True

        #apply rules to the current UR in order to retrieve the next reachable states    
        CA_result_nodes = node_visited.apply_CA_rules(users, CA)
        CR_result_nodes = node_visited.apply_CR_rules(CR)

        #remove the states already visisted from the list of the new states to visit
        CA_result_nodes_res = CA_result_nodes.copy()
        for node in CA_result_nodes:
            if node in nodes_seen:
                CA_result_nodes_res.remove(node)
        CA_result_nodes = CA_result_nodes_res

        #remove the states already visisted from the list of the new states to visit
        CR_result_nodes_res = CR_result_nodes.copy()
        for node in CR_result_nodes: 
            if node in nodes_seen:
                CR_result_nodes_res.remove(node)
        CR_result_nodes = CR_result_nodes_res

        nodes_to_check += CA_result_nodes
        nodes_to_check += CR_result_nodes
                
    return False 

