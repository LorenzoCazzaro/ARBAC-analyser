#implementation of the state/node of the state space tree that encapsulates the current UR

#UR as set of (user, role) tuples
#Users as set of users (strings)
#Roles as set of roles (strings)
#CA set of 4-tuple -> (ra, Rp, Rn, rt), ra and rt string, Rp and Rn forzenset of roles (strings)
#CR set of pairs -> (ra, rt), ra and rt strings


class Node:
    def __init__(self, UR):
        self.UR = UR.copy()
        #dictionary that map users to theirs roles
        self.users_to_roles_dict = {}
        #dictionary that map roles to the users that possess the role
        self.roles_to_users_dict = {}
    
        for assignment in self.UR:
            #if the user isn't in the dictionary, initialize a new entry
            if assignment[0] not in self.users_to_roles_dict.keys():
                self.users_to_roles_dict[assignment[0]] = [assignment[1]]
            else:
                self.users_to_roles_dict[assignment[0]] += [assignment[1]]
            
            #if the role isn't in the dictionary, initialize a new entry
            if assignment[1] not in self.roles_to_users_dict.keys():
                self.roles_to_users_dict[assignment[1]] = [assignment[0]]
            else:
                self.roles_to_users_dict[assignment[1]] += [assignment[0]]

    #overriding equality operator
    def __eq__(self, other):
        return self.UR == other.UR

    #apply the CA rules at the current node
    #INPUT set of all the users of the system, rules to apply
    #OUTPUT new nodes of the state space tree corresponding to new user-to-role assignments set
    def apply_CA_rules(self, tot_users, rules):
        #find the rules that can be applied by exploring the checking if the adm role of the rule is the actual roles assigned in the UR
        rules_appliable = set([(rule if rule[0] in self.roles_to_users_dict.keys() else None) for rule in rules])
        if None in rules_appliable:
            rules_appliable.remove(None)
        new_nodes = []

        for rule in rules_appliable:

            for user in self.users_to_roles_dict:
                #if the target role of the rule isn't assigned to the user 
                #and if the user doesn't possess a negative precondition
                #and if the user possesses all the positive precondition
                if rule[3] not in self.users_to_roles_dict[user] and len(rule[2].intersection(self.users_to_roles_dict[user])) == 0 and rule[1].issubset(self.users_to_roles_dict[user]):
                    new_nodes += [Node(self.UR | set([(user, rule[3])]))] #add the assignment and create a new node
            if len(rule[1]) == 0: #if the rule hasn't positive preconditions
                for user in set(tot_users) - set(self.users_to_roles_dict.keys()): #for every user without role
                    new_nodes += [Node(self.UR | set([(user, rule[3])]))] #add the assignment and create a new node
        return new_nodes
    
    #apply the CA rules at the current node
    #INPUT set of all the users of the system, rules to apply
    #OUTPUT new nodes of the state space tree corresponding to new user-to-role assignments set
    def apply_CR_rules(self, rules):
        #find the roles to remove by exploring the roles revoked from rules and the roles in the actual UR
        roles_to_remove = set([(rule[1] if rule[0] in self.roles_to_users_dict.keys() else None) for rule in rules])
        if None in roles_to_remove:
            roles_to_remove.remove(None)

        new_nodes = []
        for assignment in self.UR:
            if assignment[1] in roles_to_remove:
                new_nodes += [Node(self.UR - set([assignment]))]
        return new_nodes

    #check if the role submitted is assigned to a user
    def role_is_present(self, role):
        return role in self.roles_to_users_dict.keys()
        
    
        