import random
import unit as _u

class Enemy(_u.Unit):
    def __init__(self):
        super().__init__([0,0])
        self.id = 'Enemy'
        self.draw_color = (255,0,0)
        self.image.fill(self.draw_color)
        self.stats = {
            'hp':3,
            'max_hp':3,
            'atk':1,
            'mgc':1
        }

    def decide_action(self, floor, unit_map, units, player_id):
        if self.state == 'idle':
            player_cor = units[player_id].cor
            distance_map = floor.generate_distance_map(player_cor)
            dir_x = [0,1,1,1,0,-1,-1,-1]
            dir_y = [-1,-1,0,1,1,1,0,-1]
            valid_next_coordinates = []
            min_distance_coordinates = []
            move_min_distance = float('inf')
            attack_direction = -1

            for i in range(len(dir_x)):
                adjacent_cor = [self.cor[0]+dir_x[i], self.cor[1]+dir_y[i]]
                adjacent_distance = floor.get_map_value(distance_map, adjacent_cor)
                # vv this makes it so that the enemy cannot enter or exit a pathway diagonally
                block_direction = i % 2 != 0 and (not floor.isroom(self.cor) or not floor.isroom(adjacent_cor))
                if not block_direction:
                    valid_next_coordinates.append(adjacent_cor)

                    if adjacent_distance == 0:
                        attack_direction = i
                    
                    elif adjacent_distance > 0 and floor.get_map_value(unit_map, adjacent_cor) == -1:
                        if adjacent_distance == move_min_distance:
                            min_distance_coordinates.append(adjacent_cor)
                        elif adjacent_distance < move_min_distance:
                            move_min_distance = adjacent_distance
                            min_distance_coordinates = []
                            min_distance_coordinates.append(adjacent_cor)

            if attack_direction != -1:
                self.direction = attack_direction
                self.attack()
                return True
            elif min_distance_coordinates:
                next_cor = random.choice(min_distance_coordinates)
                self.set_direction(next_cor)
                self.move(next_cor)
                return True
            elif valid_next_coordinates: # this is here in case you want to have the enemy wander randomly. please refactor as necessary to be able to execute this
                next_cor = random.choice(valid_next_coordinates)
                self.set_direction(next_cor)
                self.move(next_cor)
                return True
            else:
                return False
