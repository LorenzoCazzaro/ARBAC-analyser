from node import *

#UR as set of (user, roles), also with users without roles
#Users as set of users
#Roles as set of roles
#CA set of 4-tuple -> (ra, Rp, Rn, rt)
#CR set of pairs -> (ra, rt)

#breadth first search approach
def check_reachability(roles, users, UR, CA, CR, target):
    #maximum_depth = 0
    nodes_to_check = [Node(UR)]
    nodes_seen = []
    i = 0
    
    while len(nodes_to_check) != 0 :#and i != 1:
        node_visited = nodes_to_check.pop(0)
        nodes_seen += [node_visited]
        if node_visited.role_is_present(target):
            return True
        CA_result_nodes = node_visited.apply_CA_rules(users, CA)
        CR_result_nodes = node_visited.apply_CR_rules(CR)
        CA_result_nodes_res = CA_result_nodes.copy()
        for node in CA_result_nodes:
            if node in nodes_seen:
                #print("A")
                CA_result_nodes_res.remove(node)
        CA_result_nodes = CA_result_nodes_res
        CR_result_nodes_res = CR_result_nodes.copy()
        for node in CR_result_nodes: #funziona sempre?
            if node in nodes_seen:
                #print("B")
                CR_result_nodes_res.remove(node)
        CR_result_nodes = CR_result_nodes_res
        nodes_to_check += CA_result_nodes
        nodes_to_check += CR_result_nodes
        # for node in nodes_to_check:
        #     print(node.UR)
        #     print("\n")
        i += 1
        
    return False 

