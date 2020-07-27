import tkinter as tk
from random import triangular
from numpy import cross

class GiftWrapper():
    def __init__(self, master):
        self.window = tk.Canvas(master, width=500, height=500)
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_window)
        self.start_button = tk.Button(master, text="Start", command=self.main)
        self.window.pack()
        self.reset_button.pack()
        self.start_button.pack()
        self.reset_button.invoke()

    def reset_window(self):
        self.points = []
        self.window.delete('all')
        for i in range(100):
            randx = triangular(100,400, 250)
            randy = triangular(100,400, 250)
            point_id = self.window.create_oval(randx-1, randy-1, randx+1, randy+1, fill='black')
            self.points.append((point_id, randx, randy))
        self.window.update()
        self.start_button['state'] = 'normal'

    def main(self):
        self.reset_button['state'] = 'disabled'
        self.start_button['state'] = 'disabled'
        startpoint = currpoint = min(self.points, key=lambda x: x[1])
        hull_coords = [startpoint[1], startpoint[2]]
        while True:
            hull_line = None
            self.window.itemconfig(currpoint[0], outline='red', fill='red')
            self.window.update()
            for i, point in enumerate(self.points):
                if point[0] == currpoint[0]:
                    continue
                line_id = self.window.create_line(currpoint[1], currpoint[2], point[1], point[2], fill='green')
                line_vec = (point[1]-currpoint[1], point[2]-currpoint[2], 0)
                self.window.update()
                if not hull_line:
                    hull_line = (line_id, line_vec, point, i)
                    self.window.itemconfig(hull_line[0], fill='black')
                elif cross(hull_line[1], line_vec)[2] > 0:
                    self.window.delete(line_id)
                else:
                    self.window.delete(hull_line[0])
                    hull_line = (line_id, line_vec, point, i)
                    self.window.itemconfig(hull_line[0], fill='black')
                self.window.update()
            del self.points[hull_line[3]]
            currpoint = hull_line[2]
            hull_coords.extend(currpoint[1:])

            if currpoint[0] == startpoint[0]:
                break
        self.window.create_polygon(*hull_coords, fill='purple')
        self.window.update()
        self.reset_button['state'] = 'normal'

if __name__ == '__main__':
    root = tk.Tk()
    sorter = GiftWrapper(root)
    root.mainloop()
