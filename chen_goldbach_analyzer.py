cd ~/RicercaMatematica && cat << 'EOF' > chen_goldbach_analyzer.py
import math
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def calcola_primi(n):
    setaccio = [True] * (n + 1)
    for p in range(2, int(math.sqrt(n)) + 1):
        if setaccio[p]:
            for i in range(p * p, n + 1, p): setaccio[i] = False
    return {i for i in range(2, n + 1) if setaccio[i]}

def calcola_semiprimi(n, primi):
    semiprimi = set()
    lista_primi = sorted(list(primi))
    for i in range(len(lista_primi)):
        for j in range(i, len(lista_primi)):
            prod = lista_primi[i] * lista_primi[j]
            if prod <= n: semiprimi.add(prod)
            else: break
    return semiprimi

def analizza_intervallo(start, end, step_type, step_val):
    print("\n[1/3] Generazione database dei numeri primi...")
    primi = calcola_primi(end)
    print("[2/3] Generazione database dei semiprimi...")
    semiprimi = calcola_semiprimi(end, primi)
    
    valori_N = []
    conteggi_goldbach = []
    conteggi_chen = []
    
    print("[3/3] Scansione dell'intervallo selezionato...")
    corrente = start
    while corrente <= end:
        if corrente % 2 == 0 and corrente >= 4:
            goldbach_count = 0
            chen_count = 0
            for x in range(2, corrente):
                y = corrente - x
                if x <= y:
                    if x in primi and y in primi:
                        goldbach_count += 1
                    elif (x in primi and y in semiprimi) or (x in semiprimi and y in primi):
                        chen_count += 1
            
            valori_N.append(corrente)
            conteggi_goldbach.append(goldbach_count)
            conteggi_chen.append(chen_count)
            
        if step_type == "1":
            corrente += 2
        elif step_type == "2":
            corrente += step_val
            if corrente % 2 != 0: corrente += 1
            
    return valori_N, conteggi_goldbach, conteggi_chen

def genera_grafico(valori_N, conteggi_goldbach, conteggi_chen):
    plt.figure(figsize=(8, 4.5))
    plt.scatter(valori_N, conteggi_goldbach, color="#ff5722", label="Goldbach (Primo+Primo)", s=15, alpha=0.7)
    plt.scatter(valori_N, conteggi_chen, color="#00bcd4", label="Chen (Primo+Semiprimo)", s=15, alpha=0.7)
    plt.title("Andamento della Densità di Soluzioni - Goldbach vs Chen")
    plt.xlabel("Numero Pari (N)")
    plt.ylabel("Numero di Coppie Uniche")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    path_grafico = "temp_goldbach_chen_plot.png"
    plt.savefig(path_grafico, dpi=200)
    plt.close()
    return path_grafico

def genera_pdf_report(start, end, valori_N, conteggi_goldbach, conteggi_chen, path_grafico):
    nome_pdf = f"Report_Statistico_Goldbach_Chen_{start}_{end}.pdf"
    doc = SimpleDocTemplate(nome_pdf, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#1a237e'), spaceAfter=15)
    text_style = ParagraphStyle('Text', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=8)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, leading=16, textColor=colors.HexColor('#0d47a1'), spaceBefore=12, spaceAfter=8)
    
    story = []
    story.append(Paragraph("<b>Lattice Arithmetic Sieve: Analisi Statistica Multi-Target</b>", title_style))
    story.append(Paragraph(f"<b>Intervallo esaminato:</b> da {start} a {end}<br/><b>Numero totale di campioni analizzati:</b> {len(valori_N)} numeri pari.", text_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>1. Grafico Comparativo delle Densità (Nuvole Strutturali)</b>", h2_style))
    story.append(Image(path_grafico, width=500, height=281))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>2. Report Tabellare dei Campioni (Estratto dei dati)</b>", h2_style))
    dati_tabella = [["Numero Pari (N)", "Coppie Goldbach (P+P)", "Coppie Chen (P+SP)", "Rapporto Chen/Goldbach"]]
    
    passo_stampa = max(1, len(valori_N) // 15)
    indici_stampa = [i for i in range(0, len(valori_N), passo_stampa)]
    if (len(valori_N)-1) not in indici_stampa: indici_stampa.append(len(valori_N)-1)
    
    for idx in indici_stampa:
        n = valori_N[idx]
        g = conteggi_goldbach[idx]
        c = conteggi_chen[idx]
        rapporto = f"{(c/g):.2f}x" if g > 0 else "N/D"
        dati_tabella.append([str(n), str(g), str(c), rapporto])
        
    t = Table(dati_tabella, colWidths=[120, 120, 120, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f5f5f5')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    
    doc.build(story)
    if os.path.exists(path_grafico): os.remove(path_grafico)
    return nome_pdf

def main():
    print("="*60)
    print("      LATTICE SIEVE - MOTORE DI SCANSIONE STATISTICA")
    print("="*60)
    try:
        start = int(input("Inserisci l'inizio del range (es. 100): "))
        end = int(input("Inserisci la fine del range (es. 1000): "))
        if start > end or start < 4: raise ValueError
    except ValueError:
        print("Errore nei valori numerici inseriti.")
        return
        
    print("\nScegli il criterio di avanzamento:")
    print("1) Tutti i numeri pari in sequenza (Passo = 2)")
    print("2) Solo determinati multipli (Passo personalizzato)")
    scelta = input("Scelta (1 o 2): ")
    
    step_val = 2
    if scelta == "2":
        try:
            step_val = int(input("Inserisci il passo del multiplo (es. 10 per fare 10, 20, 30...): "))
            if step_val <= 0: raise ValueError
        except ValueError:
            print("Passo non valido.")
            return

    valori_N, conteggi_goldbach, conteggi_chen = analizza_intervallo(start, end, scelta, step_val)
    
    if not valori_N:
        print("Nessun numero pari trovato nell'intervallo selezionato.")
        return
        
    print("\nGenerazione del grafico statistico...")
    path_img = genera_grafico(valori_N, conteggi_goldbach, conteggi_chen)
    
    print("Generazione del report accademico in PDF...")
    nome_risultato = genera_pdf_report(start, end, valori_N, conteggi_goldbach, conteggi_chen, path_img)
    
    print("\n" + "="*60)
    print(f"📊 SCANSIONE COMPLETATA CON SUCCESSO!")
    print(f"💾 Report PDF salvato nella cartella: {os.path.abspath(nome_risultato)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
EOF
