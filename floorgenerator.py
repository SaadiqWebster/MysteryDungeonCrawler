import random

# change to True to turn on
DEBUG = {
    'path_origins': False,
    'path_highlight': False,
    'entrance_highlights': False,
    'shortcut_highlights': False,
    'dead_end_highlight': False
}

class Room:
    def __init__(self, width, height):
        self.cor = [0,0]
        self.width = width
        self.height = height
        self.entrances = []

class FloorGenerator:
    def __init__(self):
        self.floor_width = 1
        self.floor_height = 1
        self.tile_size = 1
        self.floor_map = self.generate_empty_map(0)
        self.room_map = self.generate_empty_map(-1)
        self.rooms = {}
        self.max_rooms = 0
        self.min_room_size = [3,3]
        self.max_room_size = [10,10]
        self.max_room_area = 0
        self.max_path_size = -1
        self.num_shortcuts = 0
        self.shortcut_threshold = 0
        self.MAX_FAILURES = 7

    def get_map_value(self, map, cor):
        return map[cor[1]][cor[0]]

    def get_floor_map(self, cor):
        return self.get_map_value(self.floor_map, cor)

    def get_room_map(self, cor):
        return self.get_map_value(self.room_map, cor)
    
    def get_room(self, room_id):
        return self.rooms[room_id]
    
    def get_random_room(self):
        return random.choice([int(k) for k in self.rooms.keys()]) if len(self.rooms) > 0 else -1
        # one day try changing this so you don't need to create entire list of keys first

    def get_tile_signature(self, cor):
        signature = ''
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    tile = [cor[0]+i, cor[1]+j]
                    signature += '1' if not self.isinbound(tile) or self.get_floor_map(tile) == 0 else '0'
        return signature

    def set_floor_properties(self, properties):
        self.floor_width = properties['floor_width']
        self.floor_height = properties['floor_height']
        self.tile_size = properties['tile_size']
        self.max_rooms = properties['max_rooms']
        self.min_room_size = properties['min_room_size']
        self.max_room_size = properties['max_room_size']
        self.max_room_area = properties['max_room_area']
        self.max_path_size = properties['max_path_size']
        self.num_shortcuts = properties['num_shortcuts']
        self.shortcut_threshold = properties['shortcut_threshold']

    def set_map_value(self, map, cor, value):
        map[cor[1]][cor[0]] = value

    def set_floor_map(self, cor, value):
        self.set_map_value(self.floor_map, cor, value)

    def set_room_map(self, cor, value):
        return self.set_map_value(self.room_map, cor, value)

    def isinbound(self, cor):
        return cor[0] > 0 and cor[1] > 0 and cor[0] < self.floor_width-1 and cor[1] < self.floor_height-1

    def isroom(self, cor):
        return self.get_room_map(cor) != -1

    def iscarvable(self, cor):
        if self.get_floor_map(cor) != 0 or not self.isinbound(cor):
            return False
        carvable_signatures = ['11111111','11111x0x','x1101x11','x0x11111','11x1011x']
        tile_signature = self.get_tile_signature(cor)
        for valid_signature in carvable_signatures:
            if self.signature_compare(tile_signature, valid_signature):
                return True
        return False

    def signature_compare(self, sig1, sig2):
        for i in range(len(sig1)):
            if sig1[i] != 'x' and sig2[i] != 'x' and sig1[i] != sig2[i]:
                return False
        return True
    
    def find_walkable_neighbors(self, cor):
        neighbors = []
        for i in range(-1,2):
            for j in range(-1,2):
                if i != 0 or j != 0:
                    neighbor = [cor[0]+i, cor[1]+j]
                    if self.isinbound(neighbor) and self.get_floor_map(neighbor) != 0:
                        neighbors.append(neighbor)
        return neighbors
    
    def generate_empty_map(self, default_value):
        return [[default_value for i in range(self.floor_width)] for j in range(self.floor_height)]
    
    def print_map(self, map):
        printstr = ''
        for i in range(self.floor_height):
            for j in range(self.floor_width):
                if map[i][j] > -1 and map[i][j] < 10:
                    printstr += ' '
                printstr += str(map[i][j]) + ' '
            printstr += '\n'
        print(printstr)
        return printstr

    def generate_mark_map(self):
        mark_map = self.generate_empty_map(0)
        mark = 1
        for x in range(self.floor_width):
            for y in range(self.floor_height):
                cor = [x,y]
                if self.get_floor_map(cor) != 0 and self.get_map_value(mark_map, cor) == 0:
                    mark_map = self.mark_map_neighbors(mark_map, cor, mark)
                    mark += 1
        return mark_map

    def mark_map_neighbors(self, mark_map, cor, mark):
        self.set_map_value(mark_map, cor, mark)
        neighbors = self.find_walkable_neighbors(cor)
        for neighbor_cor in neighbors:
            if self.get_map_value(mark_map, neighbor_cor) != mark:
                mark_map = self.mark_map_neighbors(mark_map, neighbor_cor, mark)
        return mark_map

    # a lot faster than before but still causes slowness a bit, maybe optimize further in the future
    def generate_distance_map(self, start_cor):
        distance_map = self.generate_empty_map(-1)
        unmarked_tiles = [start_cor]
        distance = 0

        while len(unmarked_tiles) > 0:
            adjacent_tiles = []
            for tile in unmarked_tiles:
                if self.get_map_value(distance_map, tile) == -1:
                    self.set_map_value(distance_map, tile, distance)
                    for neighbor in self.find_walkable_neighbors(tile):
                        if self.get_map_value(distance_map, neighbor) == -1:
                            adjacent_tiles.append(neighbor)
            unmarked_tiles = adjacent_tiles
            distance += 1
        
        return distance_map

    def generate_floor_test(self):
        self.floor_map = [[0 for i in range(7)] for j in range(7)]
        self.room_map = [[0 for i in range(7)] for j in range(7)]
        self.floor_height = len(self.floor_map)
        self.floor_width = len(self.floor_map[0])
        self.rooms = {}
        testroom = self.generate_room(self.floor_width-2, self.floor_height-2)
        testroom.cor = (1,1)
        self.place_room(testroom, 1)
        return self.floor_map
    
    def generate_floor(self):
        self.floor_map = self.generate_empty_map(0)
        self.room_map = self.generate_empty_map(-1)
        self.rooms = {}
        self.spawn_rooms(self.max_rooms, self.max_room_area)
        self.spawn_paths(self.max_path_size)
        self.expand_paths()
        self.carve_entrances()
        self.carve_shortcuts(self.num_shortcuts, self.shortcut_threshold)
        self.fill_dead_ends()
        return self.floor_map
    
    def generate_room(self, width, height):
        return Room(width, height)
    
    def generate_random_room(self, minroomsize, maxroomsize, maxroomarea):
        width = random.randint(minroomsize[0], maxroomsize[0])
        height = random.randint(minroomsize[1], maxroomsize[1])

        if random.randint(0,1) == 0:
            maxheight = max(maxroomarea // width, minroomsize[1])
            height = random.randint(minroomsize[1], maxheight)
        else:
            maxwidth = max(maxroomarea // height, minroomsize[0])
            width = random.randint(minroomsize[0], maxwidth)
        
        return Room(width, height)

    def spawn_rooms(self, maxrooms, maxroomarea):
        num_rooms = 0
        num_failures = 0
        room_id = 0

        while num_rooms < maxrooms and num_failures < self.MAX_FAILURES:
            room = self.generate_random_room(self.min_room_size, self.max_room_size, maxroomarea)
            if self.place_room(room, room_id):
                num_rooms += 1
                room_id += 1
            else:
                num_failures += 1

    def place_room(self, room, room_id):
        room_coordinates = []
        for x in range(self.floor_width - room.width):
            for y in range(self.floor_height - room.height):
                if self.can_room_fit(room, [x,y]):
                    room_coordinates.append([x,y])

        if len(room_coordinates) > 0:
            room.cor = random.choice(room_coordinates)
            self.rooms[room_id] = room
            for x in range(room.width):
                for y in range(room.height):
                    tile = [x+room.cor[0], y+room.cor[1]]
                    self.set_room_map(tile, room_id)
                    self.set_floor_map(tile, 1)
            return True
        else:
            return False
    
    def can_room_fit(self, room, cor):
        if not self.isinbound(cor) or not self.isinbound([cor[0]+room.width-1, cor[1]+room.height-1]):
            return False
        for i in range(cor[0]-1, cor[0]+room.width+1):
            for j in range(cor[1]-1, cor[1]+room.height+1):
                if self.get_floor_map([i,j]) != 0:
                    return False      
        return True

    def spawn_paths(self, maxpathsize=-1):
        path_coordinates = []
        for x in range(1, self.floor_width-1):
            for y in range(1, self.floor_height-1):
                if self.get_floor_map([x,y]) == 0 and self.get_tile_signature([x,y]) == '11111111':
                    path_coordinates.append([x,y])

        if len(path_coordinates) > 0:
            cor = random.choice(path_coordinates)
            self.carve_path(cor, maxpathsize)
            if DEBUG['path_origins']:
                self.set_floor_map(cor, 3)
            self.spawn_paths()
    
    def carve_path(self, cor, maxpathsize=-1):
        dir_x = [0,0,-1,1]
        dir_y = [-1,1,0,0]
        pathsize = 1
        direction = random.randint(0, len(dir_x)-1)

        while self.iscarvable(cor):
            map_value = 1 if not DEBUG['path_highlight'] else 2
            self.set_floor_map(cor, map_value)
            pathsize += 1
            next_cor = [cor[0]+dir_x[direction], cor[1]+dir_y[direction]]
            if not self.iscarvable(next_cor) or (maxpathsize > -1 and pathsize >= maxpathsize):
                pathsize = 1
                valid_directions = []
                for i in range(len(dir_x)):
                    if i != direction and self.iscarvable([cor[0]+dir_x[i], cor[1]+dir_y[i]]):
                        valid_directions.append(i)
                if len(valid_directions) > 0:
                    direction = random.choice(valid_directions)
                else:
                    return False # end the carving entirely
            cor = [cor[0]+dir_x[direction], cor[1]+dir_y[direction]]

        return True
    
    def expand_paths(self):
        dir_x = [0,0,-1,1]
        dir_y = [-1,1,0,0]
        expand_coordinates = []

        # try removing the next_to_room part
        for x in range(self.floor_width):
            for y in range(self.floor_height):
                if self.iscarvable([x,y]):
                    next_to_room = False
                    for i in range(len(dir_x)):
                        adjacent_cor = [x+dir_x[i], y+dir_y[i]]
                        if self.isroom(adjacent_cor):
                            next_to_room = True
                    if not next_to_room:
                        expand_coordinates.append([x,y])
        
        if len(expand_coordinates) > 0:
            cor = random.choice(expand_coordinates)
            map_value = 1 if not DEBUG['path_highlight'] else 2
            self.set_floor_map(cor, map_value)
            self.expand_paths()

    def find_carvable_entrances(self):
        carvable_signatures = ['x0x11x0x','x1x00x1x']
        coordinates = []
        for x in range(self.floor_width):
            for y in range(self.floor_height):
                adjacent_cor1, adjacent_cor2 = [x,y], [x,y]
                if self.isinbound([x,y]) and self.get_floor_map([x,y]) == 0:
                    if self.signature_compare(self.get_tile_signature([x,y]), carvable_signatures[0]):
                        adjacent_cor1[0] -= 1
                        adjacent_cor2[0] += 1
                        coordinates.append([[x,y], adjacent_cor1, adjacent_cor2])
                    elif self.signature_compare(self.get_tile_signature([x,y]), carvable_signatures[1]):
                        adjacent_cor1[1] -= 1
                        adjacent_cor2[1] += 1
                        coordinates.append([[x,y], adjacent_cor1, adjacent_cor2])
        return coordinates

    def carve_entrances(self):
        mark_map = self.generate_mark_map()
        entrance_coordinates = self.find_carvable_entrances()

        while len(entrance_coordinates) > 0:
            i = random.randint(0, len(entrance_coordinates)-1)
            coordinate_list = entrance_coordinates[i]
            door_cor = coordinate_list[0]
            adjacent_cor1 = coordinate_list[1]
            adjacent_cor2 = coordinate_list[2]

            mark1 = self.get_map_value(mark_map, adjacent_cor1)
            mark2 = self.get_map_value(mark_map, adjacent_cor2)
            if mark1 != mark2:
                map_value = 1 if not DEBUG['entrance_highlights'] else 3
                self.set_floor_map(door_cor, map_value)
                mark_map = self.mark_map_neighbors(mark_map, door_cor, mark1)
                
                if self.isroom(adjacent_cor1):
                    room_id = self.get_room_map(adjacent_cor1)
                    room = self.get_room(room_id)
                    room.entrances.append(adjacent_cor1)
                if self.isroom(adjacent_cor2):
                    room_id = self.get_room_map(adjacent_cor2)
                    room = self.get_room(room_id)
                    room.entrances.append(adjacent_cor2)
            
            entrance_coordinates.pop(i)

    # may not need to call find_carvable_entrances multiple times? casues slowness, further optimize later.
    def carve_shortcuts(self, maxshortcuts, distance_threshold):
        if maxshortcuts > 0:
            entrance_coordinates = self.find_carvable_entrances()
            
            while len(entrance_coordinates) > 0:
                i = random.randint(0, len(entrance_coordinates)-1)
                coordinate_list = entrance_coordinates[i]
                shortcut_cor = coordinate_list[0]
                adjacent_cor1 = coordinate_list[1]
                adjacent_cor2 = coordinate_list[2]

                distance_map = self.generate_distance_map(adjacent_cor1)
                if self.get_map_value(distance_map, adjacent_cor2) >= distance_threshold:
                    map_value = 1 if not DEBUG['shortcut_highlights'] else 5
                    self.set_floor_map(shortcut_cor, map_value)
                    self.carve_shortcuts(maxshortcuts-1, distance_threshold)

                    if self.isroom(adjacent_cor1):
                        room_id = self.get_room_map(adjacent_cor1)
                        room = self.get_room(room_id)
                        room.entrances.append(adjacent_cor1)
                    if self.isroom(adjacent_cor2):
                        room_id = self.get_room_map(adjacent_cor2)
                        room = self.get_room(room_id)
                        room.entrances.append(adjacent_cor2)
                    
                    return
                else:
                    entrance_coordinates.pop(i)
    
    def fill_dead_ends(self):
        for x in range(self.floor_width):
            for y in range(self.floor_height):
                # need to figure out how to get walkable neighbors of cardinal directions
                if self.get_floor_map([x,y]) != 0 and self.get_floor_map([x,y]) != 4 and not self.isroom([x,y]):
                    self.fill_dead_end_neighbors([x,y])

    def fill_dead_end_neighbors(self, cor):
        dir_x = [0,0,-1,1]
        dir_y = [-1,1,0,0]
        neighbors = []

        for i in range(len(dir_x)):
            neighbor_cor = [cor[0]+dir_x[i], cor[1]+dir_y[i]]
            if self.get_floor_map(neighbor_cor) != 0 and self.get_floor_map(neighbor_cor) != 4:
                neighbors.append(neighbor_cor)

        if len(neighbors) <= 1:
            map_value = 0 if not DEBUG['dead_end_highlight'] else 4
            self.set_floor_map(cor, map_value)
            for neighbor_cor in neighbors:
                self.fill_dead_end_neighbors(neighbor_cor)
        elif self.isroom(cor):
            room_id = self.get_room_map(cor)
            room = self.get_room(room_id)
            if cor in room.entrances:
                room.entrances.remove(cor)
                    
            
