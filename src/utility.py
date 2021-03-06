def coordinate(i, j, size):
    x = i * size + size // 2
    y = j * size + size // 2
    return x, y

def coordinate_t(x, y, size):
    i = x // size
    j = y // size
    return i, j

def check_condition(cd,map=None):
    condition_satisfied = 0
    for conj_item in cd:
        item_satisfied = 1
        tr_items = conj_item[0]
        fl_items = conj_item[1]
        for tag in tr_items:
            if not (tag in map.global_vars.flags):
                item_satisfied = 0
                break
            elif map.global_vars.flags[tag] == False:
                item_satisfied = 0
                break
        if item_satisfied == 0:
            continue
        for tag in fl_items:
            if not (tag in map.global_vars.flags):
                pass
            elif map.global_vars.flags[tag] == True:
                item_satisfied = 0
                break
        if item_satisfied == 1:
            condition_satisfied = 1
            break
    if condition_satisfied == 1:
        return True
    return False

def is_weapon(s):
    if s in ["Sword","Lance","Bow","Axe","Light","Dark","Wind","Fire","Thunder"]:
        return True
    return False

def calc_dist(A,B):
    return abs(A[0]-B[0])+abs(A[1]-B[1])

def get_weapon_rank(exp):
    if exp <= 0:
        return '--'
    elif exp < 30:
        return 'E'
    elif exp < 80:
        return 'D'
    elif exp < 150:
        return 'C'
    elif exp < 230:
        return 'B'
    elif exp < 320:
        return 'A'
    else:
        return 'S'


state = ['none', 'valid_select', 'invalid_select', 'ally_select', 'enemy_select', 'menu_display', 'info']

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_PINK = (255, 182, 193)
STEEL_BLUE = (70, 130, 180)
CRIMSON = (220, 20, 60)
VIOLET = (238, 130, 238)
SLATEBLUE = (106, 90, 205)
CYAN = (0, 255, 255)
AUQAMARIN = (127, 255, 170)
LIME = (0, 255, 0)
YELLOW = (255, 255, 0)
OLIVE = (128, 128, 0)
CORNISLK = (255, 248, 220)
ORANGE = (255, 165, 0)
CORAL = (255, 127, 80)
SKY_BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
MAROON = (128, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)



