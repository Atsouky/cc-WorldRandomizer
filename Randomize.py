import json, os, random, re, shutil, threading
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import ttk,messagebox , filedialog


PATHBASE = 'assets\\data\\maps'
ENEMY_NAME = ['arid.virus-neutral', 'arid.virus-heat', 'arid.virus-cold', 'meerkat-alt', 'meerkat', 'hedgehog', 'hedgehog-alt', 'buffalo-alt', 'buffalo', 'autumn-fall.hedgehog-fall', 'autumn-fall.seahorse-fall', 'autumn-fall.buffalo-fall', 'autumn-fall.meerkat-fall', 'forest.spider', 'gray-frobbit', 'seahorse', 'goat', 'penguin', 'frobbit', 'snowman', 'forest.bug-samurai-shock', 'forest.bug-samurai-heat', 'forest.panda', 'heat.scorpion', 'heat.drillertoise', 'heat.sandshark', 'heat.sandworm', 'heat.volturbine', 'heat.scorpion-alt', 'heat.special.volturbine-cave', 'heat.jellyfish', 'heat.moth', 'heat.heat-golem', 'heat.darth-moth', 'jungle.parrot', 'jungle.plant', 'jungle.blob', 'jungle.shockcat', 'jungle.fish', 'jungle.sloth', 'jungle.chicken', 'jungle.ghost', 'jungle.powerplant', 'jungle.blob-wave', 'jungle.octopus', 'jungle.blueray', 'mine-runbot']
unstable_link = []

#region NetworkX

def visualize_teleporter_graph(G):
    """
    Improved visualization of the teleporter graph with a structured layout.
    """
    plt.figure(figsize=(12, 12))

    # Use a better layout for clearer room connections
    #pos = nx.kamada_kawai_layout(G)  # Alternative: nx.shell_layout(G)
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", edge_color="gray", 
        node_size=2000, font_size=10, font_color="black"
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

    # Define direction inversions (if not already defined elsewhere)
    directinv = {"NORTH": "SOUTH", "SOUTH": "NORTH", "EAST": "WEST", "WEST": "EAST"}

    for tp in teleporters:
        G.add_node(tp["name"], path=tp["path"], dir=tp["dir"])

        if tp["destination"]:
            # Ensure bidirectional linking
            G.add_edge(tp["name"], tp["destination"], direction=tp["dir"])
            # Optionally, you could also use directinv.get(tp["dir"], "") for reverse direction
            G.add_edge(tp["destination"], tp["name"], direction=directinv.get(tp["dir"], ""))

    return G



def build_teleporter_graph_rooms(teleporters):
    """
    Builds a graph where rooms are nodes and teleporters are edges between rooms.
    """
    # Create the rooms first
    rooms = create_rooms(teleporters)
    
    # Debugging: Print out the rooms
    #print("Rooms:", rooms)
    
    G = nx.Graph()  # Use undirected graph

    # Add nodes for each room
    for room, tps in rooms.items():
        G.add_node(room)  # Room name as the node
        #print(f"Added room: {room}")  # Debugging: Check room addition
    
    # Add edges between rooms based on teleporters
    for room, tps in rooms.items():
        for tp in tps:
            # Debugging: Check teleporter connections
            #print(f"Processing teleporter: {tp['name']} between {room} and {tp['destination']}")
            
            # Find destination room by matching tp["destination"] to a room
            destination_room = next(
                (r for r, tps in rooms.items() if any(t['name'] == tp['destination'] for t in tps)),
                None
            )
            
            # Debugging: Check if destination room is found
            if destination_room:
                #print(f"Linking {room} <-> {destination_room} with teleporter {tp['name']}")
                # Add edge between rooms with teleporter name as the attribute
                G.add_edge(room, destination_room, teleporter=tp["name"])
            #else:
                #print(f"Warning: Could not find destination room for {tp['name']}")
    
    # Debugging: Print the graph edges to verify the connections
    #print("Graph edges:", list(G.edges(data=True)))
    
    return G


#endregion


#region os

directinv = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'EAST': 'WEST', 'WEST': 'EAST'}




exclusion_patterns = [
    r"assets/data/maps/readme.txt",
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
    r'assets/data/maps/rhombus-dng/.*',
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

dng_exlusion_patterns = [
    
    r'assets/data/maps/arid-dng/.*',
    r'assets/data/maps/cold-dng/.*',
    r'assets/data/maps/heat-dng/.*',
    r'assets/data/maps/shock-dng/.*',
    r'assets/data/maps/tree-dng/.*',
    r'assets/data/maps/wave-dng/.*',

    ]
    
dng_entrance_path = [
    
    'assets\\data\\maps\\arid-dng\\first\\room-01.json',
    'assets\\data\\maps\\cold-dng\\g\\center.json',
    'assets\\data\\maps\\heat-dng\\g\\room-01.json',
    'assets\\data\\maps\\shock-dng\\g\\room1.json',
    'assets\\data\\maps\\tree-dng\\g\\center-01-entrance.json',
    'assets\\data\\maps\\wave-dng\\g\\room-entrance.json'
    
]


def is_excluded(file_path, exclusion_patterns):
    
    file_path = file_path.replace("\\", "/")
    
    return any(re.search(pattern, file_path) for pattern in exclusion_patterns)

def get_maps_ex(path, exclusion_patterns):
    global dng_entrance_path, chk_dungeons
    maps = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            if not is_excluded(full_path, exclusion_patterns):
                maps.append(full_path)
    if chk_dungeons:
        for i in dng_entrance_path:
            maps.append(i)
    
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


#endregion


#region subfunctions
def find_teleporters(maps):
    global ENEMY_NAME
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
    enemy = []
    for i in teleporters:
        if i['type'] == 'TeleportGround':
            if i["level"] == 1:
                tp1.append(i)
            
        elif i['type'] == 'Door':
            if chk_dungeons:
                if i['path'] not in dng_entrance_path:
                    tp2.append(i)
            else:
                tp2.append(i)
        elif i['type'] == 'EnemySpawner':
            enemy.append(i)
            
    return tp1, tp2


def create_rooms(teleporters):
    rooms = {}
    for tp in teleporters:
        if tp["path"] not in rooms:
            rooms[tp["path"]] = []
        rooms[tp['path']].append(tp)
    return rooms


def link_tps(tp1,tp2):
    
    tp1['destination'] = tp2['name']
    tp2['destination'] = tp1['name']
    
    tp1["marker"] = str(tp2["x"])+str(tp2["y"])
    tp2['marker'] = str(tp1["x"])+str(tp1["y"])
    
    return tp1,tp2


def save_all_data(data, tp):
    progress_bar["value"] = 0
    total = len(tp)//2
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
            my -= 16    
        elif dir == 'SOUTH':
            my += 16
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
 

def show_graph(to):
    G = build_teleporter_graph(to)
    visualize_teleporter_graph(G)


def copy_folder_to_assets_data():
    source_folder = entry_folder.get()
    if not source_folder:
        messagebox.showwarning("No Folder Selected", "You must select a folder.")
        quit()

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
            progress_bar.update_idletasks()

        #messagebox.showinfo("Success", f"Folder contents successfully copied to {dest_folder}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        progress_bar["value"] = 100
        progress_label.config(text="Copy complete.")



def verify_bidirectionality(tps):
    for tp in tps:
        # On recherche la destination correspondante
        dest = [t for t in tps if t['name'] == tp['destination']]
        if dest:  # Vérifie que la destination existe
            dest = dest[0]  # Prend le premier élément correspondant
            if tp['destination'] != dest['name'] and dest['destination'] == tp['name']:
                unstable_link.append(f'{tp["name"]} <{tp["dir"]}> <-> {dest["name"]} <{dest["dir"]}>')
        else:
            print('no destination for', tp["name"])
        



#endregion


#region randomize algorithm


def connect_tp(tps, rooms):
    global unstable_link
    tp = tps.copy()
    random.shuffle(tp)
    connected = []
    
    while len(tp) > 2:
        tp1 = tp.pop()
        tp2 = tp.pop()
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        progress_label.config(text=f"Progress tp : {len(tp)} left")
    comp = list(nx.connected_components(build_teleporter_graph(connected)))
    
    if len(tp) == 2:
        tp1 = tp.pop()
        tp2 = tp.pop()
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        comp = list(nx.connected_components(build_teleporter_graph(connected)))
    
    mini = len(comp)
    while len(comp) > 7 :
        tp = tps.copy()
        random.shuffle(tp)
        connected = []
        
        while len(tp) > 2:
            tp1 = tp.pop()
            tp2 = tp.pop()
            tp1, tp2 = link_tps(tp1, tp2)
            connected.extend([tp1, tp2])
            progress_label.config(text=f"Progress tp : {len(comp)} : {mini} left")
        
        comp = list(nx.connected_components(build_teleporter_graph(connected)))
        if mini>len(comp):
            mini = len(comp)
    while len(list(nx.connected_components(build_teleporter_graph(connected)))) > 1:
        comp = list(nx.connected_components(build_teleporter_graph(connected)))
        progress_label.config(text=f"Progress tp : 2 part")
        indimax = 0
        for i in range(len(comp)):
            if len(comp[i]) > len(comp[indimax]):
                indimax = i
        main = comp[indimax]
        
        comp.remove(main)
    
        for i in range(len(comp)):
            if len(comp[i]) == 0:
                continue
            name1 = random.choice(list(main))
            name2 = random.choice(list(comp[i]))
            tp1 = [i for i in connected if i["name"] == name1][0]
            tp2 = [i for i in connected if i["name"] == name2][0]
            
            destination1 = [i for i in connected if i["name"] == tp1["destination"]][0]
            destination2 = [i for i in connected if i["name"] == tp2["destination"]][0]
            
            if len(rooms[tp1['path']]) == 1 or len(rooms[destination1['path']]) == 1 :
                while len(rooms[tp1['path']]) == 1 or len(rooms[destination1['path']]) == 1:
                    
                    #print(len((rooms[tp1['path']])), len((rooms[tp2['path']])))
                    
                    name1 = random.choice(list(main))
                    name2 = random.choice(list(comp[i]))
                    tp1 = [i for i in connected if i["name"] == name1][0]
                    tp2 = [i for i in connected if i["name"] == name2][0]
                    destination1 = [i for i in connected if i["name"] == tp1["destination"]][0]
                    destination2 = [i for i in connected if i["name"] == tp2["destination"]][0]
            progress_label.config(text=f"Progress tp : 3 part")
            
            connected.remove(tp1)
            connected.remove(tp2)
            tp1, tp2 = link_tps(tp1, tp2)
            connected.extend([tp1, tp2])
            unstable_link.append(f'{tp1["name"]} <{tp1["dir"]}> <-> {tp2["name"]} <{tp2["dir"]}>')
            
            connected.remove(destination1)
            connected.remove(destination2)
            destination1, destination2 = link_tps(destination1, destination2)
            connected.extend([destination1, destination2])
            unstable_link.append(f'{destination1["name"]} <{destination1["dir"]}> <-> {destination2["name"]} <{destination2["dir"]}>')
            
            main.remove(name1)
            comp[i].remove(name2)
            
            
            progress_label.config(text=f"Progress tp : {len(tp)} left")
    
    
    #print('done')
    
    
    return connected
    





"""def connect_tp(tps):
    tp = tps.copy()
    random.shuffle(tp)
    connected = []
    
    while len(tp) > 2:
        tp1 = tp.pop()
        tp2 = tp.pop()
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        progress_label.config(text=f"Progress tp : {len(tp)} left")
    comp = len(list(nx.connected_components(build_teleporter_graph(connected))))
    atempt = 0
    mini = comp
    while comp > 1:
        tp = tps.copy()
        random.shuffle(tp)
        connected = []
        
        while len(tp) > 2:
            tp1 = tp.pop()
            tp2 = tp.pop()
            tp1, tp2 = link_tps(tp1, tp2)
            connected.extend([tp1, tp2])
            progress_label.config(text=f"Progress tp : {comp} comp, {atempt} atempt, {mini} min")
            
        comp = len(list(nx.connected_components(build_teleporter_graph(connected))))
        if mini > comp: mini = comp
        atempt += 1
    
    return connected"""



def connect_doors(doors):
    progress_label.config(text=f"tps")
    random.shuffle(doors)
    connected = []
    
    while len(doors) > 2:
        tp1 = doors.pop()
        tp2 = doors.pop()
        tp1, tp2 = link_tps(tp1, tp2)
        connected.extend([tp1, tp2])
        progress_label.config(text=f"Progress dors: {len(doors)} left")
    
    return connected

        
def randomize_enemy(maps):
    global ENEMY_NAME
    count = 0
    for path in maps:
        try : data = load_json(path)
        except: messagebox.showerror("Error", "Can't open file "+path)
        
        for i, entity in enumerate(data['entities']):
            if entity['type'] == 'EnemySpawner':
                for j in entity['settings']['enemyTypes']:
                    j['info']['type'] = random.choice(ENEMY_NAME)
        
        save_json(path, data)
        count += 1
        progress_label.config(text=f"Progress Enemy randomization: {round(count/len(maps)*100)}%")

#endregion


# Randomization process in a separate thread
def randomize_process(seed_value):
    global exclusion_patterns , PATHBASE, unstable_link
    
    if seed_value.isdigit():
        random.seed(int(seed_value))
    else:
        random.seed()

    progress_bar["value"] = 0
    progress_label.config(text="Progress: Starting randomization...")
    
    #exclusion des maps
    maps = get_maps_ex(PATHBASE, exclusion_patterns)
    
    
    #randomize enemy
    if enemy_random.get() == True:
        randomize_enemy(maps)
  
    #init to save and shearch for all tps and doors
    to_save = []
    to_savetp = []
    t = find_teleporters(maps)
    teleporters , doors = seperated_teleporters(t)
    rooms = create_rooms(teleporters)
    #randomize doors
    to_save = connect_doors(doors)
    
    #reinit to save and randomize teleporters
    
    to_savetp = connect_tp(teleporters,rooms)
    verify_bidirectionality(to_savetp)
    
    #print(unstable_link)
    
        
    
    
    G = build_teleporter_graph_rooms(to_savetp)
    #print('comp ',len(list(nx.connected_components(G))))
    #threading.Thread(target=visualize_teleporter_graph, args=(G,), daemon=True).start()
    
   
    
    for i in to_savetp:
        to_save.append(i)
    
    
    #save teleporter randomized
    data = {path: load_json(path) for path in maps}
    save_all_data(data, to_save)

    
    verify_bidirectionality(to_save)
    
    #spoiler
    
    os.makedirs("spoiler", exist_ok=True)
    
    with open("spoiler/Unstable_link.txt", "w", encoding="utf-8") as f:
        f.write("Unstable link : \n")
        for i in unstable_link:
            f.write(i)
            f.write("\n")
        
    with open("spoiler/spoiler.txt", "w", encoding="utf-8") as f:
        for i in to_save:
            f.write(f'{i["name"]} <{i["dir"]}> -> {i["destination"]}')
            f.write("\n")
    
    
    
    
    
    progress_bar["value"] = 100
    progress_label.config(text="Progress: Randomization complete!")
    messagebox.showinfo("Success", "Randomization complete!")
    
    btn_graph = ttk.Button(root, text="Afficher le Graphe des Téléporteurs", command=lambda:show_graph(to_savetp))
    btn_graph.pack(pady=10)
    quit()


def start_randomization():
    global exclusion_patterns, dng_exlusion_patterns
    
    if chk_dungeons.get() == True:
        for i in dng_exlusion_patterns:
            exclusion_patterns.append(i)
        
    
    progress_bar["value"] = 0
    copy_folder_to_assets_data()
    seed_value = entry_seed.get()
    

    # Start the randomization process in a separate thread
    threading.Thread(target=randomize_process, args=(seed_value,), daemon=True).start()


#region  Tkinter UI setup



default_folder = "C:/Program Files (x86)/Steam/steamapps/common/CrossCode/assets/data/maps"  # Replace with your desired default folder path

def browse_folder():
    folder_selected = filedialog.askdirectory(initialdir=default_folder)  # Start browsing from default folder
    if folder_selected:  # Only update if a folder is selected
        entry_folder.delete(0, tk.END)  # Clear the current entry
        entry_folder.insert(0, folder_selected)  # Insert the selected folder path

root = tk.Tk()
root.title("Map Randomizer")
root.geometry("800x420")  # Adjusted for the new components
root.resizable(False, False)

chk_dungeons = tk.BooleanVar()
enemy_random = tk.BooleanVar()

# Style général
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("TCheckbutton", font=("Arial", 10))

# Options
chk_dungeon = ttk.Checkbutton(root, text="Ne pas randomizer dans les donjons", variable=chk_dungeons, onvalue=True, offvalue=False)
chk_dungeon.pack(pady=2)

chk_enemy = ttk.Checkbutton(root, text="Randomiser les ennemis", variable=enemy_random, onvalue=True, offvalue=False)
chk_enemy.pack(pady=2)

# Titre
label_title = ttk.Label(root, text="Map Randomizer", font=("Arial", 14, "bold"))
label_title.pack(pady=10)

# Entrée pour la seed
label_seed = ttk.Label(root, text="Entrer une Seed (optionnel) :", font=("Arial", 10))
label_seed.pack()
entry_seed = ttk.Entry(root, font=("Arial", 10), width=20)
entry_seed.pack(pady=5)

# Entrée pour le dossier avec une valeur par défaut
label_folder = ttk.Label(root, text="Sélectionner un dossier :", font=("Arial", 10))
label_folder.pack(pady=5)

# Create a frame to hold the entry and button horizontally
folder_frame = ttk.Frame(root)
folder_frame.pack(pady=5)

entry_folder = ttk.Entry(folder_frame, font=("Arial", 10), width=70)
entry_folder.insert(0, default_folder)  # Set default folder path
entry_folder.pack(side="left", padx=5)

btn_browse = ttk.Button(folder_frame, text="Parcourir", command=browse_folder)
btn_browse.pack(side="right")

# Bouton de randomisation
btn_randomize = ttk.Button(root, text="Démarrer la Randomisation", command=start_randomization)
btn_randomize.pack(pady=10)

# Barre de progression
progress_label = ttk.Label(root, text="Progression :", font=("Arial", 10))
progress_label.pack()
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=250)
progress_bar.pack(pady=5)



# Lancement de l'interface
tk.mainloop()