import http.client
import json
import time
import timeit
import sys
import collections
from pygexf.gexf import *


if __name__ == '__main__':
    api_key = sys.argv[1]
    num_min_parts = '1120'

    #
    # implement your data retrieval code here

    #retrieve data of sets
    server = "www.rebrickable.com"
    conn = http.client.HTTPConnection(server)
    headers = {"Accept": "application/json"}
    url = "https://rebrickable.com/api/v3/lego/sets/?key={}&page=1&page_size=500&min_parts={}&ordering=-num_parts".format(api_key, num_min_parts)
    conn.request("GET",url)
    set_response = conn.getresponse()
    set_data = json.load(set_response)    
    sets = set_data['results']    
    
    #for each set retrieve the data of its parts
    parts_of_sets = []

    for s in sets:
        set_num = s['set_num']
        set_url = "https://rebrickable.com/api/v3/lego/sets/{}/parts/?key={}&page_size=1000".format(set_num, api_key)
        conn.request("GET",set_url)
        response = conn.getresponse()
        part_data = json.load(response)
        results = part_data['results']
        parts = []

        for part in results:
            dic = {}
            dic['part_color'] = part['color']['rgb']
            dic['part_quantity'] = part['quantity']
            dic['part_name'] = part['part']['name']
            dic['part_number'] = part['part']['part_num']
            dic['part_id'] = str(dic['part_number'])+'_'+str(dic['part_color'])
            parts.append(dic)


        if len(parts) >= 20:
            sorted_parts = sorted(parts, key = lambda x:x['part_quantity'], reverse = True)[:20]
        else:
            sorted_parts = parts
        parts_of_sets.append(sorted_parts)


    my_gexf = Gexf("name", "bricks_graph.gexf")
    graph=my_gexf.addGraph("undirected", "static", "bricks_graph.gexf")

    set_attr=graph.addNodeAttribute('set',type='boolean',defaultValue='false')
    part_attr=graph.addNodeAttribute('part',type='boolean',defaultValue='false')

    for i in range(len(sets)):
        set_node = graph.addNode(sets[i]['set_num'],sets[i]['name'],r="0",g="0",b="0")
        set_node.addAttribute(set_attr,'true')
        for j in range(len(parts_of_sets[i])):
            c_hex = parts_of_sets[i][j]['part_color']
            c_r = str(int(c_hex[0:2],16))
            c_g = str(int(c_hex[2:4],16))
            c_b = str(int(c_hex[4:6],16))
            part_node = graph.addNode(parts_of_sets[i][j]['part_id'],parts_of_sets[i][j]['part_name'],r=c_r,g=c_g,b=c_b)
            part_node.addAttribute(part_attr,'true')
            
            graph.addEdge(sets[i]['set_num']+"_"+parts_of_sets[i][j]['part_id'],sets[i]['set_num'],parts_of_sets[i][j]['part_id'],weight=parts_of_sets[i][j]['part_quantity'])
    output_file = open("bricks_graph.gexf","wb+")
    my_gexf.write(output_file)




# complete auto grader functions for Q1.1.b,d
def min_parts():
    """
    Returns an integer value
    """
    # you must replace this with your own value
    return 1120

def lego_sets():
    """
    return a list of lego sets.
    this may be a list of any type of values
    but each value should represent one set

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    # you must replace this line and return your own list
    return sets

def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    # my_gexf = Gexf("Chenjun Tang", "Lego Sets-Parts")
    # gexf.addGraph("undirected", "static", "I'm an empty graph")
    # return gexf.graphs[0]
    return graph

# complete auto-grader functions for Q1.2.d

def avg_node_degree():
    """
    hardcode and return the average node degree
    (run the function called “Average Degree”) within Gephi
    """
    # you must replace this value with the avg node degree
    return 5.479

def graph_diameter():
    """
    hardcode and return the diameter of the graph
    (run the function called “Network Diameter”) within Gephi
    """
    # you must replace this value with the graph diameter
    return 8

def avg_path_length():
    """
    hardcode and return the average path length
    (run the function called “Avg. Path Length”) within Gephi
    :return:
    """
    # you must replace this value with the avg path length
    return 4.413

#Constructing a graph using pygexf
