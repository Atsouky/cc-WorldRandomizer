import json,os
from tqdm import tqdm
import random

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
            TeleportGround_ids.append((i,data['entities'][i]['type'],data['entities'][i]['settings']['name'],data['entities'][i]['settings']['map'],data['entities'][i]['settings']['dir'],data['entities'][i]['settings']['marker'],data['entities'][i]['settings']['mapId']))
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


def set_tp_ground(data,teleport,name,map,dir,marker,mapId):
    data['entities'][teleport]['settings']['name'] = name
    data['entities'][teleport]['settings']['map'] = map
    data['entities'][teleport]['settings']['dir'] = dir
    data['entities'][teleport]['settings']['marker'] = marker
    data['entities'][teleport]['settings']['mapId'] = mapId
    return data

def set_tp_stairs(data,teleport,name,map,stairType,marker,mapId):
    data['entities'][teleport]['settings']['name'] = name
    data['entities'][teleport]['settings']['map'] = map
    data['entities'][teleport]['settings']['stairType'] = stairType
    data['entities'][teleport]['settings']['marker'] = marker
    data['entities'][teleport]['settings']['mapId'] = mapId
    return data

def set_tp_doors(data,teleport,name,map,dir,marker):    
    data['entities'][teleport]['settings']['name'] = name
    data['entities'][teleport]['settings']['map'] = map
    data['entities'][teleport]['settings']['dir'] = dir
    data['entities'][teleport]['settings']['marker'] = marker
    return data

def resume(maps):
    resumed_maps = []

    for path in maps:
        #print(path)
        data = load_json(path)
        Teleport_ids = search_all_Tp(data)        
        if Teleport_ids :
            resumed_maps.append((path,Teleport_ids))
    
    """
    for i in resumed_maps:
        print(i)"""
    return resumed_maps


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
    name = name[-2]
    return name

def tp_name(name):
    a = split_name(name)
    b = split_zone(name)
    return str(b+'.'+a)

def replace_slash(name):
    name = name.replace('/','\\')
    return name

#endregion







#region Randomize
NB_TP = 1731

excludes_maps = ['assets\\data\\maps\\wm-preview' ,'assets\\data\\maps\\arena']
maps = get_maps(excludes_maps)
#resumed_maps = resume(maps)


room = [
    
    'assets/data/maps/autumn/entrance.json',
    'assets/data/maps/autumn/path-1-1.json',
    'assets/data/maps/autumn/path-1-2.json',
    'assets/data/maps/autumn/path-1-3.json',
    'assets/data/maps/autumn/path-1.json',
    'assets/data/maps/autumn/path-2.json',
    'assets/data/maps/autumn/path-3-1.json',
    'assets/data/maps/autumn/path-3-2.json',
    'assets/data/maps/autumn/path-3-4.json',
    'assets/data/maps/autumn/path4.json',
    'assets/data/maps/autumn/path5.json',
    'assets/data/maps/autumn/path6.json',
    'assets/data/maps/autumn/path-7-1.json',
    'assets/data/maps/autumn/path-7-2.json',
    'assets/data/maps/autumn/path-8.json',  
]


def labyrinthe(room):
    resumed_maps = resume(room)
    resumed_maps_count = []
    directinv = {'NORTH':'SOUTH','SOUTH':'NORTH','EAST':'WEST','WEST':'EAST'}
    
    for i in resumed_maps:
        resumed_maps_count.append((i[0],i[1],count_Tp(i)))
    #print(resumed_maps_count)
    resumed_maps=resumed_maps_count
    count = 0
    for i in resumed_maps:
        count += i[2]
    print(count)
    #print(resumed_maps)
    
    
    currant = resumed_maps[0]
    currant_tp = currant[1]['Tp_Ground'][0]
    
    used_tp = []
    used_tp.append(currant_tp)
    while len(used_tp) < count:
        
        currant_dir = currant_tp[4]
        currant_map = currant[0]
        choice = random.choice(resumed_maps)
        if choice == currant:
            continue
        choice_tp = random.choice(choice[1]['Tp_Ground'])
        
        choice_dir = choice_tp[4]
        if choice_dir != directinv[currant_dir]:
            continue
        
        print(currant_tp,choice_tp)
        temp1 = currant_tp
        temp2 = choice_tp
        currant_tp = (temp1[0],temp1[1],temp1[2],temp2[3],temp1[4],temp1[5],temp1[6])
        choice_tp = (temp2[0],temp2[1],temp2[2],temp1[3],temp2[4],temp2[5],temp2[6])
        print('---')
        
        currant = choice
        used_tp.append(currant_tp)
        used_tp.append(choice_tp)
        print(currant_tp,choice_tp)
        print('---')
        print('---')
        
        
            
       
    

labyrinthe(room)







#(448, 'TeleportGround', 'south-1', 'arid.river-1', 'SOUTH/NORTH/EAST/WEST', 'north-2', 569)
#(1, 'TeleportStairs', 'up', 'autumn.guild.inner-fs-og', 'UPWARDS_EAST/UPWARDS_NORTH/UPWARDS_SOUTH/UPWARDS_WEST', 'down', 5)
#(0, 'TeleportStairs', 'down', 'autumn.guild.inner-fs-eg', 'DOWNWARDS_WEST/DOWNWARDS_NORTH/DOWNWARDS_SOUTH/DOWNWARDS_EAST', 'up', 5)
#(1, 'Door', 'door1', 'arid.test', 'NORTH/SOUTH/EAST/WEST', 'door1')














'''
cache = []
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
    
        
        
        



"""
with tqdm(total=NB_TP + 1, desc="Processing", unit="map") as pbar:
    while len(cache) <= NB_TP:
        #print(cache)
        map1=random.randint(0,len(resumed_maps)-1)
        map2=random.randint(0,len(resumed_maps)-1)
        #print(map1, map2)
        data1 = load_json(resumed_maps[map1][0])
        data2 = load_json(resumed_maps[map2][0])
        randomChoice1 = random.choice(lst)
        randomChoice2 = random.choice(lst)
        #print(randomChoice1, randomChoice2)
        
        while resumed_maps[map1][1][randomChoice1] == [] or resumed_maps[map2][1][randomChoice2] == []:
            if resumed_maps[map1][1][randomChoice1] == []: 
                randomChoice1 = random.choice(lst)
            if resumed_maps[map2][1][randomChoice2] == []: 
                randomChoice2 = random.choice(lst)
        
        
        
        randomId1 = random.choice(resumed_maps[map1][1][randomChoice1])
        randomId2 = random.choice(resumed_maps[map2][1][randomChoice2])
        
        if (map1,randomId1) in cache or (map2,randomId2) in cache:
            continue
        
        
        #print(randomId1, randomId2)
        
        name1 = data1['entities'][randomId1]['settings']['name']
        name2 = data2['entities'][randomId2]['settings']['name']
        #print(name1, name2)
        
        
        
        #print(data1['entities'][randomId1]['settings']['map'],data2['entities'][randomId2]['settings']['map'])
        
        
        if (map1, randomId1) not in cache and (map2, randomId2) not in cache:
            
            cache.append((map1, randomId1))
            cache.append((map2, randomId2))
            
            swap_room(data1, data2, randomId1, randomId2)
            
            save_json(resumed_maps[map1][0], data1)
            save_json(resumed_maps[map2][0], data2)
            
            pbar.update(1)
    """        
            

#endregion


'''




