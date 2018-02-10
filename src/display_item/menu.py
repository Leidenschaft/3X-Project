# coding=utf-8
'''
@author: Antastsy
@time: 2018/1/30 20:10
'''
from cocos.menu import Menu, MenuItem, zoom_in, zoom_out
from display_item.info import Info
from cocos.director import director
from cocos.layer import ColorLayer
class Menulayer(ColorLayer):
    def __init__(self):
        w, h = director.get_window_size()
        super().__init__(0,0,0,200,w//4, h)
        self.position = w - w //4, 0


class Ordermenu(Menu):
    is_event_handler = True

    def __init__(self, arena):
        super(Ordermenu, self).__init__(title='Order')
        l = []
        l.append(MenuItem('Move', self.move))
        l.append(MenuItem('Attack', self.attack))

        map = arena.map
        pid = arena.selected
        position = arena.target
        self.sup_dict = map.can_support(pid, position)
        if len(self.sup_dict) > 0:
            l.append(MenuItem('Support', self.support))

        l.append(MenuItem('Cancel', self.cancel))
        self.create_menu(l, zoom_in(), zoom_out())
        self.position = - director.get_window_size()[0] * 3 // 8, 0
        self.arena = arena

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons == 1:
            super().on_mouse_release(x, y, buttons, modifiers)

    def move(self):
        self.arena.move()
        self.parent.remove(self)
        del self

    def cancel(self):
        self.arena.cancel()
        self.parent.remove(self)
        del self

    def attack(self):
        self.arena.attack()
        self.parent.remove(self)
        del self

    def support(self):
        self.arena.support(self.sup_dict)
        self.parent.remove(self)
        del self

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == 4:
            self.cancel()

class Weaponmenu(Menu):
    is_event_handler = True

    def __init__(self, items, map, arena):
        super(Weaponmenu, self).__init__(title='Weapons')
        w, h = director.get_window_size()
        self.w, self.h = w, h
        l = []
        for item in items:
            if map.attackable(item.itemtype.weapontype):
                l.append(MenuItem(item.itemtype.name, self.iteminfo, item))
        l.append(MenuItem('Cancel', self.cancel))
        self.create_menu(l, zoom_in(), zoom_out())
        self.info = None
        # self.position = (-w // 4, 0)
        self.position = - director.get_window_size()[0] * 3 // 8, 0
        self.arena = arena

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons == 1:
            super().on_mouse_release(x, y, buttons, modifiers)

    def iteminfo(self, item):
        content = []
        it = item.itemtype
        content.append('name: ' + it.name)
        content.append('max_use: ' + str(it.max_use))
        content.append('use:' + str(item.use))
        content.append('type: ' + it.weapontype)
        content.append('power: ' + str(it.power))
        content.append('weight: ' + str(it.weight))
        content.append('hit: ' + str(it.hit))
        content.append('critical: ' + str(it.critical))
        content.append('max_range: ' + str(it.max_range))
        content.append('min_range: ' + str(it.min_range))
        info = Info(size=(self.w // 2, self.h), position=(self.w // 2, 0))
        self.parent.add(info)
        info.display(content)
        self.parent.remove(self)
        self.parent.wpinfo = info
        self.parent.select_target(item)


    def cancel(self):
        self.arena.state = 'valid_dst'
        self.parent.add(self.parent.menu)
        self.parent.remove(self)
        del self

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == 4:
            self.cancel()

class Endturn(Menu):
    is_event_handler = True
    def __init__(self, arena):
        super().__init__(title='Endturn')
        l = []
        l.append(MenuItem('Endturn', self.end_turn))
        l.append(MenuItem('Cancel', self.cancel))

        self.position = - director.get_window_size()[0] * 3 // 8, 0
        self.create_menu(l, zoom_in(), zoom_out())
        self.arena = arena

    def cancel(self):
        self.arena.is_event_handler = True
        self.parent.remove(self)
        del self

    def end_turn(self):
        self.arena.end_turn()
        self.parent.remove(self)
        del self

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == 4:
            self.cancel()
