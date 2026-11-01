import math, os

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

def esegui_calcolo():
    print("\n--- Lattice Arithmetic Sieve: Analizzatore Numerico Puro ---")
    try:
        n = int(input("Inserisci un numero pari elevato (es. 150000): "))
        if n < 4 or n % 2 != 0: raise ValueError
    except ValueError:
        print("Errore: Inserisci un intero pari valido >= 4.")
        return

    print("Calcolo in corso sui vettori numerici...")
    primi = calcola_primi(n)
    semiprimi = calcola_semiprimi(n, primi)

    goldbach, chen = [], []
    for x in range(2, n):
        y = n - x
        if x <= y:
            if x in primi and y in primi: goldbach.append((x, y))
            elif (x in primi and y in semiprimi) or (x in semiprimi and y in primi): chen.append((x, y))

    nome_file = f"report_{n}.txt"
    with open(nome_file, "w", encoding="utf-8") as f:
        f.write(f"📌 REPORT NUMERICO PER N = {n}\n")
        f.write(f"• Combinazioni Goldbach (Primo+Primo): {len(goldbach)}\n")
        f.write(f"• Combinazioni Chen (Primo+Semiprimo): {len(chen)}\n")
        f.write("==================================================\n\n")
        f.write("--- ELENCO COPPIE GOLDBACH ---\n")
        for s in goldbach: f.write(f"{n} = {s[0]} + {s[1]}\n")
        f.write("\n--- ELENCO COPPIE CHEN ---\n")
        for s in chen: f.write(f"{n} = {s[0]} + {s[1]}\n")

    print(f"📊 Calcolo completato in un lampo!")
    print(f"• Coppie Goldbach: {len(goldbach)}")
    print(f"• Coppie Chen:     {len(chen)}")
    print(f"💾 L'elenco completo di tutte le scomposizioni è stato salvato in: {os.path.abspath(nome_file)}")

if __name__ == "__main__":
    esegui_calcolo()
