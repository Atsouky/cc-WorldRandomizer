import re,os,json



PATHBASE = 'assets\\data\\maps'

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
    r'assets/data/maps/rookie-harbor/north2.json',

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




class Room:
    def __init__(self,name,region,dir,items = None,teleporters = None):
        self.name = name
        self.region = region
        self.dir  = dir
        self.items = items if items else []
        self.teleporters:list[Teleporter] = teleporters if teleporters else []
        self.markers = []
    
    def __repr__(self):
        return self.region+'.'+self.name
    
    def add_marker(self,marker):
        self.markers.append(marker)
        


class Teleporter:
    def __init__(self,name,destination,x,y,dx,dy,direction,dir,condition = None):
        self.name = name
        self.destination = destination
        self.condition = condition if condition else []
        self.coord = [x,y]
        self.size = [dx,dy]
        self.dir = dir
        self.direction = direction
        self.marker = str(x)+str(y)
    
    def add_condition(self,condition):
        self.condition.append(condition)
        
    def __repr__(self):
        return self.name + ' -> ' + self.destination 
        
        
def path_to_name(path):
    return path.split('\\')[-1].split('.')[0]

def path_to_region(path):
    return  path.split('assets\\data\\maps\\')[-1].replace('\\','.').replace('.json','').replace(path_to_name(path),'').removesuffix('.')
def path_to_entity(path):
    return path_to_region(path)+'.'+path_to_name(path)
 

def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erreur lors du chargement de {path}: {e}")
        return None

def save(path,data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
        
def get_teleporters(path):
    data = load(path)
    teleporters = []
    for i in data['entities']:
        if i['type'] == 'TeleportGround':
            
            teleporters.append(Teleporter(path_to_entity(path),
                                          i['settings']['map'],
                                          i['x'],i['y'],
                                          i['settings']['size']['x'],
                                          i['settings']['size']['y'],
                                          i['settings']['dir'],
                                          path
                                          ))
    return teleporters





maps = {}
teleporters = []
for i in get_maps_ex(PATHBASE, exclusion_patterns):
    maps[i] = (Room(path_to_name(i),path_to_region(i),i))
    teleporters.extend(get_teleporters(i))
    
for i in teleporters:
    maps[i.dir].teleporters.append(i)







