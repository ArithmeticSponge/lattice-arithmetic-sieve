import math
import tkinter as tk

class GrigliaMatematicaInfinita:
    def __init__(self, root):
        self.root = root
        self.root.title("Il Setaccio Geometrico di Enrico - Navigazione Infinita")
        self.zoom = 20
        self.pan_x = 400
        self.pan_y = 400
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<MouseWheel>", self.zoom_wheel)
        self.canvas.bind("<Button-4>", self.zoom_wheel_linux)
        self.canvas.bind("<Button-5>", self.zoom_wheel_linux)
        
        limite_precalcolo = 20000
        conteggio_divisori = [0] * (limite_precalcolo + 1)
        for i in range(1, limite_precalcolo + 1):
            for j in range(i, limite_precalcolo + 1, i):
                conteggio_divisori[j] += 1
                
        self.primi = set()
        self.nac = set()
        record_divisori = 0
        for x in range(1, limite_precalcolo + 1):
            if conteggio_divisori[x] == 2:
                self.primi.add(x)
            if conteggio_divisori[x] > record_divisori:
                record_divisori = conteggio_divisori[x]
                self.nac.add(x)
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
        if width <= 1: width, height = 800, 800
        
        min_x = int((-self.pan_x) / self.zoom) - 1
        max_x = int((width - self.pan_x) / self.zoom) + 1
        min_y = int((-self.pan_y) / self.zoom) - 1
        max_y = int((height - self.pan_y) / self.zoom) + 1
        
        for gx in range(max(1, min_x), max_x):
            screen_x = gx * self.zoom + self.pan_x
            if gx in self.primi:
                self.canvas.create_line(screen_x, 0, screen_x, height, fill="#d2f7d6", width=self.zoom*0.9)
            if gx in self.nac:
                self.canvas.create_line(screen_x, 0, screen_x, height, fill="#ffe680", width=max(2, self.zoom*0.4))
                self.canvas.create_text(screen_x + 5, 30, text=f"NAC {gx}", anchor="w", fill="#b38f00", font=("Arial", 9, "bold"))
                
        for gx in range(min_x, max_x):
            screen_x = gx * self.zoom + self.pan_x
            self.canvas.create_line(screen_x, 0, screen_x, height, fill="#f0f0f0")
        for gy in range(min_y, max_y):
            screen_y = gy * self.zoom + self.pan_y
            self.canvas.create_line(0, screen_y, width, screen_y, fill="#f0f0f0")
            
        self.canvas.create_line(self.pan_x, 0, self.pan_x, height, fill="#808080", width=2)
        self.canvas.create_line(0, self.pan_y, width, self.pan_y, fill="#808080", width=2)
        
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
        self.pan_x += event.x - self.last_x
        self.pan_y += event.y - self.last_y
        self.last_x, self.last_y = event.x, event.y
        self.disegna_struttura()
    def zoom_wheel(self, event):
        fattore = 1.1 if event.delta > 0 else 0.9
        nuovo_zoom = self.zoom * fattore
        if 3 <= nuovo_zoom <= 100:
            self.pan_x = event.x - (event.x - self.pan_x) * (nuovo_zoom / self.zoom)
            self.pan_y = event.y - (event.y - self.pan_y) * (nuovo_zoom / self.zoom)
            self.zoom = nuevo_zoom
            self.disegna_struttura()
    def zoom_wheel_linux(self, event):
        fattore = 1.1 if event.num == 4 else 0.9
        nuovo_zoom = self.zoom * fattore
        if 3 <= nuovo_zoom <= 100:
            self.pan_x = event.x - (event.x - self.pan_x) * (nuovo_zoom / self.zoom)
            self.pan_y = event.y - (event.y - self.pan_y) * (nuovo_zoom / self.zoom)
            self.zoom = nuovo_zoom
            self.disegna_struttura()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x850")
    app = GrigliaMatematicaInfinita(root)
    root.bind("<Configure>", lambda e: app.disegna_struttura())
    root.mainloop()
