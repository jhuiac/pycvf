#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python

import gtk
import som, random

"""
Author: Marilen Corciovei
Version: $Id: som2d.py,v 1.6 2007/01/12 23:04:56 len Exp $
Description: 2D SOM example
License: BSD

"""
class SOMDisplay(som.SOM):
    def __init__(self):
        #som.SOM.__init__(self, 16, 2, som.SOM_algorithm(16))
        som.SOM.__init__(self, 24, 2, som.SA_two_phases(24))
        self.initialize_nodes()
        self.W = 400
        self.H = self.W
        self.TIMEOUT = 20
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("SOM 2d representation")
        window.connect("destroy", lambda w: gtk.main_quit())
        self.area = gtk.DrawingArea()
        self.area.set_size_request(self.W, self.H)
        window.add(self.area)
        self.area.connect("expose-event", self.draw_network)
        self.area.show()
        window.show()
        
    def initialize_nodes(self):
        self.nodes = []
        for i in range(self.r*self.r):
            node = []
            for j in range(self.n):
                node.append(random.random()/2 + .25)
            self.nodes.append(node)

    def next_sample(self):
        return [random.random(), random.random()]

    def timed_training(self):
        gtk.timeout_add(self.TIMEOUT, self.timer)

    def timer(self):
        if self.train_step() == 0:
            gtk.timeout_add(self.TIMEOUT, self.timer)
            self.refresh()

    def draw_network(self, area, event):
        self.style = self.area.get_style()
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]

        self.setColor(1, 1, 1)
        self.area.window.draw_rectangle(self.gc, True, 0, 0, self.W, self.H)

        self.setColor(0, 0, 0)

        #draw lines
        for x in range(self.r-1):
            for y in range(self.r-1):
                self.area.window.draw_line(self.gc, \
                                           self.nodes[x*self.r+y][0]*self.W, self.nodes[x*self.r+y][1]*self.H, \
                                           self.nodes[(x+1)*self.r+y][0]*self.W, self.nodes[(x+1)*self.r+y][1]*self.H)
                self.area.window.draw_line(self.gc, \
                                           self.nodes[x*self.r+y][0]*self.W, self.nodes[x*self.r+y][1]*self.H, \
                                           self.nodes[x*self.r+y+1][0]*self.W, self.nodes[x*self.r+y+1][1]*self.H)

        for i in range(self.r-1):
            self.area.window.draw_line(self.gc, \
                                       self.nodes[i*self.r+self.r-1][0]*self.W, self.nodes[i*self.r+self.r-1][1]*self.H, \
                                       self.nodes[(i+1)*self.r+self.r-1][0]*self.W, self.nodes[(i+1)*self.r+self.r-1][1]*self.H)
            self.area.window.draw_line(self.gc, 
                                       self.nodes[(self.r-1)*self.r+i][0]*self.W, self.nodes[(self.r-1)*self.r+i][1]*self.H, \
                                       self.nodes[(self.r-1)*self.r+i+1][0]*self.W, self.nodes[(self.r-1)*self.r+i+1][1]*self.H)
        
        self.setColor(1, 0, 0)
        for x in range(self.r):
            for y in range(self.r):
                self.area.window.draw_rectangle(self.gc, True, \
                                                self.nodes[x*self.r+y][0]*self.W-2, self.nodes[x*self.r+y][1]*self.H-2, \
                                                4, 4)
                                                
    def setColor(self,red,green,blue,mult=65535):
        color = self.gc.get_colormap().alloc_color(int(red * mult), int(green * mult), int(blue * mult))
        self.gc.set_foreground(color)

    def refresh(self):
        self.area.emit("expose-event", gtk.gdk.Event(gtk.gdk.EXPOSE))
        self.area.queue_draw()
        


def main():
    net = SOMDisplay()
    net.timed_training()
    gtk.main()
    return 0

if __name__=='__main__':
    main()
