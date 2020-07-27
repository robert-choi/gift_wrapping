# linters need to be installed within the env who knew
# d(arccos(x))/dx < 0 so that's why we can cheat with el formula :3

import tkinter as tk
from random import triangular
import numpy as np

class TSAWrapper():
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
            randx = round(triangular(100,400, 250))
            randy = round(triangular(100,400, 250))
            point_id = self.window.create_oval(randx-1, randy-1, randx+1, randy+1, fill='black')
            self.points.append((point_id, randx, randy))
        self.window.update()
        self.start_button['state'] = 'normal'

    def main(self):
        self.reset_button['state'] = 'disabled'
        self.start_button['state'] = 'disabled'
        reference = self.points.pop(self.points.index(max(self.points, key=lambda y: y[2])))
        self.points.sort(key=lambda x: -(np.dot((1,0), (x[1]-reference[1], x[2]-reference[2]))/(np.linalg.norm((1,0))*np.linalg.norm((x[1]-reference[1], x[2]-reference[2])))))
        self.points.insert(0, reference)
        self.hull_points = [reference]
        self.hull_lines = list()
        for index, currpoint in enumerate(self.points[1:]):
            line_id = self.window.create_line(self.points[index][1], self.points[index][2], currpoint[1], currpoint[2])
            line_vec = (currpoint[1]-self.points[index][1], currpoint[2]-self.points[index][2], 0)
            self.window.itemconfig(currpoint[0], outline='red', fill='red')
            self.window.update()
            if not self.hull_lines or not np.cross(self.hull_lines[-1][1], line_vec)[2] > 0:
                self.hull_lines.append((line_id, line_vec))
                self.hull_points.append(currpoint)
            else:
                self.window.delete(line_id, self.hull_lines[-1][0])
                self.window.itemconfig(self.hull_points[-1][0], outline='black', fill='black')
                self.window.update()
                del self.hull_lines[-1], self.hull_points[-1]
                while True:
                    i_line = self.window.create_line(self.hull_points[-1][1], self.hull_points[-1][2], currpoint[1], currpoint[2])
                    i_vec = (currpoint[1]-self.hull_points[-1][1], currpoint[2]-self.hull_points[-1][2], 0)
                    self.window.update()
                    if np.cross(self.hull_lines[-1][1], i_vec)[2] > 0:
                        self.window.delete(i_line, self.hull_lines[-1][0])
                        self.window.itemconfig(self.hull_points[-1][0], outline='black', fill='black')
                        self.window.update()
                        del self.hull_lines[-1], self.hull_points[-1]
                    else:
                        self.hull_lines.append((i_line, i_vec))
                        self.hull_points.append(currpoint)
                        break

        hull_coords = [(p[1],p[2]) for p  in self.hull_points]
        self.window.create_polygon(*hull_coords, fill='purple')
        self.window.update()
        self.reset_button['state'] = 'normal'

if __name__ == '__main__':
    root = tk.Tk()
    sorter = TSAWrapper(root)
    root.mainloop()
