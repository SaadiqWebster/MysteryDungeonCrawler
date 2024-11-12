import pygame

CONTROLLER_BUTTON_MAP = {
    "Xbox Series X Controller": {
        0:0,
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:10,
        'dpad up':11,
        'dpad down':12,
        'dpad left':13,
        'dpad right':14
    },
    "Xbox 360 Controller": {
        0:0,
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:10,
        'dpad up':11,
        'dpad down':12,
        'dpad left':13,
        'dpad right':14
    },
    "DualSense Wireless Controller": {
        0:0,
        1:1,
        2:2,
        3:3,
        4:6,
        5:10,
        6:7,
        7:8,
        8:9,
        9:4,
        10:5,
        11:11,
        12:12,
        13:13,
        14:14,
        15:15
    },
    "PS4 Controller": {
        0:0,
        1:1,
        2:2,
        3:3,
        4:6,
        5:10,
        6:7,
        7:8,
        8:9,
        9:4,
        10:5,
        11:11,
        12:12,
        13:13,
        14:14,
        15:15
    },
    "Nintendo Switch Pro Controller": {
        0:1,
        1:0,
        2:3,
        3:2,
        4:6,
        5:10,
        6:7,
        7:8,
        8:9,
        9:4,
        10:5,
        11:11,
        12:12,
        13:13,
        14:14,
        15:15
    },
    "Wireless Gamepad": {
        0:1,
        1:0,
        2:3,
        3:2,
        4:4,
        5:5,
        8:7,
        9:7,
        10:8,
        11:8,
        12:10,
        13:10,
        14:'left trigger',
        15:'right trigger',
        'dpad up':11,
        'dpad down':12,
        'dpad left':13,
        'dpad right':14
    }
}

CONTROLLER_AXIS_MAP = {
    "Xbox Series X Controller": {
        0:'left stick hor',
        1:'left stick vert',
        2:'right stick hor',
        3:'right stick vert',
        4:'left trigger',
        5:'right trigger'
    },
    "Xbox 360 Controller": {
        0:'left stick hor',
        1:'left stick vert',
        2:'left trigger',
        3:'right stick hor',
        4:'right stick vert',
        5:'right trigger'
    },
    "DualSense Wireless Controller": {
        0:'left stick hor',
        1:'left stick vert',
        2:'right stick hor',
        3:'right stick vert',
        4:'left trigger',
        5:'right trigger'
    },
    "PS4 Controller": {
        0:'left stick hor',
        1:'left stick vert',
        2:'right stick hor',
        3:'right stick vert',
        4:'left trigger',
        5:'right trigger'
    },
    "Nintendo Switch Pro Controller": {
        0:'left stick hor',
        1:'left stick vert',
        2:'right stick hor',
        3:'right stick vert',
        4:'left trigger',
        5:'right trigger'
    }
}

class InputReader:
    def __init__(self):
        self.joysticks = {}
        self.buttons = {}
        self.button_pressed = []
        self.button_released = []
        self.keys = {}
        self.key_pressed = []
        self.key_released = []
        self.axis_values = {}
        self.trigger_threshold = 1.0 # between 0 and 1
        self.analog_threshold = 0.1 # between 0 and 1

    def refresh(self):
        self.button_pressed = []
        self.button_released = []
        self.key_pressed = []
        self.key_released = []

    def set_button(self, button, next_value):
        current_value = self.isbuttondown(button)
        self.buttons[button] = next_value
        if next_value == True and current_value == False:
            self.button_pressed.append(button)
        elif next_value == False and current_value == True:
            self.button_released.append(button)

    def set_key(self, key, next_value):
        current_value = self.iskeydown(key)
        self.keys[key] = next_value
        if next_value == True and current_value == False:
            self.key_pressed.append(key)
        elif next_value == False and current_value == True:
            self.key_released.append(key)
    
    def translate_button(self, button, controller_type):
        input_map = CONTROLLER_BUTTON_MAP.get(controller_type, CONTROLLER_BUTTON_MAP["Xbox Series X Controller"])
        return input_map.get(button, button)
    
    def translate_axis(self, axis, controller_type):
        input_map = CONTROLLER_AXIS_MAP.get(controller_type, CONTROLLER_BUTTON_MAP["Xbox Series X Controller"])
        return input_map.get(axis, None)

    def get_axis_value(self, axis):
        return self.axis_values[axis] if axis in self.axis_values else 0
    
    def isbuttondown(self, button):
        return self.buttons.get(button, False)
    
    def iskeydown(self, key):
        return self.keys.get(key, False)
    
    def isbuttonpressed(self, button):
        return button in self.button_pressed
    
    def iskeypressed(self, key):
        return key in self.key_pressed
    
    def isbuttonreleased(self, button):
        return button in self.button_released
    
    def iskeyreleased(self, key):
        return key in self.key_released

    def read_event(self, event):
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            self.joysticks[joy.get_instance_id()] = joy
            
        if event.type == pygame.JOYDEVICEREMOVED:
            self.joysticks.pop(event.instance_id)

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            self.key_pressed.append(key)
            self.keys[key] = True
            #print(key)

        if event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            self.key_released.append(key)
            self.keys[key] = False

        if event.type == pygame.JOYBUTTONDOWN:
            controller_type = self.joysticks[event.instance_id].get_name()
            button = self.translate_button(event.button, controller_type)
            self.set_button(button, True)
            #print(button)
            
        if event.type == pygame.JOYBUTTONUP:
            controller_type = self.joysticks[event.instance_id].get_name()
            button = self.translate_button(event.button, controller_type)
            self.set_button(button, False)

        if event.type == pygame.JOYAXISMOTION:
            #print(event.axis, event.value)
            controller_type = self.joysticks[event.instance_id].get_name()
            trigger = self.translate_axis(event.axis, controller_type)

            if trigger == 'left trigger' or trigger == 'right trigger':
                trigger_state = True if event.value >= self.trigger_threshold else False
                self.set_button(trigger, trigger_state)
                self.axis_values[trigger] = event.value
                #print(trigger, self.buttons[trigger])

            if trigger == 'left stick hor':
                trigger_state = True if event.value <= -self.analog_threshold else False
                self.set_button('left stick left', trigger_state)
                self.axis_values['left stick left'] = event.value
                trigger_state = True if event.value >= self.analog_threshold else False
                self.set_button('left stick right', trigger_state)
                self.axis_values['left stick right'] = event.value
                # if self.buttons['left analog left']: print('left analog left')
                # if self.buttons['left analog right']: print('left analog right') 

            if trigger == 'left stick vert':
                trigger_state = True if event.value <= -self.analog_threshold else False
                self.set_button('left stick up', trigger_state)
                self.axis_values['left stick up'] = event.value
                trigger_state = True if event.value >= self.analog_threshold else False
                self.set_button('left stick down', trigger_state)
                self.axis_values['left stick down'] = event.value
                # if self.buttons['left analog up']: print('left analog up')
                # if self.buttons['left analog down']: print('left analog down') 

            if trigger == 'right stick hor':
                trigger_state = True if event.value <= -self.analog_threshold else False
                self.set_button('right stick left', trigger_state)
                self.axis_values['right stick left'] = event.value
                trigger_state = True if event.value >= self.analog_threshold else False
                self.set_button('right stick right', trigger_state)
                self.axis_values['right stick right'] = event.value
                # if self.buttons['right analog left']: print('right analog left')
                # if self.buttons['right analog right']: print('right analog right') 
            
            if trigger == 'right stick vert':
                trigger_state = True if event.value <= -self.analog_threshold else False
                self.set_button('right stick up', trigger_state)
                self.axis_values['right stick up'] = event.value
                trigger_state = True if event.value >= self.analog_threshold else False
                self.set_button('right stick down', trigger_state) 
                self.axis_values['right stick down'] = event.value
                # if self.buttons['right analog up']: print('right analog up')
                # if self.buttons['right analog down']: print('right analog down') 

        if event.type == pygame.JOYHATMOTION:
            #print(event.value)
            controller_type = self.joysticks[event.instance_id].get_name()
            
            button = self.translate_button('dpad left', controller_type)
            button_state = True if event.value[0] < 0 else False
            self.set_button(button, button_state)

            button = self.translate_button('dpad right', controller_type)
            button_state = True if event.value[0] > 0 else False
            self.set_button(button, button_state)

            button = self.translate_button('dpad up', controller_type)
            button_state = True if event.value[1] > 0 else False
            self.set_button(button, button_state)

            button = self.translate_button('dpad down', controller_type)
            button_state = True if event.value[1] < 0 else False
            self.set_button(button, button_state)

