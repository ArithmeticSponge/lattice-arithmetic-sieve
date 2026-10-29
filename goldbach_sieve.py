import math
import tkinter as tk
from tkinter import messagebox

class SetaccioGoldbachInterattivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Lattice Arithmetic Sieve - Proiezione Geometrica di Goldbach")
        self.zoom = 25
        self.pan_x = 50
        self.pan_y = 650  # Posiziona l'origine in basso a sinistra
        
        # Precalcolo dei primi fino a un limite ragionevole per la visualizzazione
        self.limite_primi = 5000
        self.primi = self.calcola_primi(self.limite_primi)
        self.numero_pari = 60  # Impostato a 60 così vedi subito lo splendido grafico di prima
        self.coppie_attuali = []

        # Layout principale diviso in due pannelli
        self.pannello_controllo = tk.Frame(root, width=250, bg="#f4f4f6", bd=1, relief=tk.SUNKEN)
        self.pannello_controllo.pack(side=tk.LEFT, fill=tk.Y)
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configurazione comandi interattivi nel pannello sinistro
        self.setup_interfaccia_controllo()

        # Legami del mouse per lo spostamento e zoom della griglia
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<MouseWheel>", self.zoom_wheel)

        self.aggiorna_calcoli_goldbach()
        self.disegna_struttura()

    def calcola_primi(self, n):
        setaccio = [True] * (n + 1)
        for p in range(2, int(math.sqrt(n)) + 1):
            if setaccio[p]:
                for i in range(p * p, n + 1, p):
                    setaccio[i] = False
        return {i for i in range(2, n + 1) if setaccio[i]}

    def setup_interfaccia_controllo(self):
        # Spazio di immissione del numero pari
        lbl = tk.Label(self.pannello_controllo, text="Inserisci Numero Pari (N):", font=("Arial", 11, "bold"), bg="#f4f4f6", fg="black")
        lbl.pack(pady=(20, 5), padx=10, anchor="w")
        
        self.entry_numero = tk.Entry(self.pannello_controllo, font=("Arial", 12), width=15, bg="white", fg="black")
        self.entry_numero.insert(0, str(self.numero_pari))
        self.entry_numero.pack(pady=5, padx=10, anchor="w")
        
        btn_calcola = tk.Button(self.pannello_controllo, text="Visualizza Proiezione", command=self.cambia_numero_pari, font=("Arial", 10, "bold"), bg="#4CAF50", fg="black")
        btn_calcola.pack(pady=10, padx=10, fill=tk.X)

        # Sezione dei risultati testuali integrati
        lbl_res = tk.Label(self.pannello_controllo, text="Coppie di Goldbach:", font=("Arial", 11, "bold"), bg="#f4f4f6", fg="black")
        lbl_res.pack(pady=(20, 5), padx=10, anchor="w")

        # Riquadro di testo con colore nero esplicito e barra di scorrimento
        self.lista_coppie_testo = tk.Text(self.pannello_controllo, font=("Courier", 10, "bold"), bg="white", fg="black", height=20, width=28)
        self.lista_coppie_testo.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        lbl_info = tk.Label(self.pannello_controllo, text="Trascina con il mouse per esplorare.\nUsa la rotella per lo Zoom.", font=("Arial", 9, "italic"), bg="#f4f4f6", fg="black")
        lbl_info.pack(pady=20, padx=10)

    def cambia_numero_pari(self):
        try:
            valore = int(self.entry_numero.get())
            if valore < 4 or valore % 2 != 0:
                raise ValueError
            self.numero_pari = valore
            self.aggiorna_calcoli_goldbach()
            self.disegna_struttura()
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un numero intero pari maggiore o uguale a 4.")

    def aggiorna_calcoli_goldbach(self):
        self.coppie_attuali = []
        # Trova tutte le coppie (p1, p2) tali che p1 + p2 = N
        for p1 in sorted(self.primi):
            if p1 >= self.numero_pari: break
            p2 = self.numero_pari - p1
            if p2 in self.primi:
                self.coppie_attuali.append((p1, p2))
        
        # Aggiorna il pannello di testo laterale
        self.lista_coppie_testo.delete("1.0", tk.END)
        self.lista_coppie_testo.insert(tk.END, f"Per N = {self.numero_pari}:\n\n")
        for c in self.coppie_attuali:
            self.lista_coppie_testo.insert(tk.END, f" {self.numero_pari} = {c[0]} + {c[1]}\n")

    def deve_avere_punto(self, x, y):
        if x == 0 and y == 0: return False
        if abs(x) == 1 or abs(y) == 1: return False
        if x == 0: return abs(y) > 1
        if y == 0: return abs(x) > 1
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

        # 1. Disegna le Lame di Luce Verticali (Primi su asse X) e Orizzontali (Primi su asse Y)
        for p in self.primi:
            if min_x <= p <= max_x:
                sx = p * self.zoom + self.pan_x
                self.canvas.create_line(sx, 0, sx, h, fill="#e8f5e9", width=self.zoom * 0.8) # Verde chiaro
            if min_y <= p <= max_y:
                sy = self.pan_y - p * self.zoom
                self.canvas.create_line(0, sy, w, sy, fill="#e8f5e9", width=self.zoom * 0.8)

        # 2. Disegna la griglia di sfondo sottile del reticolo geometrico
        for gx in range(max(0, min_x), max_x):
            sx = gx * self.zoom + self.pan_x
            self.canvas.create_line(sx, 0, sx, h, fill="#f0f0f0")
        for gy in range(max(0, min_y), max_y):
            sy = self.pan_y - gy * self.zoom
            self.canvas.create_line(0, sy, w, sy, fill="#f0f0f0")

        # 3. Disegna l'asse cartesiano primario
        self.canvas.create_line(self.pan_x, 0, self.pan_x, h, fill="#888888", width=2)
        self.canvas.create_line(0, self.pan_y, w, self.pan_y, fill="#888888", width=2)

        # 4. Disegna la Diagonale Speculare di Goldbach (la linea a 45° decrescente)
        x_inizio = 0 * self.zoom + self.pan_x
        y_inizio = self.pan_y - self.numero_pari * self.zoom
        x_fine = self.numero_pari * self.zoom + self.pan_x
        y_fine = self.pan_y - 0 * self.zoom
        self.canvas.create_line(x_inizio, y_inizio, x_fine, y_fine, fill="#2196F3", width=3, dash=(4, 2)) # Blu tratteggiato

        # 5. Disegna i nodi di ostruzione del reticolo (Punti e Vuoti del Setaccio)
        r_punto = max(2, self.zoom // 8)
        for gx in range(max(0, min_x), max_x):
            for gy in range(max(0, min_y), max_y):
                if self.deve_avere_punto(gx, gy):
                    cx = gx * self.zoom + self.pan_x
                    cy = self.pan_y - gy * self.zoom
                    self.canvas.create_oval(cx - r_punto, cy - r_punto, cx + r_punto, cy + r_punto, fill="#b0bec5", outline="")

        # 6. Evidenzia graficamente gli Incontri Perfetti delle coppie di Goldbach
        for c in self.coppie_attuali:
            p1, p2 = c[0], c[1]
            cx = p1 * self.zoom + self.pan_x
            cy = self.pan_y - p2 * self.zoom
            
            # Disegna un cerchio luminoso concentrico nel punto esatto d'incontro
            r_gold = max(5, self.zoom // 4)
            self.canvas.create_oval(cx - r_gold, cy - r_gold, cx + r_gold, cy + r_gold, outline="#ff5722", width=3, fill="#ffebe6")
            self.canvas.create_text(cx, cy - (r_gold + 10), text=f"({p1}+{p2})", font=("Arial", 9, "bold"), fill="#d84315")

    # Funzioni di interazione per lo scorrimento dello schermo
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
        if 5 <= nuovo_zoom <= 150:
            self.pan_x = event.x - (event.x - self.pan_x) * (nuovo_zoom / self.zoom)
            self.pan_y = event.y - (event.y - self.pan_y) * (nuovo_zoom / self.zoom)
            self.zoom = nuovo_zoom
            self.disegna_struttura()

if __name__ == "__main__":
    finestra = tk.Tk()
    finestra.geometry("1150x850")
    app = SetaccioGoldbachInterattivo(finestra)
    finestra.bind("<Configure>", lambda e: app.disegna_struttura())
    finestra.mainloop()
