def produce_prolog_rule(list_of_weights, data):
    list_of_labels = []
    list_of_weight = []
    for ids, weights in list_of_weights:
        if float(weights) > 0.90:
            for each_id in ids:
                label = ""
                if each_id < 2000:
                    # search affordance
                    aff_id = each_id - 1000
                    look_into = data["affordance"]
                    for row in look_into:
                        if row.id == aff_id:
                            label = row.name + "___a"
                elif each_id <3000:
                    #search physical
                    phy_id = each_id -2000
                    look_into = data["physical"]
                    for row in look_into:
                        if row.id == phy_id:
                            label = row.name + "___p"
                elif each_id < 4000:
                    cate_id = each_id - 3000
                    look_into = data["category"]
                    for row in look_into:
                        if row.id == cate_id:
                            label = row.name + "___c"
                list_of_labels.append(label)
                list_of_weight.append(weights)



    #TODO: now we need to actually develop the rules
    """format :
        when inferring the affordance
            inf_has_affordance( object, affordance, active ) :- ( has_property( object, thatProperty, type) ; 
                                                                is_a (object, category) ), has_affordance ( some other object, affordance, is_active)
            inf_has_property( object, property, 
    """
    inferring_by_list = []
    inferred = "empty"
    print(len(list_of_labels))
    print(len(list_of_weight))
    #TODO : still working on the problog 11/16/2022
    define_problog_version(list_of_labels, list_of_weight)
    for i in range(0, len(list_of_labels)):
        if i == 0 or i % 2 == 0 :
            if inferred == "empty":
                inferred = list_of_labels[i]
            elif inferred == list_of_labels[i]:
                continue
            elif inferred != list_of_labels[i]:
                # pass the list
                # print(inferring_by_list)
                modify_rule_statement(inferred, inferring_by_list)
                # reset the list
                inferring_by_list = []
                inferred = list_of_labels[i]
        else:
            proof = list_of_labels[i]
            inferring_by_list.append((inferred, proof))





def modify_rule_statement(inferring, inferring_by_list):
    statement = ""
    # assign the starting rule
    label = inferring.split("___")[0]
    type = inferring.split("___")[1]
    label = label.replace(" ", "_")
    if type == "a":
        statement = "inf_has_affordance(X, " + label + ", Y) :- ("
    elif type == "c":
        statement = "inf_is_a(X, " + label + ") :- ("
    elif type == "p":
        statement = "inf_has_property(X, " + label + ", Y) :- ("

    multiple_proof = len(inferring_by_list)
    for i in range(0, multiple_proof):
        proof = (inferring_by_list[i])[1]
        if proof != "":
            proof_type = proof.split("___")[1]
            proof_property = proof.split("___")[0]
            multiple_proof = len(inferring_by_list)
            if proof_type == "a":
                statement = statement + "has_affordance(X, " + proof_property + ", A)"
            elif proof_type == "c":
                statement = statement + "is_a(X, " + proof_property + ")"
            elif proof_type == "p":
                statement = statement + "has_property(X, " + proof_property + ", Z)"
            if i == multiple_proof-1:
                # last
                statement = statement + ")"
                if type == "a":
                    statement = statement + ", has_affordance(A, " + label +", Y)"
                elif type == "p":
                    statement = statement + ", has_property(A, " + label +", Y)"
                statement = statement + "."
            elif i != multiple_proof:
                statement = statement + "; "
    # print(statement)
    f = open("rule_book_draft_11-09-2022", "a")
    if(len(statement)>40):
        f.writelines(statement)
        f.writelines("\n")


def produce_aggregate_query():
    path = "C://Users//suzin//OneDrive//Documents//WSU//Research//experiment scripts//90per_inf_rule.txt"
    f = open(path, "r")
    f2 = open("90per_command", "a")
    rules = f.readlines()
    for each_rule in rules:
        just_the_rule = each_rule.split(" :-")[0]
        #print(just_the_rule)
        adding_command = f"aggregate_all(count, distinct({just_the_rule}), Count)."
        #print(adding_command)
        f2.writelines(adding_command)
        f2.writelines("\n")

def define_problog_version(list_of_labels, list_of_weight):
    inferred = "empty"
    inferring_by_list = []
    lists_by_weights = []
    f2 = open("problog_90per_rule", "a")
    for i in range(0, len(list_of_labels)):
        if i == 0 or i % 2 == 0:
            if inferred == "empty":
                inferred = list_of_labels[i]
            elif inferred == list_of_labels[i]:
                continue
            elif inferred != list_of_labels[i]:
                # pass the list
                # (inferring_by_list)
                # reset the list
                #print(lists_by_weights)
                #print(inferring_by_list)
                modify_rule_statement_problog(inferred, inferring_by_list, lists_by_weights)
                inferring_by_list = []
                lists_by_weights = []
                inferred = list_of_labels[i]
        else:
            proof = list_of_labels[i]
            # print(proof)
            inferring_by_list.append((inferred, proof))
            lists_by_weights.append(list_of_weight[i])


def modify_rule_statement_problog(inferring, inferring_by_list, weight_lists):
    statement = ""
    statement_list = []
    # assign the starting rule

    multiple_proof = len(inferring_by_list)
    for i in range(0, multiple_proof):
        label = inferring.split("___")[0]
        type = inferring.split("___")[1]
        label = label.replace(" ", "_")
        if type == "a":
            statement = "inf_has_affordance(X, " + label + ", Y) :- ("
        elif type == "c":
            statement = "inf_is_a(X, " + label + ") :- ("
        elif type == "p":
            statement = "inf_has_property(X, " + label + ", Y) :- ("
        proof = (inferring_by_list[i])[1]
        if proof != "":
            proof_type = proof.split("___")[1]
            proof_property = proof.split("___")[0]
            multiple_proof = len(inferring_by_list)
            if proof_type == "a":
                statement = statement + "has_affordance(X, " + proof_property + ", A)"
            elif proof_type == "c":
                statement = statement + "is_a(X, " + proof_property + ")"
            elif proof_type == "p":
                statement = statement + "has_property(X, " + proof_property + ", Z)"
            statement = str(weight_lists[i]) + "::" + statement
            statement = statement + ")"
            if type == "a":
                statement = statement + ", has_affordance(A, " + label +", Y)"
            elif type == "p":
                statement = statement + ", has_property(A, " + label +", Y)"
            statement = statement + "."
            # elif i != multiple_proof:
            #     statement = statement + "; "
            # statement_list.append(statement)
            print(statement)
    f = open("problog_rulebook_1116_90per", "a")
    if(len(statement)>40):
        f.writelines(statement)
        f.writelines("\n")
