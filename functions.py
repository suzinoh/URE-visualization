import mariadb
import sys
from data_class import Nodes, Objects, Affordance, Physical, Category
from os import listdir
from datetime import date

Host = "localhost"
User = "root"
Password ="1234"
database = "ure-suzinoh"

try:
    conn = mariadb.connect(
        user="root",
        password="1234",
        host="127.0.0.1",
        port = 3306,
        database = "ure-suzinoh"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def populate(data):
    executeStr = "SELECT object_id, object_label, object_category FROM object"
    cur.execute(executeStr)
    queried = cur.fetchall()
    for each in queried:
        data["object"].append(Objects(each[0], each[1], each[2]))
    executeStr2 = "SELECT affordance_id, affordance_label, is_active FROM affordance"
    cur.execute(executeStr2)
    queried = cur.fetchall()
    for each in queried:
        data["affordance"].append(Affordance(each[0], each[1], each[2]))
    executeStr3 = "SELECT physical_id, physical_label, physical_subcategory FROM physical"
    cur.execute(executeStr3)
    queried = cur.fetchall()
    for each in queried:
        data["physical"].append(Physical(each[0], each[1], each[2]))
    executeStr4 = "SELECT category_id, category_label FROM category"
    cur.execute(executeStr4)
    queried = cur.fetchall()
    for each in queried:
        data["category"].append(Category(each[0], each[1]))

final_list =[]
def deserialize_rule_book():
    """takes in string for original and features in a serialized form created by getting inferred edges
     from "summary" table
        WHAT TO RETURN : starting one's index of node in pyvis
                         ending one's index of node in pyvis
                         weight to assign
        INPUT : take original and features as input
        UNDERLYING RULE FOR ID:
            affordance = +1000
            physical = +2000
            category = +3000

            order = affordance -> category -> physical
            sub_relation structure == start_id , end_id , weight
     """
    path = "C://Users//suzin//PycharmProjects//testingVisualization"
    weight_doct =[]
    dir_list = listdir(path)
    for item in dir_list:
        if "2022" in item and (".html" not in item):
            weight_doct.append(item)
    print(weight_doct)
    #TODO: implement the selection part when we have more than 1, paused for now
    f = open(weight_doct[0], "r")
    lines = f.readlines()
    original = "empty"
    weight_line = "empty"
    type = "empty" # type will be used for the addition of the ids
    for each_line in lines:
        if "/weight:" in each_line:
            weight_line = each_line
        else:
            original = each_line.replace("\n","")
        if weight_line != "empty":
            if ("c___") not in weight_line:
                type = "category"
            elif ("c___" and "p___") in weight_line:
                type = "affordance"
            elif ("a___" and "c___") in weight_line:
                type = "physical"
            construct_sub_relation(original, weight_line, type)
            original, weight_line, type = "empty", "empty", "emtpy"
        # splitting = original.split("___")
        # print(splitting, type)

    return (final_list)

def construct_sub_relation(original, weight, type):
    get_original_id = int((original.split("___"))[1])
    if type == "affordance" : get_original_id = get_original_id + 1000
    elif type == "category" : get_original_id = get_original_id + 3000
    else : get_original_id = get_original_id + 2000
    weight_factors = weight.split(",")
    for items in weight_factors:
        splits = items.split("___")
        if len(splits) < 3:
            return None
        else:
            weight_type = splits[0]
            end_id = int((splits[1].split("."))[1])
            weight = splits[2]
            if "c" in weight_type:
                end_id = end_id + 3000
            elif "p" in weight_type:
                end_id = end_id + 2000
            else :
                end_id = end_id + 1000
            element_of_final = ((get_original_id, end_id), weight)
            final_list.append(element_of_final)


def type_configure(book_name):
    if "Aff" in book_name:
        return "affordance"
    if "Cate" in book_name:
        return "category"
    if "Physic" in book_name:
        return "physical"


def parsing_rule_book(data):
    """parse the rule book into different nodes with weights, in order to
    represent the nodes
    """
    inferred_relations = []
    path = "C://Users//suzin//PycharmProjects//URE-BuildKB-GitHub"
    rule_books = []
    dir_list = listdir(path)
    for item in dir_list:
        if "Rule Book 2022" in item:
            rule_books.append(item)

    if len(rule_books) > 3:
        # choose which one to process
        print("Not supporting multiple versions of dictionary yet")
    else:
        """open the file and read the lines, and we need to deserialize"""
        for book in rule_books:
            raw_path = path + "//" + book
            type = type_configure(book)
            f = open(raw_path, "r")
            lines = f.readlines()
            feature = "empty"
            original = "emtpy"
            for each_line in lines:
                if "features" in each_line:
                    feature = each_line
                else:
                    original = each_line
                if feature != "empty" and original != "empty":
                    #inferred_relations.append(deserialize_rule_book(original, feature, data, type))
                    # print(feature, original)
                    weight_line = process_weight(feature, original)
                    weight_line = weight_line + "\n"
                    # print(original, weight_line)
                    today = date.today()
                    f = open(str(today), "a")
                    f.writelines(original)
                    f.writelines(weight_line)
                    feature = "empty"
                    original = "emtpy"


def process_weight(feature, original):
    feature = feature.replace("/features:", "")
    a = feature.split(",")
    # when split with ",", the last of the list is \n
    kind_master = "empty"
    labels = []
    frequency = []
    weight_config = "/weight: "
    for item in a:
        item = item.replace(" ", "")
        splitting = item.split("___")
        kind = splitting[0]
        if len(splitting) == 3:
            if kind_master == "empty":
                kind_master = kind
            if kind_master != kind:
                weights = calculate_weight(frequency)
                #calculate the weight with given
                for i in range(0, len(weights)):
                    weight_config = weight_config + kind_master + "___" + labels[i] + "___" + str(weights[i]) + ", "
                kind_master = kind
                labels = []
                frequency = []
            if kind_master == kind:
                # we are going to continue until kind changes
                labels.append(splitting[1])
                frequency.append(int(splitting[2]))
    # finishing the weight calculation
    weights = calculate_weight(frequency)
    for i in range(0, len(weights)):
        weight_config = weight_config + kind_master + "___" + labels[i] + "___" + str(weights[i]) + ", "
    return weight_config

def calculate_weight(list_of_frequency):
    """return the list of weights"""
    sum = 0
    result = []
    for each_frequency in list_of_frequency:
        sum = sum + each_frequency

    if len(list_of_frequency) == 1:
        # only 1 element exists
        result.append(1)
    else:
        for each_frequency in list_of_frequency:
            weight = each_frequency/sum
            result.append(weight)

    return result
