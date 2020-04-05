#implementation of the aggressive pruning to semplify instances of role reachability problem

#UR as set of (user, role) tuples
#Users as set of users (strings)
#Roles as set of roles (strings)
#CA set of 4-tuple -> (ra, Rp, Rn, rt), ra and rt string, Rp and Rn forzenset of roles (strings)
#CR set of pairs -> (ra, rt), ra and rt strings



#implementation of backward slicing -> compute an overapproximation of the roles
#which are relevant to assign the goal of the role reachability problem

#INPUT: description of the problem: roles, users, user-to-role assignments, can-assign rules,
#can-revoke rules, goal role
#OUTPUT: updated and reduced description of the problem
def backward_slicing(roles, users, UR, CA, CR, goal):

    #S_0
    #in order to assign the target role, the same target role is relevant ;)
    result_roles_set = set([goal])
    
    #S_(i-1)
    prec_roles_set = set([])

    while prec_roles_set != result_roles_set:
        prec_roles_set = result_roles_set.copy()
        for rule in CA:
            if rule[3] in prec_roles_set:
                result_roles_set.update(rule[1])
                result_roles_set.update(rule[2])
                result_roles_set.add(rule[0])
    
    #result roles set S* is result_roles_set

    #remove from CA all the rules that assign a role not in S*
    CA_res = CA.copy()
    for rule in CA:
        if rule[3] not in result_roles_set:
            CA_res.remove(rule)
    
    #remove from CR all the rules that revoke a role not in S*
    CR_res = CR.copy()
    for rule in CR:
        if rule[1] not in result_roles_set:
            CR_res.remove(rule)

    #delete roles not in S*
    roles_res = roles.copy()
    for role in roles:
        if role not in result_roles_set:
            roles_res.remove(role)

    #delete also user-to-role assignments that involve roles deleted
    UR_res = UR.copy()
    for assignment in UR:
        if assignment[1] not in result_roles_set:
            UR_res.remove(assignment)

    return roles_res, users, UR_res, CA_res, CR_res, goal





#implementation of forward slicing -> Compute an over-approximation of the reachable roles

#INPUT: description of the problem: roles, users, user-to-role assignments, can-assign rules,
#can-revoke rules, goal role
#OUTPUT: updated and reduced description of the problem
def forward_slicing(roles, users, UR, CA, CR, goal):
    #S_0, initial set of reachable roles
    result_roles_set = set([assignment[1] for assignment in UR])
    
    #S_(i-1)
    prec_roles_set = set([])

    #continue if the set of reachable roles isn't a fixed point
    while prec_roles_set != result_roles_set:
        prec_roles_set = result_roles_set.copy()
        #for every rule
        for rule in CA:
            #insert the role target of the rule if the administrative role is reachable
            #and the set of preconditions is subset of the set of reachable roles
            if rule[0] in prec_roles_set and rule[1].issubset(prec_roles_set):
                result_roles_set.add(rule[3])

    #result roles set S* is result_roles_set

    #remove from CA all the rules that include any role not in S* 
    #in the positive preconditions or in the target            
    CA_res = CA.copy()
    for rule in CA:
        if rule[3] not in result_roles_set or not rule[1].issubset(result_roles_set):
            CA_res.remove(rule)
        rule[2] &= result_roles_set    
    
    #remove from CR all the rules that mention any role not in S*
    CR_res = CR.copy()
    for rule in CR:
        if rule[0] not in result_roles_set or rule[1] not in result_roles_set:
            CR_res.remove(rule)

    #delete roles not in S*
    roles_res = roles.copy()
    for role in roles:
        if role not in result_roles_set:
            roles_res.remove(role)

    #delete also user-to-role assignments that involve roles deleted
    UR_res = UR.copy()
    for assignment in UR:
        if assignment[1] not in result_roles_set:
            UR_res.remove(assignment)

    return roles_res, users, UR_res, CA_res, CR_res, goal
