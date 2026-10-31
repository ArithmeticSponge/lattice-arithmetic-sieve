mport math
import tkinter as tk
from tkinter import messagebox

class SetaccioChenInterattivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Lattice Arithmetic Sieve - Visualizzazione del Teorema di Chen")
        self.zoom = 25
        self.pan_x = 50
        self.pan_y = 650
        
        self.limite_calcolo = 5000
        self.primi = self.calcola_primi(self.limite_calcolo)
        self.semiprimi = self.calcola_semiprimi(self.limite_calcolo)
        
        self.numero_pari = 22
        self.soluzioni_goldbach = [] # Primo + Primo
        self.soluzioni_chen = []     # Primo + Semiprimo (o viceversa)

        self.pannello_controllo = tk.Frame(root, width=280, bg="#f4f4f6", bd=1, relief=tk.SUNKEN)
        self.pannello_controllo.pack(side=tk.LEFT, fill=tk.Y)
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_interfaccia_controllo()

        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<MouseWheel>", self.zoom_wheel)

        self.aggiorna_combinazioni_chen()
        self.disegna_struttura()

    def calcola_primi(self, n):
        setaccio = [True] * (n + 1)
        for p in range(2, int(math.sqrt(n)) + 1):
            if setaccio[p]:
                for i in range(p * p, n + 1, p):
                    setaccio[i] = False
        return {i for i in range(2, n + 1) if setaccio[i]}

    def calcola_semiprimi(self, n):
        semiprimi = set()
        lista_primi = sorted(list(self.primi))
        for i in range(len(lista_primi)):
            for j in range(i, len(lista_primi)):
                prod = lista_primi[i] * lista_primi[j]
                if prod <= n:
                    semiprimi.add(prod)
                else:
                    break
        return semiprimi

    def setup_interfaccia_controllo(self):
        lbl = tk.Label(self.pannello_controllo, text="Numero Pari (N):", font=("Arial", 11, "bold"), bg="#f4f4f6", fg="black")
        lbl.pack(pady=(20, 5), padx=10, anchor="w")
        
        self.entry_numero = tk.Entry(self.pannello_controllo, font=("Arial", 12), width=15, bg="white", fg="black")
        self.entry_numero.insert(0, str(self.numero_pari))
        self.entry_numero.pack(pady=5, padx=10, anchor="w")
        
        btn_calcola = tk.Button(self.pannello_controllo, text="Visualizza Teorema Chen", command=self.cambia_numero_pari, font=("Arial", 10, "bold"), bg="#2196F3", fg="black")
        btn_calcola.pack(pady=10, padx=10, fill=tk.X)

        lbl_res = tk.Label(self.pannello_controllo, text="Scomposizioni Rilevate:", font=("Arial", 11, "bold"), bg="#f4f4f6", fg="black")
        lbl_res.pack(pady=(20, 5), padx=10, anchor="w")

        self.lista_testo = tk.Text(self.pannello_controllo, font=("Courier", 9, "bold"), bg="white", fg="black", height=22, width=32)
        self.lista_testo.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    def cambia_numero_pari(self):
        try:
            valore = int(self.entry_numero.get())
            if valore < 4 or valore % 2 != 0: raise ValueError
            self.numero_pari = valore
            self.aggiorna_combinazioni_chen()
            self.disegna_struttura()
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero intero pari >= 4.")

    def aggiorna_combinazioni_chen(self):
        self.soluzioni_goldbach = []
        self.soluzioni_chen = []
        
        for x in range(2, self.numero_pari):
            y = self.numero_pari - x
            if x in self.primi and y in self.primi:
                self.soluzioni_goldbach.append((x, y))
            elif (x in self.primi and y in self.semiprimi) or (x in self.semiprimi and y in self.primi):
                self.soluzioni_chen.append((x, y))

        self.lista_testo.delete("1.0", tk.END)
        self.lista_testo.insert(tk.END, f"Per N = {self.numero_pari}:\n\n")
        self.lista_testo.insert(tk.END, "--- PRIMO + PRIMO ---\n")
        for s in self.soluzioni_goldbach:
            self.lista_testo.insert(tk.END, f" {self.numero_pari} = {s[0]} + {s[1]}\n")
        
        self.lista_testo.insert(tk.END, "\n--- PRIMO + SEMIPRIMO ---\n")
        for s in self.soluzioni_chen:
            self.lista_testo.insert(tk.END, f" {self.numero_pari} = {s[0]} + {s[1]}\n")

    def deve_avere_punto(self, x, y):
        if x == 0 and y == 0: return False
        if abs(x) == 1 or abs(y) == 1: return False
        if x == 0 or y == 0: return True
        return math.gcd(abs(x), abs(y)) > 1

    def disegna_struttura(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1: w, h = 900, 800

        min_x = int((-self.pan_x) / self.zoom) - 1
        max_x = int((w - self.pan_x) / self.zoom) + 1
        min_y = int((self.pan_y - h) / self.zoom) - 1
        max_y = int(self.pan_y / self.zoom) + 1

        # 1. Disegna le Lame di Luce (Primi - Verde Soffuso)
        for p in self.primi:
            if min_x <= p <= max_x:
                sx = p * self.zoom + self.pan_x
                self.canvas.create_line(sx, 0, sx, h, fill="#e8f5e9", width=self.zoom * 0.8)
            if min_y <= p <= max_y:
                sy = self.pan_y - p * self.zoom
                self.canvas.create_line(0, sy, w, sy, fill="#e8f5e9", width=self.zoom * 0.8)

        # 2. Disegna le Lame di Penombra (Semiprimi - Grigio/Azzurro Soffuso)
        for sp in self.semiprimi:
            if min_x <= sp <= max_x:
                sx = sp * self.zoom + self.pan_x
                self.canvas.create_line(sx, 0, sx, h, fill="#e1f5fe", width=self.zoom * 0.8)
            if min_y <= sp <= max_y:
                sy = self.pan_y - sp * self.zoom
                self.canvas.create_line(0, sy, w, sy, fill="#e1f5fe", width=self.zoom * 0.8)

        # 3. Griglia e Assi di Sfondo
        for gx in range(max(0, min_x), max_x):
            sx = gx * self.zoom + self.pan_x
            self.canvas.create_line(sx, 0, sx, h, fill="#f5f5f5")
        for gy in range(max(0, min_y), max_y):
            sy = self.pan_y - gy * self.zoom
            self.canvas.create_line(0, sy, w, sy, fill="#f5f5f5")

        self.canvas.create_line(self.pan_x, 0, self.pan_x, h, fill="#888888", width=2)
        self.canvas.create_line(0, self.pan_y, w, self.pan_y, fill="#888888", width=2)

        # 4. Diagonale del Numero Pari N
        x_inizio, y_inizio = 0 * self.zoom + self.pan_x, self.pan_y - self.numero_pari * self.zoom
        x_fine, y_fine = self.numero_pari * self.zoom + self.pan_x, self.pan_y - 0 * self.zoom
        self.canvas.create_line(x_inizio, y_inizio, x_fine, y_fine, fill="#9c27b0", width=3, dash=(4, 2))

        # 5. Nodi del reticolo
        r_punto = max(2, self.zoom // 8)
        for gx in range(max(0, min_x), max_x):
            for gy in range(max(0, min_y), max_y):
                if self.deve_avere_punto(gx, gy):
                    cx, cy = gx * self.zoom + self.pan_x, self.pan_y - gy * self.zoom
                    self.canvas.create_oval(cx - r_punto, cy - r_punto, cx + r_punto, cy + r_punto, fill="#cfd8dc", outline="")

        # 6. Accensione Intersezioni Goldbach (Arancione)
        for s in self.soluzioni_goldbach:
            cx, cy = s[0] * self.zoom + self.pan_x, self.pan_y - s[1] * self.zoom
            r_g = max(5, self.zoom // 4)
            self.canvas.create_oval(cx - r_g, cy - r_g, cx + r_g, cy + r_g, outline="#ff5722", width=3, fill="#ffebe6")

        # 7. Accensione Intersezioni Chen (Blu/Azzurro)
        for s in self.soluzioni_chen:
            cx, cy = s[0] * self.zoom + self.pan_x, self.pan_y - s[1] * self.zoom
            r_c = max(5, self.zoom // 4)
            self.canvas.create_oval(cx - r_c, cy - r_c, cx + r_c, cy + r_c, outline="#00bcd4", width=3, fill="#e0f7fa")

    def scroll_start(self, event): self.last_x, self.last_y = event.x, event.y
    def scroll_move(self, event):
        self.pan_x += event.x - self.last_x
        self.pan_y += event.y - self.last_y
        self.last_x, self.last_y = event.x, event.y
        self.disegna_struttura()
    def zoom_wheel(self, event):
        fattore = 1.1 if event.delta > 0 else 0.9
        nuovo_zoom = self.zoom * fattore
        if 5 <= nuovo_zoom <= 150:
            self.pan_x = event.x - (event.x - self.pan_x) * (nuovo_zoom / self.zoom)
            self.pan_y = event.y - (event.y - self.pan_y) * (nuovo_zoom / self.zoom)
            self.zoom = nuovo_zoom
            self.disegna_struttura()

if __name__ == "__main__":
    finestra = tk.Tk()
    finestra.geometry("1150x850")
    app = SetaccioChenInterattivo(finestra)
    finestra.bind("<Configure>", lambda e: app.disegna_struttura())
    finestra.mainloop()
