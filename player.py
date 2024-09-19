import unit as _u

class Player(_u.Unit):
    def __init__(self, spawn_cor, stats, inventory):
        super().__init__(spawn_cor)
        self.id = 'Avatar'
        self.draw_color = (0,255,0)

        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = []
        
        if stats is not None:
            self.stats = stats
        else:
            self.stats = {
                'hp':20,
                'max_hp':20,
                'sp':10,
                'max_sp':10,
                'en':100,
                'max_en':100,
                'atk':1,
                'magic':1
            }
        
        self.stat_modifiers = {
            'max_hp':0,
            'max_sp':0,
            'max_en':0,
            'atk':0,
            'magic':0
        }

        self.max_inventory_size = 12
        self.energy_duration = 5
        self.energy_timer = self.energy_duration

    def update_state(self):
        prev_state = self.state
        end_turn = super().update_state()
        if end_turn and prev_state == 'move':
            self.consume_energy()
        return end_turn

    def consume_energy(self):
        if self.stats['en'] > 0:
            self.stats['hp'] = min(self.stats['hp']+1, self.stats['max_hp'])
            self.stats['sp'] = min(self.stats['sp']+1, self.stats['max_sp'])
            self.energy_timer -= 1
        if self.energy_timer <= 0:
            self.stats['en'] = max(0, self.stats['en']-1)
            self.energy_timer = self.energy_duration

    def add_to_inventory(self, item):
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(item)
            return False
        else:
            return True
        
    def is_inventory_full(self):
        return len(self.inventory) >= self.max_inventory_size
    
    def equip_item(self, equipment):
        equipment.isequipped = True
        self.stats[equipment.stat] += equipment.value
        if equipment.stat == 'max_hp':
            self.stats['hp'] += equipment.value
        if equipment.stat == 'max_sp':
            self.stats['sp'] += equipment.value

    def unequip_item(self, equipment):
        equipment.isequipped = False
        self.stats[equipment.stat] -= equipment.value
        if equipment.stat == 'max_hp' and self.stats['hp'] > self.stats['max_hp']:
            self.stats['hp'] == self.stats['max_hp']
        if equipment.stat == 'max_sp' and self.stats['sp'] > self.stats['max_sp']:
            self.stats['sp'] == self.stats['max_sp']

