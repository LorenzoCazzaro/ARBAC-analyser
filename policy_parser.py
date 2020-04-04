#UR as set of (user, roles), also with users without roles
#Users as set of users
#Roles as set of roles
#CA set of 4-tuple -> (ra, Rp, Rn, rt)
#CR set of pairs -> (ra, rt)

keys = ["Roles", "Users", "UA", "CR", "CA", "Goal"]

def read_policy(path, separator):

    f = open(path, "r")
    
    problem = {}

    for line in f:
        line = line.strip("\n")
        line = line.strip(";")
        line = line.strip(" ")

        line_splitted = line.split(separator)

        if line_splitted[0] in keys:

            if line_splitted[0] == "UA":
                problem[line_splitted[0]] = set([])
                for assignment in line_splitted[1:]:
                    assignment_dec = assignment.strip("<").strip(">").split(",")
                    problem["UA"].add((assignment_dec[0], assignment_dec[1]))

            elif line_splitted[0] == "CR":
                problem[line_splitted[0]] = set([])
                #print(line_splitted)
                for rule in line_splitted[1:]:
                    #print(rule)
                    rule_dec = rule.strip("<").strip(">").split(",")
                    #print(rule_dec)
                    problem["CR"].add((rule_dec[0], rule_dec[1]))

            elif line_splitted[0] == "CA":
                problem[line_splitted[0]] = set([])
                for rule in line_splitted[1:]:
                    rule_dec = rule.strip("<").strip(">").split(",")
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




