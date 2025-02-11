import sys
sys.path.insert(0, './libs')


import json,os,random
from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk,messagebox , filedialog
import shutil
import threading
import re






#region NetworkX

def visualize_teleporter_graph(G):
    """
    Improved visualization of the teleporter graph with a structured layout.
    """
    plt.figure(figsize=(12, 12))

    # Use a better layout for clearer room connections
    pos = nx.kamada_kawai_layout(G)  # Alternative: nx.shell_layout(G)

    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", edge_color="gray", 
        node_size=2000, font_size=10, font_color="black", arrowsize=20
    )

    edge_labels = nx.get_edge_attributes(G, "direction")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Teleporter Network")
    plt.show()



def build_teleporter_graph(teleporters):
    """
    Builds an undirected graph of teleporters and their connections.
    """
    G = nx.Graph()  # Change to undirected

    for tp in teleporters:
        G.add_node(tp["name"], path=tp["path"], dir=tp["dir"])

        if tp["destination"]:
            # Ensure bidirectional linking
            G.add_edge(tp["name"], tp["destination"], direction=tp["dir"])
            G.add_edge(tp["destination"], tp["name"], direction=directinv.get(tp["dir"], ""))

    return G


#endregion


#region os

directinv = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'EAST': 'WEST', 'WEST': 'EAST'}




exclusion_patterns = [
    r"assets/data/maps/arena/.*",
    r"assets/data/maps/.*test.*",
    r'assets/data/maps/.*template.*',
    r'assets/data/maps/.*old.*',
    r'assets/data/maps/wm-preview/.*',
    r"assets/data/maps/puzzle-ideas/.*",
    r"assets/data/maps/path-finding/.*",
    r"assets/data/maps/minigames/.*", 
    r'assets/data/maps/flashback/.*',
    r'assets/data/maps/hideout/.*',
    r'assets/data/maps/final-dng/.*',
    r'assets/data/maps/evo-village/.*',
    r'assets/data/maps/dreams/.*',
    r'assets/data/maps/bmt/.*',
    r'assets/data/maps/cliff-mod.json',
    r'assets/data/maps/empty.json',
    r'assets/data/maps/.*henne.*',
    r'assets/data/maps/enemy-fishgear.json',
    r"assets/data/maps/enemy-snowman.json",
    r"assets/data/maps/killer-mice.json",
    r"assets/data/maps/meta-space.json",
    r"assets/data/maps/newgame.json",
    r"assets/data/maps/rhombus-square-view.json",
    r"assets/data/maps/room1-old.json",
    r"assets/data/maps/room2.json",
    r'assets/data/maps/cargo-ship/.*',

]


def is_excluded(file_path, exclusion_patterns):
    
    file_path = file_path.replace("\\", "/")
    
    return any(re.search(pattern, file_path) for pattern in exclusion_patterns)

def get_maps_ex(path, exclusion_patterns):
    maps = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            if not is_excluded(full_path, exclusion_patterns):
                maps.append(full_path)
    return maps

#endregion



#region json

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erreur lors du chargement de {path}: {e}")
        return None

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

#endregion


#region edit strings


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

def find_teleporters(maps):
    progress_bar["value"] = 0
    teleporters = []
    for path in maps:
        try : data = load_json(path)
        except: messagebox.showerror("Error", "Can't open file "+path)
        
        
        progress_bar["value"] += 100/len(maps)
        for i, entity in enumerate(data['entities']):
             
            if entity['type'] in {'TeleportGround', 'Door'} and entity['settings']['map']:
                
                
                
                teleporters.append({
                    "id": i, 
                    "name" : tp_name(path), 
                    "level" : entity.get('level', 1),
                    "type": entity.get("type", "TeleportGround"),
                    "path": path,
                    "dir": entity['settings'].get('dir', ''),
                    "x": entity.get("x", 0),
                    "y": entity.get("y", 0),
                    "width": entity.get("settings", {}).get("size", {}).get("x", 15),
                    "height": entity.get("settings", {}).get("size", {}).get("y", 15),
                    "destination": None,
                    "marker" : None
                })
            
    return teleporters

def seperated_teleporters(teleporters):
    tp1 = []
    tp2 = []
    for i in teleporters:
        if i['type'] == 'TeleportGround':
            if i["level"] == 1:
                tp1.append(i)
            
        elif i['type'] == 'Door':
            tp2.append(i)
    return tp1,tp2



def link_tps(tp1,tp2):
    
    tp1['destination'] = tp2['name']
    tp2['destination'] = tp1['name']
    
    tp1["marker"] = str(tp2["x"])+str(tp2["y"])
    tp2['marker'] = str(tp1["x"])+str(tp1["y"])
    
    return tp1,tp2







def save_all_data(data, tp):
    progress_bar["value"] = 0
    total = len(tp)
    progress_step = 100 / total
    modified_paths = set()  # Track modified paths to batch save

    for index, i in enumerate(tp):
        settings = data[i['path']]['entities'][i['id']]['settings']
        
        # Update settings
        settings.update({
            'map': i['destination'],
            'marker': i["marker"]
        })

        if i['type'] == 'TeleportGround':
            settings.update({'transitionType': 'REGULAR', 'spawnDistance': 46})
        elif i['type'] == 'Door':
            settings.update({'doorType': 'REGULAR'})

        add_marker(data, i)  # Assuming this modifies `data` in place
        modified_paths.add(i['path'])

        

    # Save all modified paths at the end
    for path in modified_paths:
        save_json(path, data[path])
        progress_bar["value"] += progress_step
        progress_label.config(text=f"Progress Save: {round(progress_bar['value'])}%")



def add_marker(data,i):
    path = i['path']
    dir = i['dir']
    tpx,tpy,tpw,tph = i['x'],i['y'],i['width'],i['height']
    level = i['level']
    
    mx = tpx + tpw / 2
    my = tpy + tph / 2
    
    if i['type'] == 'TeleportGround':
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
            
    elif i['type'] == 'Door':
        if dir == 'NORTH':
            my -= 24    
        elif dir == 'SOUTH':
            my += 24
        elif dir == 'EAST':
            mx += 16
        elif dir == 'WEST':
            mx -= 16
            
    if i['type'] == 'TeleportGround': d = directinv[dir]
    else: d = dir
    
    Mark = {
        "type":"Marker",
        "x":round(mx),
        "y":round(my),
        "level":level,
        "settings":
            {"size":{"x":16,"y":16},
             "mapId":random.randint(208,300),
             "name":str(i["x"])+str(i["y"]),
             "dir":d
             }
        }
    
    data[path]["entities"].append(Mark)
    return data

    

def show_graph():
    global exclusion_patterns
    pathbase = 'assets\\data\\maps\\autumn'
    #pathbase = 'assets\\data\\maps'
    maps = get_maps_ex(pathbase, exclusion_patterns)
    teleporters , doors = seperated_teleporters(find_teleporters(maps))
    G = build_teleporter_graph(teleporters)
    visualize_teleporter_graph(G)
    G = build_teleporter_graph(doors)
    visualize_teleporter_graph(G)


# Folder selection and copy function
def copy_folder_to_assets_data():
    source_folder = filedialog.askdirectory(title="Select Folder to Copy")
    if not source_folder:
        messagebox.showwarning("No Folder Selected", "You must select a folder.")
        return

    dest_folder = os.path.join(os.getcwd(), "assets", "data",'maps')
    os.makedirs(dest_folder, exist_ok=True)

    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    total_files = len(files)
    if total_files == 0:
        messagebox.showinfo("Empty Folder", "The selected folder has no files to copy.")
        return

    # Update progress bar
    progress_bar["value"] = 0
    progress_label.config(text="Copying files...")
    progress_step = 100 / total_files

    try:
        for idx, file_path in enumerate(files, 1):
            relative_path = os.path.relpath(file_path, source_folder)
            dest_path = os.path.join(dest_folder, relative_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)

            # Update the progress bar
            progress_bar["value"] += progress_step
            progress_label.config(text=f"Copying files: {idx}/{total_files}")
            app.update_idletasks()

        #messagebox.showinfo("Success", f"Folder contents successfully copied to {dest_folder}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        progress_bar["value"] = 100
        progress_label.config(text="Copy complete.")




def connect_doors(doors):
    random.shuffle(doors)
    connected = []
    
    while len(doors) > 2:
        tp1 = doors.pop()
        tp2 = doors.pop()
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        progress_label.config(text=f"Progress: {len(doors)} left")
    return connected



def connect_tps(doors):
    random.shuffle(doors)
    door = doors.copy()
    connected = []
    connect = False
    while connect == False:
        while len(door) > 2:
            tp1 = door.pop()
            tp2 = door.pop()
            tp1, tp2 = link_tps(tp1, tp2)
            connected.extend([tp1, tp2])
        G = build_teleporter_graph(connected)
        if len(list(nx.connected_components(G))) == 1:
            connect = True
        else:
            door = doors.copy()
            random.shuffle(door)
            connected = []
    
            
    visualize_teleporter_graph(G)
    
    return connected

def change_tp_links(tp1,tp2,tp3,tp4):
    """
    link tp1 to tp3
    link tp2 to tp4
    """
    
    tp1['destination'] = tp3['name']
    tp2['destination'] = tp4['name']
    
    tp1["marker"] = str(tp3["x"])+str(tp3["y"])
    tp2['marker'] = str(tp4["x"])+str(tp4["y"])
    
    tp3['destination'] = tp1['name']
    tp4['destination'] = tp2['name']
    
    tp3["marker"] = str(tp1["x"])+str(tp1["y"])
    tp4['marker'] = str(tp2["x"])+str(tp2["y"])
    
    return tp1,tp2,tp3,tp4
    
    
    
    
    

import random
import networkx as nx

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True  # Successfully merged
        return False  # Already connected

def connect_tps(doors):
    random.shuffle(doors)
    uf = UnionFind(len(doors))  # Track connected components
    connected = []
    
    for i in range(0, len(doors) - 1, 2):  # Pair doors sequentially
        tp1, tp2 = doors[i], doors[i + 1]
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        uf.union(i, i + 1)

    # Ensure full connectivity
    G = build_teleporter_graph(connected)
    components = list(nx.connected_components(G))

    if len(components) > 1:
        for i in range(len(components) - 1):  
            tp1 = list(components[i])[0]  
            tp2 = list(components[i + 1])[0]  
            tp1, tp2 = link_tps(tp1, tp2)
            connected.extend([tp1, tp2])
            uf.union(tp1, tp2)

    visualize_teleporter_graph(G)
    return connected


def create_rooms(teleporters):
    rooms = {}
    for tp in teleporters:
        if tp["name"] not in rooms:
            rooms[tp["name"]] = []
        rooms[tp['name']].append(tp)
    return rooms


    


# Randomization process in a separate thread
def randomize_process(seed_value):
    global exclusion_patterns
    if seed_value.isdigit():
        random.seed(int(seed_value))
    else:
        random.seed()

    progress_bar["value"] = 0
    progress_label.config(text="Progress: Starting randomization...")
    progress_bar_Total['value'] = 10
    
    
    pathbase = 'assets\\data\\maps\\autumn'
    #pathbase = 'assets\\data\\maps'
    maps = get_maps_ex(pathbase, exclusion_patterns)
    

    to_save = []
    t = find_teleporters(maps)
    teleporters , doors = seperated_teleporters(t)

    progress_bar_Total["value"] = 30
    
    #del_marker(maps)
    
    progress_bar_Total["value"] = 40

    to_save = connect_doors(doors)
    #room = create_rooms(teleporters)
    
    
    
    progress_bar_Total["value"] = 50
    
    
    data = {path: load_json(path) for path in maps}
    save_all_data(data, to_save)
    
    progress_label.config(text="Progress: Randomizing teleporters...")
    
    to_save = []
    
    progress_bar_Total["value"] = 70
    
    
    #to_save = connect_doors(teleporters)
    to_save = connect_tps(teleporters)
    
    
    
    if to_save is None:
        messagebox.showerror("Error", "Failed to generate a valid teleporter network after multiple attempts!")
        return

    
    
    
    progress_bar_Total["value"] = 80
    
    progress_label.config(text="Progress: Randomizing doors...")
    data = {path: load_json(path) for path in maps}
    save_all_data(data, to_save)

       
    progress_bar_Total["value"] = 100
    progress_bar["value"] = 100
    progress_label.config(text="Progress: Randomization complete!")
    messagebox.showinfo("Success", "Randomization complete!")
    start_button.config(state="normal")
    graph_button.config(state="normal")
    quit()






def start_randomization():
    copy_folder_to_assets_data()
    seed_value = seed_entry.get()
    start_button.config(state="disabled")
    graph_button.config(state="disabled")

    # Start the randomization process in a separate thread
    threading.Thread(target=randomize_process, args=(seed_value,), daemon=True).start()










# Tkinter UI setup
app = tk.Tk()
app.title("Map Randomizer")
app.geometry("600x400")

# UI Elements
label = tk.Label(app, text="Map Randomizer", font=("Arial", 16))
label.pack(pady=10)

seed_label = tk.Label(app, text="Enter Seed (optional):")
seed_label.pack(pady=5)
seed_entry = tk.Entry(app)
seed_entry.pack(pady=5)

start_button = tk.Button(app, text="Start Randomization", command=start_randomization)
start_button.pack(pady=10)

progress_label = tk.Label(app, text="Progress:")
progress_label.pack(pady=5)

progress_bar_Total = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
progress_bar_Total.pack(pady=5)

progress_bar = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

graph_button = tk.Button(app, text="Show Teleporter Graph", command= show_graph)
graph_button.pack(pady=10)




# Run the app
app.mainloop()




"""



montrer les lien de paranté entre l'espece humaine et les autres primates


pour voire si on a un lien de parentée avec les primate on va dabord regarder ce qu'est un lien de parantée entre espece

on dit qu'un espece a un lien de parentée quant ces deux espece on un caractère commun comme par exemple les ongle / les griffe
une lien de parentée ne veux pas dire que l'on déscent de cette espece mais plutot qu'un encètre commun a eu un mutation qui a 
donnée une nouvelle ligné d'espece.

donc pour les primate et les humain nous avons de nombreux caractère commun :
- ongle 
- pouce inverser
- poile 
- petite queue -> coxys
- plissement accru du cortex
- fusion des os du poignet
- orbite en avant 










"""

















