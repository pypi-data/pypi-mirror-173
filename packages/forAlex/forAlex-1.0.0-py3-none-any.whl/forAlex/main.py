import argparse
import tkinter as tk
import random

class Fish:
    def __init__(self, canvas, windowW, windowH):
        self.canvas = canvas

        self.x = random.randint(100, windowW-100)
        self.y = random.randint(100, windowH-100)
        self.dx = random.randint(-30, 30)

        self.lv = random.randint(2, 6)*10

        self.color = rgb(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

        self.windowW = windowW
        self.windowH = windowH

    def paint(self, dx, dy):
        self.canvas.create_oval(self.x-self.lv-dx, self.y-self.lv//5-dy, self.x+self.lv-dx, self.y+self.lv//5-dy, fill=self.color, outline=self.color)
        if self.dx>0:
            self.canvas.create_polygon(self.x-self.lv-dx, self.y-dy, self.x-self.lv-self.lv//2-dx, self.y-self.lv//4-dy, self.x-self.lv-self.lv//2-dx, self.y+self.lv//4-dy, fill=self.color, outline=self.color)
        else:
            self.canvas.create_polygon(self.x+self.lv-dx, self.y-dy, self.x+self.lv+self.lv//2-dx, self.y-self.lv//4-dy, self.x+self.lv+self.lv//2-dx, self.y+self.lv//4-dy, fill=self.color, outline=self.color)

    def move(self):
        self.x += self.dx
        if self.dx>0:
            if self.x>self.windowW+200:
                self.x = -200
                self.y = random.randint(100, self.windowH-100)
        if self.dx<0:
            if self.x<-200:
                self.x = self.windowW+200
                self.y = random.randint(100, self.windowH-100)

class Bubble:
    def __init__(self, canvas, windowW, windowH):
        self.canvas = canvas

        self.x = random.randint(300, windowW-100)
        self.y = random.randint(300, windowH-100)
        self.dy = random.randint(5, 15)

        self.color = rgb(200, 200, random.randint(200, 220))

        self.windowW = windowW
        self.windowH = windowH

    def paint(self, dx, dy):
        self.canvas.create_oval(self.x-3-dx, self.y-3-dy, self.x+6-dx, self.y+6-dy, fill=self.color, outline=self.color)
        self.canvas.create_oval(self.x-6-dx, self.y-12-dy, self.x+2-dx, self.y-4-dy, fill=self.color, outline=self.color)
        self.canvas.create_oval(self.x-1-dx, self.y-20-dy, self.x+7-dx, self.y-12-dy, fill=self.color, outline=self.color)
        self.canvas.create_oval(self.x-5-dx, self.y-30-dy, self.x+5-dx, self.y-20-dy, fill=self.color, outline=self.color)

    def move(self):
        self.y -= self.dy
        if self.y<200:
            self.y = self.windowH+200
            self.x = random.randint(100, self.windowW-100)

def rgb(r, g, b):
   return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0")
      for c in (r, g, b)])
        
def main():
    parser = argparse.ArgumentParser(description='Happy birthday Alex! Move the window and find a message from me:)\n \
                                      At first, You should not add "--flag" option. Enjoy this simple app and then run with "--flag" option.')
    parser.add_argument("--flag", help="The window size is maximized", action="store_true")
    args = parser.parse_args()

    root = tk.Tk()

    WIDTH = root.winfo_screenwidth()
    HEIGHT = root.winfo_screenheight()

    if args.flag:
        root.geometry('{}x{}'.format(WIDTH, HEIGHT))
        root.title("maximized window")
    else:
        root.geometry('350x300')
        root.title("move this window and find a message!")
        root.resizable(False, False)

    
    canvas = tk.Canvas(root, bg="#00bfff", width=WIDTH, height=HEIGHT)
    canvas.pack()

    lbl = tk.Label(text='Happy Birthday Alex!!', foreground='#ff0000', background='#ffd700')
    lbl.place(x=WIDTH//2, y=HEIGHT-300)

    fish = [Fish(canvas, WIDTH, HEIGHT) for _ in range(12)]
    bubble = [Bubble(canvas, WIDTH, HEIGHT) for _ in range(10)]

    def move(xx):
        
        ps_window = root.geometry().split("+")[1:]
        dx = int(ps_window[0])
        dy = int(ps_window[1])
        canvas.delete("all")
        for y in range(0, 256):
            r = 0
            g = 0
            b = int(22+180*y/256)
            canvas.create_rectangle(0-dx, HEIGHT-(HEIGHT-100)*y/256-dy, WIDTH-dx, HEIGHT-(HEIGHT-100)*(y+1)/256-dy, fill=rgb(r, g, b), outline=rgb(r, g, b))
        for x in range(WIDTH//21):
            tmp = (WIDTH//20*x+xx)
            if tmp>WIDTH:
                tmp = tmp-WIDTH-WIDTH//20
            canvas.create_arc(tmp-dx, 100-WIDTH//40-dy, tmp+WIDTH//20-dx, 100+WIDTH//40-dy, width=1, fill="#0000CA", outline="#0000CA", extent=180)
        for f in fish:
            f.move()
            f.paint(dx, dy)

        for b in bubble:
            b.move()
            b.paint(dx, dy)

        lbl.place(x=WIDTH//2-dx, y=HEIGHT-300-dy)
        xx = (xx+5)%(WIDTH+WIDTH//20)
        root.after(100, move, xx)

    root.after(100, move, 0)
    root.mainloop()
