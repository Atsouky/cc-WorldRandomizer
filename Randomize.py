import json,os,random
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx


#region NetworkX

def build_teleporter_graph(teleporters):
    """
    Builds a graph of teleporters and their connections.
    Args:
        teleporters: List of teleporter dictionaries with their connections.
    Returns:
        G: A networkx graph.
    """
    G = nx.DiGraph()  # Use a directed graph since teleporters have directions

    for tp in teleporters:
        # Add a node for each teleporter
        G.add_node(tp["name"], path=tp["path"], dir=tp["dir"])
        
        # Add an edge to the destination teleporter
        if tp["To"]["destination"]:
            G.add_edge(tp["name"], tp["To"]["destination"], direction=tp["dir"])
    
    return G

def visualize_teleporter_graph(G):
    """
    Visualizes the teleporter graph.
    Args:
        G: A networkx graph.
    """
    plt.figure(figsize=(12, 12))
    
    # Position nodes in a spring layout
    pos = nx.spring_layout(G,k=10,iterations=10000)
    
    # Draw the graph
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", edge_color="gray", 
        node_size=2000, font_size=10, font_color="black", arrowsize=20
    )
    
    # Draw edge labels for directions
    edge_labels = nx.get_edge_attributes(G, "direction")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Teleporter Network")
    plt.show()

#endregion 





directinv = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'EAST': 'WEST', 'WEST': 'EAST'}
markerinv = {'NORTH': 'bottom', 'SOUTH': 'north', 'EAST': 'left', 'WEST': 'right'}
markerinv2 = {'north': 'bottom', 'bottom': 'north', 'right': 'left', 'left': 'right'}

def get_all_dir(path:str = 'assets\data\maps'):
    dirs = []
    for i in os.walk(path):
        dirs.append(i[0])
    return dirs

def get_all_file_and_dir(path:str = 'assets\data\maps'):
    dirs = {}
    for i in os.walk(path):
        dirs[i[0]] = i[2]
    return dirs

def get_all_file():
    files = []
    for i in os.walk('assets\data\maps'):
        files.append(i[2])
    return files

def exclude_maps(paths:list[str]):
    exclude = ['assets\\data\\maps']
    b = {}
    for path in paths:
        d = get_all_dir(path)
        for i in d:
            exclude.append(i)
    a = get_all_file_and_dir()
    for i in a.keys():
        if i not in exclude:
            b[i] = a[i]
    return b

def get_maps_ex(excludepaths:list[str] = []):
    a = exclude_maps(excludepaths)
    maps = []
    for i in a.keys():
        for j in a[i]:
            maps.append(i + '\\' + j)
    return maps

def get_maps_zone(path:str = 'assets\data\maps'):
    maps = get_all_file_and_dir(path)
    lst = []
    for i in maps.keys():
        for j in maps[i]:
            lst.append(i+'\\'+j)
    return lst


#endregion


#region json

def load_json(file_path:str):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_json(path:str,data):
    with open(path, 'w') as f:
        json.dump(data, f)

#endregion


#region get id tp

def swap_room(data1, data2, id1:int, id2:int):
    temp = data1['entities'][id1]['settings']['map']
    data1['entities'][id1]['settings']['map'] = data2['entities'][id2]['settings']['map']
    data2['entities'][id2]['settings']['map'] =  temp
    return data1, data2

"""def search_id_Tp_Ground(data):
    TeleportGround_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportGround':   
            if data['entities'][i]['level'] == 1:
                TeleportGround_ids.append((i,data['entities'][i]['type'],data['entities'][i]['settings']['name'],data['entities'][i]['settings']['map'],data['entities'][i]['settings']['dir'],data['entities'][i]['settings']['marker'],data['entities'][i]['settings']['mapId']))
    return TeleportGround_ids"""

def search_id_Tp_Ground(data):
    TeleportGround_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportGround':   
            if data['entities'][i]['level'] == 1:
                TeleportGround_ids.append()
    return TeleportGround_ids


def search_id_Tp_stairs(data):
    TeleportStairs_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportStairs':   
            TeleportStairs_ids.append((i,data['entities'][i]['type'],data['entities'][i]['settings']['name'],data['entities'][i]['settings']['map'],data['entities'][i]['settings']['stairType'],data['entities'][i]['settings']['marker'],data['entities'][i]['settings']['mapId']))
    return TeleportStairs_ids

def search_id_Tp_Doors(data):
    TeleportDoors_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'Door':    
            TeleportDoors_ids.append((i,data['entities'][i]['type'],data['entities'][i]['settings']['name'],data['entities'][i]['settings']['map'],data['entities'][i]['settings']['dir'],data['entities'][i]['settings']['marker']))
    return TeleportDoors_ids

def search_id_Tp_Fields(data):
    TeleportFields_ids = []
    exclude = ['','landmark','t1','t2','t3']
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportField': 
            if data['entities'][i]['settings']['name'] not in exclude:
                TeleportFields_ids.append(i)
    return TeleportFields_ids

def search_all_Tp(data):
    #Teleport_ids = {'Tp_Ground': search_id_Tp_Ground(data), 'Tp_stairs': search_id_Tp_stairs(data), 'Tp_Doors': search_id_Tp_Doors(data), 'Tp_Fields': search_id_Tp_Fields(data)}
    if search_id_Tp_Ground(data) == [] and search_id_Tp_stairs(data) == [] and search_id_Tp_Doors(data) == []:
        Teleport_ids = None
    else:
        Teleport_ids = {'Tp_Ground': search_id_Tp_Ground(data), 'Tp_stairs': search_id_Tp_stairs(data), 'Tp_Doors': search_id_Tp_Doors(data)}
    
    return Teleport_ids


def get_map_by_name(name:str):
    maps = get_all_file_and_dir()
    lst=[]
    name = str(name)+'.json'
    for i in maps.keys():
        if name in maps[i]:
            lst.append(i)
    return lst





def count_Tp(resumed_maps):
    count = 0
    count += len(resumed_maps[1]['Tp_Ground'])
    count += len(resumed_maps[1]['Tp_stairs'])
    count += len(resumed_maps[1]['Tp_Doors'])
    return count
    
def split_name(name):
    #name = assets/data/maps/autumn/entrance.json
    name = name.split('\\')
    name = name[-1]
    name = name.split('.')
    name = name[0]
    return name

def split_zone(name):
    #name = assets/data/maps/autumn/entrance.json
    name = name.split('\\')
    names = name[3]
    if names == name[-2]:
        return names
    else:
        return names+'.'+name[-2]

def tp_name(name):
    a = split_name(name)
    b = split_zone(name)
    return str(b+'.'+a)

def replace_slash(name):
    name = name.replace('/','\\')
    return name

def resume(maps):
    Teleporters = []

    for path in tqdm(maps, desc='Teleporters_resume', unit='maps'):
        
        data = load_json(path)
        Teleport_ids = search_all_Tp(data)        
        if Teleport_ids :
            
            for i in Teleport_ids['Tp_Ground']:
                
                tp = {
                    
                    "name" : tp_name(path), 
                    "path" : path,
                    "type" : i[1],
                    "id" : i[0],
                    "dir" : i[4],
                    "mapId" : i[6],
                    "To" : {
                        "destination" : i[3],
                        "marker" : markerinv[i[4]],
                        "dir" : directinv[i[4]]
                        }
                    }
                Teleporters.append(tp)
    
    
    return Teleporters


def link_tps(tp1,tp2):
    
    tp1['To']['destination'] = tp2['name']
    tp2['To']['destination'] = tp1['name']
    return tp1,tp2


def Salles(teleporters,maps):
    # salle = [[teleporter1,teleporter2],[teleporter3,teleporter4]]
    Salles = {}
    salles = []
    for path in maps:
        for i in teleporters:
            if i['path'] == path:
                salles.append(i)
        if salles != []:
            Salles[path] = salles
            salles = []
    return Salles   


def categorizeDir(teleporter):
    North = []
    South = []
    East = []
    West = []
    for i in teleporter:
        if i['dir'] == 'NORTH':
            North.append(i) 
        elif i['dir'] == 'SOUTH':
            South.append(i)
        elif i['dir'] == 'EAST':
            East.append(i)
        elif i['dir'] == 'WEST':
            West.append(i)
    
    return North,South,East,West


def load_all_data(maps):


    data = {}

    for path in tqdm(maps, desc='Load', unit='maps'):
        data[path] = load_json(path)
    return data
def save_all_data(data,tp):
    for i in tqdm(tp, desc='Save', unit='maps'):
    
        data[i['path']]['entities'][i['id']]['settings']['map'] = i['To']['destination']
        data[i['path']]['entities'][i['id']]['settings']['marker'] = i['To']['marker']
        data[i['path']]['entities'][i['id']]['settings']['transitionType'] = 'REGULAR'
        data[i['path']]['entities'][i['id']]['settings']['spawnDistance'] = 46
    

        save_json(i['path'],data[i['path']])



def place_marker(maps):
    for path in tqdm(maps, desc='Marker', unit='maps'):
        data = load_json(path)
        
        #{"type":"Marker","x":379,"y":177,"level":0,"settings":{"size":{"x":16,"y":16},"mapId":5,"name":"spawnN","dir":"SOUTH"}}]
        tp = search_id_Tp_Ground(data)
        
        for i in tp:
            if i[4] == 'NORTH':
                data['entities'].append({"type":"Marker","x":379,"y":177,"level":0,"settings":{"size":{"x":16,"y":16},"mapId":5,"name":"spawnN","dir":"SOUTH"}})
            elif i[4] == 'SOUTH':
                data['entities'].append({"type":"Marker","x":379,"y":177,"level":0,"settings":{"size":{"x":16,"y":16},"mapId":5,"name":"spawnS","dir":"SOUTH"}})
            elif i[4] == 'EAST':
                data['entities'].append({"type":"Marker","x":379,"y":177,"level":0,"settings":{"size":{"x":16,"y":16},"mapId":5,"name":"spawnE","dir":"SOUTH"}})
            elif i[4] == 'WEST':
                data['entities'].append({"type":"Marker","x":379,"y":177,"level":0,"settings":{"size":{"x":16,"y":16},"mapId":5,"name":"spawnW","dir":"SOUTH"}})
        
        
        
       
        save_json(path,data)


#endregion








excl = ["assets\\data\\maps\\autumn\\test.json","assets\\data\\maps\\autumn\\test2.json"]

#maps = get_maps_ex(excl)

pathbase = 'assets\\data\\maps\\autumn'

maps = get_maps_zone(pathbase)
#maps = exclude_maps(excl)

for i in maps:
    if i in excl:
        maps.remove(i)

to_save = []

teleporters = resume(maps)



while len(teleporters) > 0:
    t1 = random.choice(teleporters)
    t2 = random.choice(teleporters)
    while t1['name'] == t2["name"]:
        t2 = random.choice(teleporters)

    t1s,t2s = link_tps(t1,t2)

    teleporters.remove(t1)
    teleporters.remove(t2)
    to_save.append(t1s)
    to_save.append(t2s)
    





data = load_all_data(maps)
save_all_data(data,to_save)
    


G = build_teleporter_graph(to_save)
visualize_teleporter_graph(G)



