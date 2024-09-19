import pygame, random
import floorgenerator as _fg
import menu as _m, textlog as _l
import player as _p, enemies as _e, items as _i, traps as _t

class FloorManager:
    def __init__(self, dungeon_name):
        self.dungeon_name = dungeon_name
        self.floor = _fg.FloorGenerator(1,1)
        self.floor_number = 0
        self.stairs_cor = [0,0]
        self.next_object_id = 0
        self.player_id = -1
        self.units = {}
        self.items = {}
        self.traps = {}
        self.unit_map = self.floor.generate_empty_map(-1)
        self.item_map = self.floor.generate_empty_map(-1)
        self.trap_map = self.floor.generate_empty_map(-1)
        self.visibility_map = self.floor.generate_empty_map(0)
        self.turn_order = []
        self.moving_units = []
        self.attacked_units = []
        self.thrown_items = []
        self.current_turn = 0
        self.active_menus = []
        self.text_log = _l.TextLog()

    def get_unit(self, unit_id):
        return self.units.get(unit_id, None)

    def get_player(self):
        if self.player_id == -1:
            return None
        return self.get_unit(self.player_id)
    
    def get_item(self, item_id):
        return self.items.get(item_id, None)
    
    def get_trap(self, trap_id):
        return self.traps.get(trap_id, None)
    
    def get_unit_map(self, cor):
        return self.floor.get_map_value(self.unit_map, cor)
    
    def get_item_map(self, cor):
        return self.floor.get_map_value(self.item_map, cor)

    def get_trap_map(self, cor):
        return self.floor.get_map_value(self.trap_map, cor)
    
    def get_visibility_map(self, cor):
        return self.floor.get_map_value(self.visibility_map, cor)
    
    def get_current_turn(self):
        return self.turn_order[self.current_turn]
    
    def get_active_menu(self):
        if self.active_menus:
            return self.active_menus[-1]
    
    def set_floor_properties(self, properties):
        self.floor.set_floor_properties(properties)

    def set_unit_map(self, cor, value):
        return self.floor.set_map_value(self.unit_map, cor, value)
    
    def set_item_map(self, cor, value):
        return self.floor.set_map_value(self.item_map, cor, value)

    def set_trap_map(self, cor, value):
        return self.floor.set_map_value(self.trap_map, cor, value)
    
    def set_visibility_map(self, cor, value):
        return self.floor.set_map_value(self.visibility_map, cor, value)

    def isplayerturn(self):
        return False if len(self.turn_order) < 1 else self.get_current_turn() == self.player_id
    
    def iswalkabletile(self, cor):
        if self.floor.get_floor_map(cor) == 0:
            return False
        
        if self.get_unit_map(cor) != -1:
            return False

        return True

    def isemptytile(self, cor):
        if not self.iswalkabletile(cor):
            return False

        if self.stairs_cor == cor:
            return False
        
        if self.get_item_map(cor) != -1:
            return False
        
        if self.get_trap_map(cor) != -1:
            return False
        
        return True
    
    def isblocked(self, direction, current_cor, adjacent_cor):
        return direction % 2 != 0 and (not self.floor.isroom(current_cor) or not self.floor.isroom(adjacent_cor))
    
    def find_empty_tile(self, room_id):
        room = self.floor.get_room(room_id)
        empty_tiles = []

        for x in range(room.width):
            for y in range(room.height):
                room_cor = [room.cor[0]+x, room.cor[1]+y]
                if self.isemptytile(room_cor) and room_cor not in room.entrances:
                    empty_tiles.append(room_cor)

        if len(empty_tiles) > 0:
            return random.choice(empty_tiles)
        
    def place_unit(self, unit_id):
        unit = self.get_unit(unit_id)
        if self.get_unit_map(unit.prev_cor) == unit_id:
            self.set_unit_map(unit.prev_cor, -1)
        self.set_unit_map(unit.cor, unit_id)

    def hit_unit(self, unit_id, damage):
        unit = self.get_unit(unit_id)
        unit.hit(damage)
        self.attacked_units.append(unit_id)
    
    def check_visibility(self, unit):
            visibility_radius = 1

            if self.floor.isroom(unit.cor) and self.get_visibility_map(unit.cor) <= 0:
                room = self.floor.get_room(self.floor.get_room_map(unit.cor))
                self.make_visible([room.cor[0]-1, room.cor[1]-1], room.width+2, room.height+2)

            self.make_visible((unit.cor[0]-visibility_radius, unit.cor[1]-visibility_radius), (visibility_radius*2)+1, (visibility_radius*2)+1)

    def make_visible(self, start_cor, width, height):
        for i in range(width):
            for j in range(height):
                visible_cor = [start_cor[0]+i, start_cor[1]+j]
                self.set_visibility_map(visible_cor, 1)

    def log_message(self, message):
        if message != '':
            self.text_log.add(message)

    def open_menu(self, menu):
        self.active_menus.append(menu)

    def close_active_menu(self):
        self.active_menus.pop(-1)

    def close_all_menus(self):
        self.active_menus.clear()

    def generate_test_floor(self):
        self.floor.generate_floor_test()
        self.spawn_player()

    def generate_new_floor(self):
        player = self.get_player()
        player_stats = None if player is None else player.stats
        player_inventory = None if player is None else player.inventory
    
        self.units = {}
        self.items = {}
        self.traps = {}
        self.unit_map = self.floor.generate_empty_map(-1)
        self.item_map = self.floor.generate_empty_map(-1)
        self.trap_map = self.floor.generate_empty_map(-1)
        self.visibility_map = self.floor.generate_empty_map(0)
        self.turn_order = []
        self.moving_units = []
        self.attacked_units = []
        self.thrown_items = []
        self.text_log.clear()
        self.current_turn = 0

        self.floor.generate_floor()
        self.floor_number += 1
        

        self.spawn_stairs()
        self.spawn_player(player_stats, player_inventory)
        self.spawn_enemy(_e.Enemy(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_enemy(_e.Enemy(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_item(_i.HealthItem(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_item(_i.AttackItem(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_item(_i.ThrowItem(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_item(_i.Equipment(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_trap(_t.HitTrap(), self.find_empty_tile(self.floor.get_random_room()))
        self.spawn_trap(_t.DebuffTrap(), self.find_empty_tile(self.floor.get_random_room()))

    def spawn_stairs(self):
        self.stairs_cor = [0,0]
        room_id = self.floor.get_random_room()
        if room_id != -1:
            self.stairs_cor = self.find_empty_tile(room_id)

    def spawn_player(self, player_stats=None, player_inventory=None):
        room_id = self.floor.get_random_room()

        if len(self.floor.rooms) > 1:
            stairs_room_id = self.floor.get_room_map(self.stairs_cor)
            while room_id == stairs_room_id:
                room_id = self.floor.get_random_room()

        spawn_cor = self.find_empty_tile(room_id)
        player = _p.Player(spawn_cor, player_stats, player_inventory)
        self.units[self.next_object_id] = player
        self.player_id = self.next_object_id
        self.place_unit(self.next_object_id)
        self.turn_order.append(self.next_object_id)
        self.check_visibility(player)
        self.next_object_id += 1
        return self.next_object_id - 1

    def spawn_enemy(self, enemy, spawn_cor):
        if spawn_cor:
            enemy.cor = spawn_cor.copy()
            enemy.prev_cor = spawn_cor.copy()
            self.units[self.next_object_id] = enemy
            self.place_unit(self.next_object_id)
            self.turn_order.append(self.next_object_id)
            self.next_object_id += 1
            return self.next_object_id - 1
        else:
            return -1
    
    def spawn_trap(self, trap, spawn_cor):
        if spawn_cor:
            trap.cor = spawn_cor
            self.traps[self.next_object_id] = trap
            self.set_trap_map(spawn_cor, self.next_object_id)
            self.next_object_id += 1
            return self.next_object_id - 1
        else:
            return -1

    def spawn_item(self, item, spawn_cor):
        if spawn_cor:
            item.cor = spawn_cor
            self.items[self.next_object_id] = item
            self.set_item_map(spawn_cor, self.next_object_id)
            self.next_object_id += 1
            return self.next_object_id - 1
        else:
            return -1

    def pickup_item(self, cor):
        item_id = self.get_item_map(cor)
        if item_id != -1:
            player = self.get_player()
            item = self.get_item(item_id)
            isinventoryfull = player.add_to_inventory(item)
            if not isinventoryfull:
                self.set_item_map(cor, -1)
                self.items.pop(item_id)
                self.log_message(player.id + ' picked up ' + item.id + '.')

    def drop_item(self, item, cor):
        dir_x = [0,0,1,1,1,0,-1,-1,-1]
        dir_y = [0,-1,-1,0,1,1,1,0,-1]
        player = self.get_player()

        for i in range(len(dir_x)):
            adjacent_cor = [cor[0]+dir_x[i], cor[1]+dir_y[i]]
            if self.floor.get_floor_map(adjacent_cor) == 1 and self.get_item_map(adjacent_cor) == -1:
                self.spawn_item(item, adjacent_cor)
                self.log_message(player.id + ' dropped ' + item.id + '.')
                return True
        return False

    def throw_item(self, item, direction):
        prev_map_value =  self.get_item_map(item.cor)
        item_id = self.spawn_item(item, item.cor)
        self.set_item_map(item.cor, prev_map_value)
        item.throw_direction = direction
        self.thrown_items.append(item_id)
        self.check_item_collision(item_id)

    def check_item_collision(self, item_id):
        dir_x = [0,1,1,1,0,-1,-1,-1]
        dir_y = [-1,-1,0,1,1,1,0,-1]
        item = self.get_item(item_id)

        next_cor = [item.cor[0]+dir_x[item.throw_direction], item.cor[1]+dir_y[item.throw_direction]]
        unit_map_value = self.get_unit_map(next_cor)
        floor_map_value = self.floor.get_floor_map(next_cor)

        if floor_map_value == 0 or self.isblocked(item.throw_direction, item.cor, next_cor): # if item collides with a wall
            self.items.pop(item_id)
            self.thrown_items.remove(item_id)
            self.drop_item(item, item.cor)
            self.change_turn()
        elif unit_map_value != -1: # if item collides with a unit
            self.items.pop(item_id)
            self.thrown_items.remove(item_id)
            self.use_item(item, unit_map_value)
            self.change_turn()
        else: # no collision, move forward one cell
            item.set_throw_target(next_cor)

    def use_item(self, item, unit_id):
        unit = self.get_unit(unit_id)
        log_message = ''

        if item.effect == 'heal':
            healing_amount = min(unit.stats['hp'] + item.value, unit.stats['max_hp']) - unit.stats['hp']
            unit.stats['hp'] += healing_amount
            log_message = str(unit.id) + ' used the ' + str(item.id) + ' to heal ' + str(healing_amount) + ' HP.'

        if item.effect == 'damage' or item.effect == 'throw':
            self.hit_unit(unit_id, item.value)
            log_message = str(unit.id) + ' used the ' + str(item.id) + ' and took ' + str(item.value) + ' damage.'

        if item.effect == 'equip':
            self.hit_unit(unit_id, item.value)
            log_message = str(unit.id) + ' threw the ' + str(item.id) + ' and took ' + str(item.value) + ' damage.'
            self.drop_item(item, unit.cor)

        self.log_message(log_message)
    
    def trigger_trap(self, unit_id):
        unit = self.get_unit(unit_id)
        trap_id = self.get_trap_map(unit.cor)
        if trap_id != -1:
            trap = self.get_trap(trap_id)
            trap.visible = True
            self.log_message(unit.id + ' triggered the ' + trap.id + ' Trap!')

            if trap.effect == 'damage':
                self.hit_unit(unit_id, trap.value)

            if trap.effect == 'debuff':
                unit.set_stat_modifier(trap.stat, trap.value)

            self.log_message(trap.log_message)

    def read_input(self, input):
        player = self.get_player()
        active_menu = self.get_active_menu()

        if self.active_menus:
            if input.iskeypressed('up') or input.isbuttonpressed('left stick up') or input.isbuttonpressed(11):
                active_menu.cursor_forward()
            
            if input.iskeypressed('down') or input.isbuttonpressed('left stick down') or input.isbuttonpressed(12):
                active_menu.cursor_backward()

            if input.iskeypressed('x') or input.isbuttonpressed(1):
                self.close_active_menu()

            if input.iskeypressed('z') or input.isbuttonpressed(0):
                self.select_menu_option()
        
        elif self.isplayerturn() and player.state == 'idle' and not self.moving_units and not self.thrown_items:
            if (input.iskeydown('left ctrl') and input.iskeydown('left alt')) or (input.isbuttondown('left trigger') and input.isbuttondown(4)):
                self.change_turn()
                return

            if input.iskeypressed('z') or input.isbuttonpressed(3):
                options = ['Attack','Skills','Items','Wait','Exit']
                if player.cor == self.stairs_cor:
                    options.insert(-1, 'Proceed')
                self.open_menu(_m.Menu((2, 40), options))
            
            if (input.iskeypressed('space') or input.isbuttonpressed(0)) and player.state == 'idle':
                player.attack()
                self.close_all_menus()

            input_direction = [0, 0]
            
            if input.iskeydown('up') or input.isbuttondown('left stick up') or input.isbuttondown(11):
                input_direction[1] -= 1
            
            if input.iskeydown('down')  or input.isbuttondown('left stick down') or input.isbuttondown(12):
                input_direction[1] += 1
            
            if input.iskeydown('left')  or input.isbuttondown('left stick left') or input.isbuttondown(13):
                input_direction[0] -= 1
            
            if input.iskeydown('right')  or input.isbuttondown('left stick right') or input.isbuttondown(14):
                input_direction[0] += 1
            

            if input_direction != [0,0] and player.state == 'idle' and not self.active_menus and not self.moving_units:
                next_cor = [input_direction[0] + player.cor[0], input_direction[1] + player.cor[1]]
                player.set_direction(next_cor)
                
                # this makes it so that the player cannot enter or exit a pathway diagonally
                block_direction = self.isblocked(player.direction, player.cor, next_cor)
                
                if input.iskeydown('left ctrl')  or input.isbuttondown('left trigger'):
                    block_direction = True
                elif (input.iskeydown('left alt')  or input.isbuttondown(4)) and 0 in input_direction:
                    block_direction = True

                if self.iswalkabletile(next_cor) and not block_direction:
                    player.move(next_cor)
                    self.place_unit(self.player_id)
                    self.moving_units.append(self.player_id)
                    self.change_turn()
    
    def select_menu_option(self): 
        player = self.get_player()
        active_menu = self.get_active_menu()

        if active_menu.id == 'inventory' and len(active_menu.options) > 0:
            item = active_menu.get_selected()
            menu_options = []
            
            if item.effect == 'equip' and not item.isequipped:
                menu_options.append('Equip')
            
            elif item.effect == 'equip' and item.isequipped:
                menu_options.append('Unequip')
            
            elif item.effect != 'throw':
                menu_options.append('Use')
            
            menu_options.append('Throw')
            
            menu_options.append('Drop')
            
            if self.get_item_map(player.cor) != -1:
                menu_options.append('Swap')
            
            menu_options.append('Back')
            
            if menu_options:
                self.open_menu(_m.Menu((104, 30), menu_options))

        elif active_menu.id == 'menu':
            option = active_menu.get_option()
            
            if option == 'Exit' or option == 'Back' or option == 'Cancel':
                self.close_active_menu()

            if option == 'Wait':
                self.close_active_menu()
                player.consume_energy()
                self.change_turn()

            if option == 'Proceed':
                self.close_active_menu()
                self.generate_new_floor()
            
            if option == 'Attack':
                player.attack()
                self.close_all_menus()
            
            if option == 'Items':
                player_inv = player.inventory
                self.open_menu(_m.InventoryMenu((2, 30), player_inv))

            if option == 'Use':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                self.use_item(inventory_menu.pop_selected(), self.player_id)
                self.active_menus.clear()
                self.change_turn()

            if option == 'Equip':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                equipment = inventory_menu.get_selected()
                player.equip_item(equipment)

            if option == 'Unequip':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                equipment = inventory_menu.get_selected()
                player.unequip_item(equipment)
            
            if option == 'Throw':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                selected_item = inventory_menu.pop_selected()
                if selected_item.effect == 'equip' and selected_item.isequipped:
                    player.unequip_item(selected_item)
                selected_item.cor = player.cor.copy()
                self.throw_item(selected_item, player.direction)
                self.close_all_menus()

            if option == 'Drop':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                selected_item = inventory_menu.pop_selected()
                if selected_item.effect == 'equip' and selected_item.isequipped:
                    player.unequip_item(selected_item)
                self.drop_item(selected_item, player.cor)
                self.close_all_menus()
                self.change_turn()

            if option == 'Swap':
                self.close_active_menu()
                inventory_menu = self.get_active_menu()
                selected_item = inventory_menu.pop_selected()
                if selected_item.effect == 'equip' and selected_item.isequipped:
                    player.unequip_item(selected_item)
                self.pickup_item(player.cor)
                self.drop_item(selected_item, player.cor)
                self.close_all_menus()
                self.change_turn()

    def update_objects(self):
        for i in range(len(self.thrown_items)):
            item_id = self.thrown_items[i]
            item = self.get_item(item_id)
            if item.move():
                self.check_item_collision(item_id)

        for unit_id in self.units:
            unit = self.get_unit(unit_id)
            prev_state = unit.state
            end_turn = False
            if not (unit.state == 'attack_forward' and (self.active_menus or self.moving_units or self.attacked_units or self.thrown_items)) and not (unit.state == 'move' and (self.active_menus or self.attacked_units or self.thrown_items)):
                end_turn = unit.update_state()
            if end_turn:
                if prev_state == 'attack_forward':
                    dir_x = [0,1,1,1,0,-1,-1,-1]
                    dir_y = [-1,-1,0,1,1,1,0,-1]
                    target_cor = [unit.cor[0]+dir_x[unit.direction], unit.cor[1]+dir_y[unit.direction]]
                    target_id = self.get_unit_map(target_cor)
                    if target_id > -1 and not self.isblocked(unit.direction, unit.cor, target_cor):
                        target = self.get_unit(target_id)
                        damage = unit.get_modified_stat('atk')
                        self.hit_unit(target_id, damage)
                        target.set_direction(unit.cor)
                        self.log_message(unit.id + ' dealt ' + str(damage) + ' damage to ' + target.id + '.')

                if prev_state == 'attack_backward':
                    self.change_turn()

                if prev_state == 'hit':
                    if unit.stats['hp'] <= 0:
                        unit.kill()
                        self.log_message(unit.id + ' was defeated!')
                    else:
                        self.attacked_units.remove(unit_id)

                if prev_state == 'kill':
                    self.attacked_units.remove(unit_id)
                    if unit_id == self.player_id:
                        self.player_id = -1
                    self.set_unit_map(unit.cor, -1)
                    self.turn_order.remove(unit_id)
                    self.units.pop(unit_id)
                    self.current_turn = self.current_turn % len(self.turn_order) # if the unit killed was the very last one in the turn order it caused a defect. not sure if this line is the best solution. might cause problems later?
                    break

                if prev_state == 'move':
                    self.moving_units.remove(unit_id)
                    if unit_id == self.player_id:
                        player = self.get_player()
                        self.check_visibility(player)
                        self.pickup_item(player.cor)
                        self.trigger_trap(unit_id)
                        if player.cor == self.stairs_cor:
                            self.open_menu(_m.Menu((2, 40), ['Proceed','Cancel']))

            if self.get_player() is not None and unit_id == self.get_current_turn() and unit.state == 'idle' and not self.thrown_items:
                self.decide_action(unit_id)
                
            unit.update_animation()

    def decide_action(self, unit_id):
        if unit_id != self.player_id:
            unit = self.get_unit(unit_id)
            decision_made = unit.decide_action(self.floor, self.unit_map, self.units, self.player_id)
            if not decision_made:
                self.change_turn()
            elif unit.state == 'move':
                    self.place_unit(unit_id)
                    self.moving_units.append(unit_id)
                    self.change_turn()

    def change_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        next_unit_id = self.get_current_turn()
        next_unit = self.get_unit(next_unit_id)
        if next_unit.state == 'idle':
            self.decide_action(next_unit_id)
