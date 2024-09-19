
class Item():
    def __init__(self):
        self.cor = [0,0]
        self.id = 'Item'
        self.effect = ''
        self.value = 0
        self.throw_target = [0,0]
        self.throw_direction = 0
        self.throw_damage = 1
        self.description = 'default item with no value.'
        self.state_timer = 0 # NEED TO IMPLEMENT DELTA TIME INTO THE MOVEMENT OR THE MOVEMENT TIMER
        self.move_duration = 12
        self.draw_color = (0,255,255)
        self.draw_offset = [0,0]

    def set_throw_target(self, target_cor):
        self.state_timer = self.move_duration
        self.throw_target = target_cor
    
    def move(self):
        self.state_timer = max(0, self.state_timer-1)
        if self.state_timer > 0:
            x_distance = self.throw_target[0] - self.cor[0]
            y_distance = self.throw_target[1] - self.cor[1]
            proportion_traveled = 1 - float(self.state_timer / self.move_duration)
            self.draw_offset = [(x_distance * proportion_traveled), (y_distance * proportion_traveled)]
            return False
        else:
            self.draw_offset = [0,0]
            self.cor = self.throw_target.copy()
            return True

    def draw(self):
        return [self.cor[0] + self.draw_offset[0], self.cor[1] + self.draw_offset[1]]
    
class HealthItem(Item):
    def __init__(self):
        super().__init__()
        self.id = 'Healing Item'
        self.effect = 'heal'
        self.value = 3
        self.description = 'Heals 3 HP.'

class AttackItem(Item):
    def __init__(self):
        super().__init__()
        self.id = 'Attacking Item'
        self.effect = 'damage'
        self.value = 3
        self.description = 'Deals 3 HP of damage.'

class ThrowItem(Item):
    def __init__(self):
        super().__init__()
        self.id = 'Throwing Item'
        self.effect = 'throw'
        self.value = 3
        self.description = 'Deals 5 HP of damage. Can only throw.'

class Equipment(Item):
    def __init__(self):
        super().__init__()
        self.id = 'Equipment'
        self.effect = 'equip'
        self.stat = 'atk'
        self.value = 3
        self.description = 'Increases Attack by 3.'
        self.isequipped = False
