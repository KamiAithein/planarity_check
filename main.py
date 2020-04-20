from tkinter import *
import numpy as np

#height of window
width, height = 500, 500

#width of vertex (edge width, too lazy to fix)
v_width = 20

#goes alphabetically and wraps around back to start_char after reaching z
start_char = 'u'

root = Tk()

frame = Frame(root)
frame.pack()

canvas = Canvas(root, width=width, height=height)
canvas.pack()

class Vertex:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
class Edge:
    def __init__(self, v_pair):
        self.v_pair = v_pair

class Graph:
    def __init__(self):
        self.V = set([])
        self.E = set([])
    
    def reset(self):
        self.V = set([])
        self.E = set([])
    
    def add_edge(self, v_pair):
        for v in v_pair:
            if v not in self.V:
                raise ValueError("add edge between one or more vertexes that do not exist")
        self.E.add(Edge(v_pair))

    def add_vertex(self, pos, name):
        self.V.add(Vertex(pos, name))



label_char = start_char

G = Graph()

selected = set([])

state = 0
#0 default
#1 waiting to add vertex after Button-1
#2 a vertex as been selected

mouse_down = False


def click_reset():
    reset()

def reset():
    global state
    global label_char
    selected = set([])
    state = 0
    canvas.delete("all")
    #canvas.create_rectangle(0,0,width,height, fill = "black")
    G.reset()
    label_char = start_char
    update_canvas(canvas)


def click_add_v():
    global state
    state = 1

def add_vertex(pos, name):
    G.add_vertex(pos, name)



def add_edge():
    if(len(selected) == 2):
        v_pair = selected.pop(), selected.pop()
        v_pair2 = v_pair[1], v_pair[0]
        if v_pair not in G.E and v_pair2 not in G.E:
            G.add_edge(v_pair)
        #need some check that acutally works here



def select(event, vertex):
    select.add(vertex)

def update_canvas(canvas):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, width, height, fill = "black")
    for e in G.E:
        v1, v2 = e.v_pair
        (x1, y1), (x2, y2) = v1.pos, v2.pos
        canvas.create_line(x1, y1, x2, y2, fill = "white")
    for v in G.V:
        x, y = v.pos
        canvas.create_oval(x, y, x, y, width = v_width, outline = 'red' if v in selected else 'white')
        canvas.create_text(x, y, text=v.name)
    

def point_within_circle(c_pos, c_r, pos):
    cx, cy = c_pos
    x, y = pos
    return ((x-cx)**2 + (y-cy)**2)**.5 < c_r



def mclick(event):
    global state
    global selected
    global mouse_down
    global label_char
    mouse_down = True

    if state == 0:
        
        x, y = event.x, event.y
        event_pos = x, y
        for v in G.V:
            c_pos = v.pos
            if point_within_circle(c_pos, v_width/2.0, event_pos) and v not in selected:
                selected.add(v)
                state = 2

    elif state == 1:
        add_vertex((event.x, event.y), label_char)
        label_char = chr((ord(label_char) - ord(start_char) + 1) % (ord('z')  + 1 - ord(start_char)) + ord(start_char)) 
        state = 0
    
    elif state == 2:
        x, y = event.x, event.y
        event_pos = x, y
        len_1 = len(selected)
        for v in G.V:
            c_pos = v.pos
            if point_within_circle(c_pos, v_width/2.0, event_pos) and v not in selected:
                selected.add(v)
                add_edge()
        if(len_1 == len(selected)):
            selected = set([])
        state = 0

    update_canvas(canvas)

def mrelease(event):
    global mouse_down
    mouse_down = False
    update_canvas(canvas)

def mmove(event):
    if(mouse_down and len(selected) == 1):
        v = selected.pop()
        v.pos = (event.x, event.y)
        selected.add(v)
    update_canvas(canvas)


reset_b = Button(frame, text="reset", fg="black", command=click_reset)
reset_b.pack(side = LEFT)

add_v_b = Button(frame, text="add vertex", fg="black", command=click_add_v)
add_v_b.pack(side = LEFT)



root.bind('<Motion>', mmove)
root.bind('<Button-1>', mclick)
root.bind('<ButtonRelease-1>', mrelease)





mainloop()