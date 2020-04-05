#Implementation of the role reachablity problem parser

#UR as set of (user, role) tuples
#Users as set of users (strings)
#Roles as set of roles (strings)
#CA set of 4-tuple -> (ra, Rp, Rn, rt), ra and rt string, Rp and Rn forzenset of roles (strings)
#CR set of pairs -> (ra, rt), ra and rt strings

keys = ["Roles", "Users", "UA", "CR", "CA", "Goal"]

#INPUT path of the problem in arbac format, separator of fields inside a line
#OUTPUT dictionary with the components of the problem with keys in the keys list
def read_policy(path, separator = " "):

    f = open(path, "r")
    
    problem = {} #dictionary of the components of the problems

    for line in f:
        #strip characters in order to be safe
        line = line.strip("\n")
        line = line.strip(";")
        line = line.strip(" ")

        #split the line using the separator
        line_splitted = line.split(separator)

        #the first string of the line identify the field of the problem
        if line_splitted[0] in keys:

            #role-to-user assignments line
            if line_splitted[0] == "UA":
                #prepare the set of role-to-user assignments
                problem[line_splitted[0]] = set([])
                #for every assignment <user,role>
                for assignment in line_splitted[1:]:
                    #recover user and role and insert the pair
                    assignment_dec = assignment.strip("<").strip(">").split(",")
                    problem["UA"].add((assignment_dec[0], assignment_dec[1]))

            #can-revoke rules line
            elif line_splitted[0] == "CR":
                #prepare the set of can-revoke rules
                problem[line_splitted[0]] = set([])
                #for every can-revoke rule <adm-role, revoked-role>
                for rule in line_splitted[1:]:
                    #recover adm role and revoked role and insert the pair
                    rule_dec = rule.strip("<").strip(">").split(",")
                    problem["CR"].add((rule_dec[0], rule_dec[1]))

            #can-assign rules line
            elif line_splitted[0] == "CA":
                #prepare the set of can-assign rules
                problem[line_splitted[0]] = set([])
                #for every can-assign rule <adm-role, positive-precs, negative-precs, assigned-role>
                for rule in line_splitted[1:]:
                    rule_dec = rule.strip("<").strip(">").split(",")
                    #recover adm role, assigned role, preconditions and insert the pair
                    #used frozenset in order to make the set hashable to inset it in the set of can-assign rules
                    if rule_dec[1] == "TRUE":
                        problem["CA"].add((rule_dec[0], frozenset([]), frozenset([]), rule_dec[2]))
                    else:
                        Rp = []
                        Rn = []
                        for role in rule_dec[1].split("&"):
                            if role[0] == "-":
                                Rn += [role.strip("-")]
                            else:
                                Rp += [role]
                        problem["CA"].add((rule_dec[0], frozenset(Rp), frozenset(Rn), rule_dec[2]))
                         
            else:
                problem[line_splitted[0]] = line_splitted[1:]
        
    f.close()
    return problem




