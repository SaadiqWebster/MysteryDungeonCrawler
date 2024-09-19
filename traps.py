
class Trap:
    def __init__(self):
        self.cor = [0,0]
        self.id = 'Trap'
        self.effect = ''
        self.value = 0
        self.log_message = ''
        self.visible = False
        self.draw_color = (255,255,255)

    def draw(self):
        return self.cor
    
class HitTrap(Trap):
    def __init__(self):
        super().__init__()
        self.id = 'Damage'
        self.effect = 'damage'
        self.value = 5
        self.log_message = 'It dealt 5 HP of damage!'

class DebuffTrap(Trap):
    def __init__(self):
        super().__init__()
        self.id = 'Debuff'
        self.effect = 'debuff'
        self.stat = 'atk'
        self.value = -0.05
        self.log_message = 'Attack decreased by 5%!'
