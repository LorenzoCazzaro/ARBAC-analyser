
def backward_slicing(roles, users, UR, CA, CR, goal):
    result_roles_set = set([goal])
    prec_roles_set = set([])
    while prec_roles_set != result_roles_set:
        prec_roles_set = result_roles_set.copy()
        for rule in CA:
            if rule[3] in prec_roles_set:
                result_roles_set.update(rule[1])
                result_roles_set.update(rule[2])
                result_roles_set.add(rule[0])
    
    CA_res = CA.copy()
    for rule in CA:
        if rule[3] not in result_roles_set:
            CA_res.remove(rule)
    
    CR_res = CR.copy()
    for rule in CR:
        if rule[1] not in result_roles_set:
            CR_res.remove(rule)

    roles_res = roles.copy()
    for role in roles:
        if role not in result_roles_set:
            roles_res.remove(role)

    UR_res = UR.copy()
    for assignment in UR:
        if assignment[1] not in result_roles_set:
            UR_res.remove(assignment)

    return roles_res, users, UR_res, CA_res, CR_res, goal
