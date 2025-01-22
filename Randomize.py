import sys
sys.path.insert(0, './libs')


import json,os,random
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx


'TODO : add doors teleporters'
'TODO : add ground teleporters for other heights'











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



#region os

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

def exclude_maps(basepath='assets\\data\\maps',paths:list[str] = []):
    exclude = ['assets\\data\\maps']
    b = {}
    for path in paths:
        d = get_all_dir(path)
        for i in d:
            exclude.append(i)
    a = get_all_file_and_dir(basepath)
    for i in a.keys():
        if i not in exclude:
            b[i] = a[i]
    return b

def get_maps_ex(basepath:str = 'assets\\data\\maps',excludepaths:list[str] = []):
    a = exclude_maps(basepath,excludepaths)
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

def search_id_Tp_Ground(data):
    TeleportGround_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportGround':   
            if data['entities'][i]['level'] == 1:
                TeleportGround_ids.append((
                    
                                                i,
                                                data['entities'][i]['type'],
                                                data['entities'][i]['settings']['name'],
                                                data['entities'][i]['settings']['map'],
                                                data['entities'][i]['settings']['dir'],
                                                data['entities'][i]['settings']['marker'],
                                                data['entities'][i]['settings']['mapId'],
                                                data['entities'][i]["x"],
                                                data['entities'][i]["y"],
                                                data['entities'][i]["settings"]["size"]["x"],
                                                data['entities'][i]["settings"]["size"]["y"],
                                                data['entities'][i]["level"],
                                            ))
    return TeleportGround_ids

def search_id_Tp_stairs(data):
    TeleportStairs_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportStairs':   
            TeleportStairs_ids.append((
                
                                            i,data['entities'][i]['type'],
                                            data['entities'][i]['settings']['name'],
                                            data['entities'][i]['settings']['map'],
                                            data['entities'][i]['settings']['stairType'],
                                            data['entities'][i]['settings']['marker'],
                                            data['entities'][i]['settings']['mapId'],
                                            
                                            
                                        ))
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
#endregion







#region edit strings

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

#endregion


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
                    "level" : i[11],
                    "id" : i[0],
                    "dir" : i[4],
                    "mapId" : i[6],
                    "marque" : None,
                    "x" : i[7],
                    "y": i[8],
                    "width" : i[9],
                    "height" : i[10],
                    "To" : {
                        "destination" : i[3],
                        "marker" : None,
                        "dir" : directinv[i[4]],
                        }
                    }
                Teleporters.append(tp)
    
    
    return Teleporters


def link_tps(tp1,tp2):
    
    tp1['To']['destination'] = tp2['name']
    tp1["marque"] = str(tp2["x"])+str(tp2["y"])
    
    
    tp2['To']['destination'] = tp1['name']
    tp2['marque'] = str(tp1["x"])+str(tp1["y"])
    
    return tp1,tp2



def load_all_data(maps):
    data = {}
    for path in tqdm(maps, desc='Load', unit='maps'):
        data[path] = load_json(path)
    return data



def save_all_data(data,tp):
    for i in tqdm(tp, desc='Randomize', unit='maps'):
        
        #Ground Teleporter
        data[i['path']]['entities'][i['id']]['settings']['map'] = i['To']['destination']
        data[i['path']]['entities'][i['id']]['settings']['marker'] = i['marque']
        data[i['path']]['entities'][i['id']]['settings']['transitionType'] = 'REGULAR'
        data[i['path']]['entities'][i['id']]['settings']['spawnDistance'] = 46
        data = add_marker(data,i)
    

        save_json(i['path'],data[i['path']])



def add_marker(data,i):
    path = i['path']
    dir = i['dir']
    tpx,tpy,tpw,tph = i['x'],i['y'],i['width'],i['height']
    level = i['level']
    
    mx = tpx + tpw / 2
    my = tpy + tph / 2
    
    
    if dir == 'NORTH':
        my += 30
        mx -= 8
    elif dir == 'SOUTH':
        my -= 30
        mx -= 8
    elif dir == 'EAST':
        mx -= 30
        my -= 8
    elif dir == 'WEST':
        mx += 30
        my -= 8
            
    Mark = {
        "type":"Marker",
        "x":round(mx),
        "y":round(my),
        "level":level,
        "settings":
            {"size":{"x":16,"y":16},
             "mapId":random.randint(208,300),
             "name":str(i["x"])+str(i["y"]),
             "dir":directinv[dir]
             }
        }
    
    data[path]["entities"].append(Mark)
    return data

    
def del_marker(maps): 
    data = load_all_data(maps)
    for i in data:
        data[i]['entities'] = [j for j in data[i]['entities'] if not (j['type'] == 'Marker' and j['settings']['name'].isdigit())]


    for i in tqdm(data, desc='verifing if marker already exist', unit='maps'):
        save_json(i,data[i])







#endregion

#region Randomizer

"""
print("Welcome to Map Randomizer")
print("")
print("Do you want to set a seed? (y/n)")
if input() == 'y':
    Seed = int(input("Seed: "))
    random.seed(Seed)
else:
    random.seed()

print("Randomize Started")"""



excl = ["assets\\data\\maps\\autumn\\test.json","assets\\data\\maps\\autumn\\test2.json"]


pathbase = 'assets\\data\\maps\\autumn'

maps = get_maps_ex(pathbase,excl)

for i in maps:
    if i in excl:
        maps.remove(i)

to_save = []

teleporters = resume(maps)

del_marker(maps)

random.shuffle(teleporters)


while len(teleporters) > 1:
    t1, t2 = teleporters.pop(), teleporters.pop()
    t1s, t2s = link_tps(t1, t2)
    to_save.extend([t1s, t2s])
    

data = load_all_data(maps)
save_all_data(data, to_save)



print("Do you want to show the teleporter graph? (y/n)")
if input() == 'y':
    G = build_teleporter_graph(to_save)
    visualize_teleporter_graph(G)




#endregion
