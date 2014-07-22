import kivy
kivy.require('1.8.0')
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.properties import NumericProperty,ListProperty,ReferenceListProperty,AliasProperty,BooleanProperty,ObjectProperty
from kivy.vector import Vector

from kivy.app import App

class FilterVIew(FloatLayout):
     pass

class CentralLine(Widget):
    calc_pos=ListProperty([0,0])
    my_points=ListProperty([0,0])
    def __init__(self,**kwargs):
        super(CentralLine, self).__init__(**kwargs)

class Dot(Widget):
    """modified Slider for x an y value"""
    x_value = NumericProperty(0.)
    y_value = NumericProperty(0.)
    x_min= NumericProperty(0.)
    y_min= NumericProperty(0.)
    x_max= NumericProperty(100.)
    y_max= NumericProperty(0.)
    padding = NumericProperty(10)
    limit_left=NumericProperty(0)
    limit_right=NumericProperty(10)
    limit_bottom=NumericProperty(0)
    limit_top=NumericProperty(10)

    def get_x_norm_value(self):
        vmin = self.x_min
        d = self.x_max - vmin
        if d == 0:
            return 0
        return (self.x_value - vmin) / float(d)

    def get_y_norm_value(self):
        vmin = self.y_min
        d = self.y_max - vmin
        if d == 0:
            return 0
        return (self.y_value - vmin) / float(d)

    def set_x_norm_value(self, x_value):
        vmin = self.x_min
        val = x_value * (self.x_max - vmin) + vmin
        self.x_value = min(round((val - vmin) )  + vmin,
                             self.x_max)

    def set_y_norm_value(self, y_value):
        vmin = self.y_min
        val = y_value * (self.y_max - vmin) + vmin

        self.y_value = min(round((val - vmin) )   + vmin,
                             self.y_max)


    x_value_normalized = AliasProperty(get_x_norm_value, set_x_norm_value,
                                     bind=('x_value', 'x_min', 'x_max'))

    y_value_normalized = AliasProperty(get_y_norm_value, set_y_norm_value,
                                     bind=('y_value', 'y_min', 'y_max'))

    def get_x_value_pos(self):
        padding = self.padding
        x = self.limit_left
        w=self.limit_right-self.limit_left

        nval = self.x_value_normalized
        self.center_x=x + padding + nval * (w - 2 * padding)
        return x + padding + nval * (w - 2 * padding)

    def get_y_value_pos(self):
        padding = self.padding
        y = self.limit_bottom
        h=self.limit_top-self.limit_bottom
        nval = self.y_value_normalized
        self.center_y=y + padding + nval * (h - 2 * padding)

        return y + padding + nval * (h - 2 * padding)

    def set_x_value_pos(self, pos):
        padding = self.padding
        x = min(self.limit_right - padding, max(pos, self.limit_left + padding))
        w=self.limit_right-self.limit_left

        if self.width == 0:
            self.x_value_normalized = 0
        else:
            self.x_value_normalized = (x - self.limit_left - padding
                                     ) / float(w - 2* padding)
            self.center_x=x

    def set_y_value_pos(self, pos):
        padding = self.padding
        y = min(self.limit_top - padding, max(pos, self.limit_bottom + padding))
        h=self.limit_top-self.limit_bottom


        self.y_value_normalized = (y - self.limit_bottom - padding
                                     ) / float(h - 2 * padding)
        self.center_y=y

    x_value_pos=AliasProperty(get_x_value_pos, set_x_value_pos,
                              bind=('x', 'y', 'limit_left', 'limit_right', 'x_min',
                                    'x_max', 'x_value_normalized'))
    y_value_pos=AliasProperty(get_y_value_pos, set_y_value_pos,
                              bind=('x', 'y', 'limit_bottom', 'limit_top', 'y_min',
                                    'y_max', 'y_value_normalized'))

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return

        elif self.collide_point(*touch.pos):
            touch.grab(self)
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            return True

class FilterDot(Dot):

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return

        elif self.collide_point(*touch.pos):
            touch.grab(self)
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            self.parent.cdot.x_value=round((self.parent.lpd.x_value+self.parent.hpd.x_value)/2,0)
            self.parent.cdot.y_value=round((self.parent.lpd.y_value+self.parent.hpd.y_value)/2,0)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            self.parent.cdot.x_value=round((self.parent.lpd.x_value+self.parent.hpd.x_value)/2,0)
            self.parent.cdot.y_value=round((self.parent.lpd.y_value+self.parent.hpd.y_value)/2,0)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.x_value_pos = touch.x
            self.y_value_pos = touch.y
            self.parent.cdot.x_value=round((self.parent.lpd.x_value+self.parent.hpd.x_value)/2,0)
            self.parent.cdot.y_value=round((self.parent.lpd.y_value+self.parent.hpd.y_value)/2,0)
            return True

class CenterDot(Dot):
    limit_x=NumericProperty(0)

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return

        elif self.collide_point(*touch.pos):
            touch.grab(self)
            lp_value=self.parent.lpd.x_value
            hp_value=self.parent.hpd.x_value
            self.lp_range=self.x_value-lp_value
            self.hp_range=self.x_value-hp_value

        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            lp_value=self.parent.lpd.x_value
            hp_value=self.parent.hpd.x_value

            self.x_value_pos = touch.x
            self.parent.lpd.x_value=self.x_value-self.lp_range
            self.parent.hpd.x_value=self.x_value-self.hp_range

            if self.parent.lpd.x_value<0 :
                self.parent.lpd.x_value=0
                self.x_value= self.lp_range
                self.parent.hpd.x_value=self.x_value+self.lp_range
                print("test")

            if self.parent.hpd.x_value<0 :
                self.parent.hpd.x_value=0
                self.x_value= self.hp_range
                self.parent.lpd.x_value=self.x_value-self.lp_range

            if self.parent.lpd.x_value>100 :
                self.parent.lpd.x_value=100
                self.x_value= 100+self.lp_range
                self.parent.hpd.x_value=self.x_value-self.hp_range

            if self.parent.hpd.x_value>100 :
                self.parent.hpd.x_value=100
                self.x_value= 100+self.hp_range
                self.parent.lpd.x_value=self.x_value-self.lp_range

            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            pass

            return True

class BezierLp(Widget):
    list_points=ListProperty([])
    l_indices=ListProperty([])

    def calc_bez_point(self,t,p0,p1,p2,p3):
        u=1-t
        tt=t*t
        uu=u*u
        uuu=uu*u
        ttt=tt*t
        p = uuu * p0
        p += 3 * uu * t * p1
        p += 3 * u * tt * p2
        p += ttt * p3

        return p

    def make_line(self):
        parent=self.parent
        dot=self.parent.lpd
        vertices = []
        indices = []
        step = 20
        middle_y=parent.y+parent.height/2
        vertices.extend([
        dot.x_value_pos,parent.y,0,0,
        parent.x,parent.y,0,0,
        parent.x,middle_y,0,0,
        dot.x_value_pos-200,middle_y,0,0

        ])

        p3=Vector(dot.x_value_pos,middle_y-91)
        p2=Vector(dot.x_value_pos+10,middle_y+52+(dot.y_value*5))
        p1=Vector(dot.x_value_pos-100,middle_y-6)
        p0=Vector(dot.x_value_pos-200,middle_y)

        for i in range(step):
            t=i/step
            b_p=self.calc_bez_point(t, p0, p1, p2, p3)
            vertices.extend([b_p[0],b_p[1],b_p[0],b_p[1]])

        vertices.extend([
        dot.x_value_pos,parent.y,0,0,

        ])

        len_vert=int(len(vertices)/4)
        for z in range(len_vert):
            indices.append(z)


        self.list_points=vertices
        self. l_indices=indices

class BezierHp(Widget):
    list_points=ListProperty([])
    l_indices=ListProperty([])

    def calc_bez_point(self,t,p0,p1,p2,p3):
        u=1-t
        tt=t*t
        uu=u*u
        uuu=uu*u
        ttt=tt*t
        p = uuu * p0
        p += 3 * uu * t * p1
        p += 3 * u * tt * p2
        p += ttt * p3

        return p

    def make_line(self):
        parent=self.parent
        dot=self.parent.hpd
        vertices = []
        indices = []
        step = 10
        middle_y=parent.y+parent.height/2
        vertices.extend([
        parent.right,middle_y,0,0,
        parent.right,parent.y,0,0,
        dot.x_value_pos,parent.y,0,0,
        dot.x_value_pos,middle_y-73,0,0
        ])

        p0=Vector(dot.x_value_pos,middle_y-73)
        p1=Vector(dot.x_value_pos+5,middle_y+10)
        p2=Vector(dot.x_value_pos-23,middle_y+2)
        p3=Vector(dot.x_value_pos+117,middle_y)

        for i in range(step):
            t=i/step
            b_p=self.calc_bez_point(t, p0, p1, p2, p3)
            vertices.extend([b_p[0],b_p[1],0,0])

        vertices.extend([
        parent.right,middle_y,0,0
        ])

        len_vert=int(len(vertices)/4)
        for z in range(len_vert):
            indices.append(z)

        self.list_points=vertices
        self. l_indices=indices

class FilterApp(App):

    def build(self):
        fl = FloatLayout()
        inspector.create_inspector(Window, fl)
        filter=FilterVIew()
        return filter

if __name__ == '__main__':
    FilterApp().run()