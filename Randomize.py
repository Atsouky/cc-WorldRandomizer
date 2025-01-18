import json,os
from tqdm import tqdm

"""
print(data['entities'][68]['settings']['map'])
print(data['entities'][87]['settings']['map'])
"""



#region os

def get_all_dir(path:str = 'assets\data\maps'):
    dirs = []
    for i in os.walk(path):
        dirs.append(i[0])
    return dirs

def get_all_file_and_dir():
    dirs = {}
    for i in os.walk('assets\data\maps'):
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

def get_maps(excludepaths:list[str] = []):
    a = exclude_maps(excludepaths)
    maps = []
    for i in a.keys():
        for j in a[i]:
            maps.append(i + '\\' + j)
    return maps

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
            TeleportGround_ids.append(i)
    return TeleportGround_ids

def search_id_Tp_stairs(data):
    TeleportStairs_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'TeleportStairs':    
            TeleportStairs_ids.append(i)
    return TeleportStairs_ids

def search_id_Tp_Doors(data):
    TeleportDoors_ids = []
    for i in range(len(data['entities'])):
        if data['entities'][i]['type'] == 'Door':    
            TeleportDoors_ids.append(i)
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







#region Randomize

import random
excludes_maps = ['assets\\data\\maps\\wm-preview' ,'assets\\data\\maps\\arena']
cache = []

NB_TP = 1731
maps = get_maps(excludes_maps)


resumed_maps = []

for path in maps:
    #print(path)
    data = load_json(path)
    Teleport_ids = search_all_Tp(data)
    if Teleport_ids == None:
        continue

    resumed_maps.append((path,Teleport_ids))
   
"""
for i in resumed_maps:
    print(i)"""

lst = ['Tp_Ground','Tp_stairs','Tp_Doors']



with tqdm(total=NB_TP + 1, desc="Processing", unit="map") as pbar:
    while len(cache) <= NB_TP:
        map1=random.randint(0,len(resumed_maps)-1)
        map2=random.randint(0,len(resumed_maps)-1)

        randomChoice1 = random.choice(lst)
        randomChoice2 = random.choice(lst)
        
        while resumed_maps[map1][1][randomChoice1] == [] or resumed_maps[map2][1][randomChoice2] == []:
            if resumed_maps[map1][1][randomChoice1] == []: 
                randomChoice1 = random.choice(lst)
            if resumed_maps[map2][1][randomChoice2] == []: 
                randomChoice2 = random.choice(lst)
        
        randomId1 = random.choice(resumed_maps[map1][1][randomChoice1])
        randomId2 = random.choice(resumed_maps[map2][1][randomChoice2])
        
        
        
        if (map1, randomId1, map2, randomId2) not in cache and (map2, randomId2, map1, randomId1) not in cache:
            
            cache.append((map1,randomId1,map2,randomId2))
            
            pbar.update(1)
    


all_data = {path: load_json(path) for path in maps}

# Perform swaps using `all_data`
for i, j, k, l in tqdm(cache, desc="Swapping", unit="map"):
    data1 = all_data[resumed_maps[i][0]]
    data2 = all_data[resumed_maps[k][0]]

    data1, data2 = swap_room(data1, data2, j, l)
    all_data[resumed_maps[i][0]] = data1
    all_data[resumed_maps[k][0]] = data2

# Write back to files at the end
for path, data in tqdm(all_data.items(), desc="Writing Files", unit="map"):
    save_json(path, data)
    
        
        


#endregion