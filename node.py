import numpy as np

#UR as set of (user, roles), also with users without roles
#Users as set of users
#Roles as set of roles
#CA set of 4-tuple -> (ra, Rp, Rn, rt)
#CR set of pairs -> (ra, rt)

class Node:
    def __init__(self, UR):
        self.UR = UR
        #self.roles = np.array([assignment[1] for assignment in self.UR])
        #self.users = np.array([assignment[0] for assignment in self.UR])
        self.users_to_roles_dict = {}
        self.roles_to_users_dict = {}
        for assignment in self.UR:
            if assignment[0] not in self.users_to_roles_dict.keys():
                self.users_to_roles_dict.keys[assignment[0]] = [assignment[1]]
            else:
                self.users_to_roles_dict.keys[assignment[0]] += [assignment[1]]
            
            if assignment[1] not in self.roles_to_users_dict.keys():
                self.roles_to_users_dict.keys[assignment[1]] = [assignment[0]]
            else:
                self.roles_to_users_dict.keys[assignment[1]] += [assignment[0]]

    def roles_assigned(self):
        return self.roles_to_users_dict.keys().copy()

    def user_assigned(self):
        return self.users_to_roles_dict.keys().copy()

    def __eq__(self, other):
        return self.UR == other.UR

    def apply_CA_rules(self, tot_users, rules):
        rules_appliable = set([(rule if rule[0] in self.roles else None) for rule in rules])
        rules_appliable.remove(None)
        print(rules_appliable)

        new_nodes = []
        for rule in rules_appliable:
            if 

        return
    
    def apply_CR_rules(self, rules):
        roles_to_remove = set([(rule[1] if rule[0] in self.roles else None) for rule in rules])
        roles_to_remove.remove(None)
        print(roles_to_remove)
        new_nodes = []
        for assignment in self.UR:
            if assignment[1] in roles_to_remove:
                new_nodes += [Node(self.UR - set([assignment]))]
        return np.array(new_nodes)

    def role_is_present(self, role):
        return role in self.roles_to_users_dict.keys()

    def __get_role_for_user(self, user):
        if user not in self.users_to_roles_dict.keys():
            return np.array([])
        return self.users_to_roles_dict[user]
        roles = []
        for assignment in self.UR:
            if assignment[0] == user:
                roles += [assignment[1]]
        return np.array(roles)

    def __get_users_for_role(self, role):
        if role not in self.roles:
            return np.array([])
        
        users = []
        for assignment in self.UR:
            if assignment[1] == role:
                users += [assignment[0]]
        return np.array(users)
        