import networkx as nx
from pyvis.network import Network
import functions as functions
import prolog as pg
from data_class import Nodes, Objects, Affordance, Physical

nx_graph = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", select_menu=True, filter_menu=True)
nx_graph.barnes_hut()
data = {
    "object": [],
    "affordance": [],
    "physical": [],
    "category": []
}
#
functions.populate(data)
functions.parsing_rule_book(data)
sub_relations = []
sub_relations = functions.deserialize_rule_book()

pg.produce_prolog_rule(sub_relations, data)
#pg.produce_aggregate_query()
# TODO uncomment the below
# for item in data["object"]:
#     nx_graph.add_node(item.id, size=400, title=item.name, group=item.category)
for item in data["affordance"]:
    if item.isActive == 1:
        var = 1
    else:
        var = 0
    nx_graph.add_node(item.id+1000, title=item.name, group=1000+var, size=100)
for item in data["physical"]:
    nx_graph.add_node(item.id+2000, title=item.name, group=2000+item.type, size=100)
for item in data["category"]:
    nx_graph.add_node(item.id+3000, title=item.name, group=3000, size=100)
for ids, weights in sub_relations:
    start_id, end_id = ids[0], ids[1]
    if start_id < 10000 and end_id < 10000:
        if float(weights) > 0.30:
            nx_graph.add_edge(start_id, end_id, weight=float(weights))
nx_graph.show_buttons(filter_=['physics'])
nx_graph.show("30percent_inferrence.html")