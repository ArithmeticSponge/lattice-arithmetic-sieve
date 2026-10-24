import tkinter as tk
import math

class GrigliaEnrico:
    def __init__(self, root):
        self.root = root
        self.root.title("Il Setaccio Geometrico di Enrico")
        self.zoom = 25 
        self.pan_x = 500 
        self.pan_y = 500
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<MouseWheel>", self.zoom_wheel) 
        self.disegna_struttura()

    def deve_avere_punto(self, x, y):
        if x == 0 and y == 0: return False
        if abs(x) == 1 or abs(y) == 1: return False
        if x == 0: return abs(y) > 1
        if y == 0: return abs(x) > 1
        return math.gcd(abs(x), abs(y)) > 1

    def disegna_struttura(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1: width, height = 1000, 1000 
        min_x = int((-self.pan_x) / self.zoom) - 1
        max_x = int((width - self.pan_x) / self.zoom) + 1
        min_y = int((-self.pan_y) / self.zoom) - 1
        max_y = int((height - self.pan_y) / self.zoom) + 1
        
        for gx in range(min_x, max_x):
            screen_x = gx * self.zoom + self.pan_x
            self.canvas.create_line(screen_x, 0, screen_x, height, fill="#f2f2f2")
        for gy in range(min_y, max_y):
            screen_y = gy * self.zoom + self.pan_y
            self.canvas.create_line(0, screen_y, width, screen_y, fill="#f2f2f2")
            
        self.canvas.create_line(self.pan_x + min_x*self.zoom, self.pan_y - min_x*self.zoom, self.pan_x + max_x*self.zoom, self.pan_y - max_x*self.zoom, fill="#ff3333", width=2, dash=(6,4))
        self.canvas.create_line(self.pan_x + min_x*self.zoom, self.pan_y + min_x*self.zoom, self.pan_x + max_x*self.zoom, self.pan_y + max_x*self.zoom, fill="#ff3333", width=2, dash=(6,4))
        self.canvas.create_line(self.pan_x, 0, self.pan_x, height, fill="#555555", width=2)
        self.canvas.create_line(0, self.pan_y, width, self.pan_y, fill="#555555", width=2)
        
        raggio_punto = max(2, self.zoom // 6) 
        for gx in range(min_x, max_x):
            for gy in range(min_y, max_y):
                mat_x = gx
                mat_y = -gy 
                if self.deve_avere_punto(mat_x, mat_y):
                    cx = gx * self.zoom + self.pan_x
                    cy = gy * self.zoom + self.pan_y
                    self.canvas.create_oval(cx - raggio_punto, cy - raggio_punto, cx + raggio_punto, cy + raggio_punto, fill="black", outline="")

    def scroll_start(self, event):
        self.last_x, self.last_y = event.x, event.y
    def scroll_move(self, event):
        self.pan_x += event.x - self.last_x if hasattr(self, 'last_x') else 0
        self.pan_y += event.y - self.last_y if hasattr(self, 'last_y') else 0
        self.last_x, self.last_y = event.x, event.y
        self.disegna_struttura()
    def zoom_wheel(self, event):
        if event.delta > 0: self.zoom = min(150, self.zoom + 2)
        else: self.zoom = max(3, self.zoom - 2)
        self.disegna_struttura()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x1000")
    app = GrigliaEnrico(root)
    root.bind("<Configure>", lambda e: app.disegna_struttura())
    root.mainloop()
