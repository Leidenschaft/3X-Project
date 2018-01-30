import cocos
from cocos.sprite import Sprite
from cocos.director import director
from cocos.actions import MoveTo, Delay, sequence, CallFunc
from global_vars import Main as Global
from data_loader import Main as Data
from terrain_container import Main as Terrain_Container
from person_container import Main as Person_Container
from person import Person
import map_controller
from utility import *
import pyglet
from person_info import Info
from battle_scene import Battlescene
from menu import Optionmenu

def test_print(self):
    print('hello')


class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        pyglet.resource.path = ['../img']
        pyglet.resource.reindex()
        self.size = 80
        self.select = None #当前选中的角色
        self.state = 'none' # 0：默认 什么都没选中； 1：选中一个友军 左击移动右击取消 2：选中一个敌军 任何操作都取消 3： 正在显示某个人的信息 任何操作返回
        self.origin_color = WHITE
        data = Data()
        global_vars = Global(data)
        terrain_container_test = Terrain_Container(data.terrain_map, global_vars.terrainBank)
        person_container_test = Person_Container(data.map_armylist, global_vars.personBank)
        map1 = map_controller.Main(terrain_container_test, person_container_test, global_vars)
        self.w = terrain_container_test.M
        self.h = terrain_container_test.N

        super(Arena, self).__init__(r=0,g=0,b=0,a=255,width=self.w*self.size,height=self.h*self.size)
        self.info = Info()

        self.tiles = []
        for x in range(self.w):
            tl_x = []
            for y in range(self.h):
                tile = Tile(pos=coordinate(x, y, self.size), size=self.size)
                self.add(tile)
                tl_x.append(tile)
            self.tiles.append(tl_x)

        self.repaint(map1)
        self.map = map1
        self.text = cocos.text.RichLabel('ROUND 1' ,
                                     font_name='times new roman',
                                     font_size=36,
                                     position=(0, 420),
                                    color = (127, 255, 170, 255))
        self.add(self.text)
        self.end_turn = Sprite(image='ring.png', position=(560,200), color=MAROON, scale=0.8)

        self.add(self.end_turn)
        self.add(cocos.text.RichLabel(text='END', position=(520, 190), font_size=30))

        self.highlight = set()
        self.mouse_select = None
        self.add(self.info)
        self.mapstate = self.map.send_mapstate()
        self.next_round()

    def move(self, person, i, j):
        obj = self.person[person.pid]
        self.map2per[(i, j)] = person
        mov = MoveTo(coordinate(i, j, self.size), 2)
        obj.do(Delay(0.5)+ mov  + CallFunc(self.mark_role) + CallFunc(self.clear_map)+ CallFunc(self.take_turn))

    def sequential_move(self, person, dst): #传入前先修改位置
        map = self.map
        i, j = dst[-1]
        id = person.pid
        map.person_container.position[id] = i, j
        map.person_container.movable[id] = False
        self.is_event_handler = False
        obj = self.person[person.pid]
        self.map2per[dst[-1]] = person
        action = Delay(0.1)
        for x,y in dst:
            action = action + MoveTo(coordinate(x, y, self.size), 0.5)
        obj.do(action + CallFunc(self.mark_role) + CallFunc(self.clear_map)
               + CallFunc(self.take_turn))


    def take_turn(self): #according to the controller, take turn of next charactor
        map = self.map
        if map.controller == 0:
            map.player_turn(self)
        else:
            map.ai_turn(self)

    def mark_role(self):
        if self.select is not None: #选中的是自己角色
            id = self.select.pid
            self.person[id].color = OLIVE
            self.mapstate = self.map.send_mapstate()

    def next_round(self):
        self.map.turn += 1
        self.text.element.text = 'ROUND '+str(self.map.turn)
        self.map.controller = 0
        self.mapstate = self.map.send_mapstate()
        for p in self.person:
            if self.map.person_container.controller[p] == 1:
                self.person[p].color = ORANGE
            else:
                self.person[p].color = SKY_BLUE

        if self.map.turn > 6 :
            director.pop()
        else:
            self.take_turn()

    def repaint(self, map_controller):
        position = map_controller.person_container.position
        controller = map_controller.person_container.controller
        people = map_controller.person_container.people
        self.person = {}
        self.map2per = {}
        for p in people:
            id = p.pid
            (x, y) = position[id]
            if controller[id] == 1 :
                color = ORANGE
            else:
                color = SKY_BLUE
            self.map2per[(x, y)] = p
            self.person[id] = Ally(pos=coordinate(x, y, self.size), color=color, size=self.size)
            self.add(self.person[id])


    def on_mouse_motion(self, x, y, buttons, modifiers):
        if self.state == 'menu_display':
            return
        i, j = coordinate_t(x, y, self.size)
        if (x-560)**2 + (y-200)**2 < 80**2:
            self.end_turn.color = GOLD
        else:
            self.end_turn.color = MAROON
        if i in range(0, self.w) and j in range(0, self.h):
            if self.mouse_select is not None: #之前有 则先修改先前的颜色
                i0, j0 = self.mouse_select
                if (i0, j0) in self.highlight:
                    if self.state == 'valid_select' :
                        self.tiles[i0][j0].color = STEEL_BLUE
                    elif self.state == 'enemy_select':
                        self.tiles[i0][j0].color = CORAL
                else:
                    self.tiles[i0][j0].color = WHITE
            if (i, j) in self.highlight:
                self.tiles[i][j].color = VIOLET
            else:
                self.tiles[i][j].color = LIGHT_PINK
            self.mouse_select = i, j

        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.is_event_handler:
            i, j = coordinate_t(x, y, self.size)
            map = self.map
            valid, invalid, ally, enemy = self.mapstate
            if self.state == 'info': #显示信息界面 任何操作都返回
                self.info.info_clear()
                self.clear_map()
            elif self.state == 'invalid_select' or self.state == 'enemy_select' \
                    or self.state == 'ally_select': #选中一个敌军或友军 任何操作都返回
                self.clear_map()
            else: #其他情况 进行判断左击或右击
                if buttons == 1:
                    if self.end_turn.color == list(GOLD): #判断是否结束回合
                        map.controller = 1
                        map.reset_state(0)
                        self.is_event_handler = False
                        self.clear_map()
                        self.take_turn()
                        return
                    if self.state == 'none': #谁都没被选中，判断点击位置是否是人，标准状态
                        # 现在只有一个人
                        if (i, j) in self.map2per.keys(): #选中的是玩家角色
                            select = self.map2per[(i, j)] # type:Person
                            pid = select.pid
                            if pid in valid.keys(): #选中的是可移动角色
                                # 显示移动范围
                                self.select = select
                                self.state = 'valid_select'
                                color = STEEL_BLUE
                                area = valid[pid]

                            elif pid in invalid.keys(): #选中的是已行动的本方角色
                                self.state = 'invalid_select'

                            elif pid in enemy.keys():
                                self.state = 'enemy_select'
                                color = CORAL
                                area = enemy[pid]
                            elif pid in ally.keys():
                                self.state = 'ally_select'
                            else:
                                # 已经移动或其他原因
                                pass
                            self.highlighting(area, color)
                        else:
                            # 显示其他信息，不处理
                            return

                    elif self.state == 'valid_select':  # 已经选中一个可移动的人
                        id = self.select.pid

                        if (i, j) in self.highlight:

                            dst = valid[id][(i, j)][1]
                            self.state = 'menu_display'
                            self.menu = Optionmenu(self.select, dst)
                            self.add(self.menu)
                            '''
                            # self.move(self.select, i, j)
                            self.sequential_move(self.select, dst)
                            # 显示移动确定选项
                            
                            
                            self.sequential_move(self.select, dst)
                            '''
                        else:
                            self.clear_map()

                elif  buttons == 4: #右击
                    if self.state == 'valid_select': # 已经选中一个人，改操作为取消
                        self.clear_map()
                    elif self.state == 'none': # 谁都没选中 显示选中者的信息
                        if (i, j) in self.map2per.keys(): #选中的是玩家角色
                            select = self.map2per[(i, j)] # type:Person
                            self.state = 'info' # 选中信息的界面状态
                            self.info.info_display(select)
                        else:
                            pass # 显示地图信息？
                    else:
                        pass
                    pass
            '''
            

            if self.end_turn.color == list(GOLD):
                map.controller = 1
                map.reset_state(0)
                self.is_event_handler = False
                self.next_round()
            else:
                if i in range(0, self.w) and j in range(0, self.h):
                    if map.person_container.movable['1']:
                        map.person_container.position['1'] = i, j
                        map.person_container.movable['1'] = False
                        self.move('1', i, j)

            '''

    def confirm(self, person, dst):
        self.sequential_move(person, dst)
        pass

    def highlighting(self, area, color):
        for x0, y0 in area:
            self.tiles[x0][y0].color = color
        self.highlight = area

    def exit(self, scene):
        director.push(scene)

    def clear_map(self):
        self.state = 'none'
        if self.highlight is not None:
            for i, j in self.highlight:
                self.tiles[i][j].color = WHITE
        self.highlight = set()
        self.select = None


class Tile(Sprite):
    def __init__(self, size=50,pos=None):
        path = 'ring.png'
        super(Tile, self).__init__(image=path)
        self.scale = size/self.height
        self.color = (255, 255, 255)
        self.position = pos

class Ally(Sprite):
    select = False
    def __init__(self, size=50,pos=None, color=(135, 206, 235)):
        path = 'ring.png'
        super(Ally, self).__init__(image=path)
        self.scale = size/self.height * 0.8
        self.color = color
        self.position = pos


class Check_state(Delay):
    def start(self):
        arena = self.target.parent     #type:Arena
        map = arena.map
        map.turn += 1
        if map.turn <= 5:
            if map.check_states():
                self.target.do(sequence(MoveTo(coordinate(map.i, map.j, arena.size), 2), Check_state(1)))
            else:
                self.target.do(Check_state(1))
        else:
            print('gg')



    def stop(self):
        arena = self.target     #type:Arena
        arena.is_event_handler = True



if __name__ == '__main__':
    director.init(caption='3X-Project')
    director.run(cocos.scene.Scene(Arena()))
