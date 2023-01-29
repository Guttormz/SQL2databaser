import sqlite3 as sq
from tqdm import tqdm

conn = sq.connect('kunde.db') # Lager en database
cur = conn.cursor() # Lager en cursor


def table(): # Lager funksjonen table()

    if cur.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='post'"): # Sjekker om tabellen postnummer eksisterer
        try:
            cur.execute("DROP TABLE post") # Sletter tabellen postnummer
        except:
            sq.OperationalError

    cur.execute('''CREATE TABLE IF NOT EXISTS post (
                    postnummer      TEXT PRIMARY KEY, 
                    poststed      TEXT    NOT NULL, 
                    kommunenummer TEXT NOT NULL, 
                    kommunenavn TEXT NOT NULL, 
                    kategori TEXT NOT NULL);''') # Lager tabellen postnummer

    if cur.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='kunder'"): # Sjekker om tabellen kunder eksisterer
        try:
            cur.execute("DROP TABLE kunder") # Sletter tabellen kunder
        except:
            sq.OperationalError
            
    cur.execute('''CREATE TABLE IF NOT EXISTS kunder (
                    Kundenr    INTEGER PRIMARY KEY AUTOINCREMENT, 
                    fnavn      TEXT    NOT NULL, 
                    enavn      TEXT    NOT NULL, 
                    epost      TEXT    NOT NULL,
                    tlf        TEXT    , 
                    postnummer TEXT NOT NULL, 
                    FOREIGN    KEY (postnummer) REFERENCES postnummer (post));''')

    conn.commit() # Lagrer endringene


def postnummer(): # Lager funksjonen postnummer
    f = open('Postnummerregister.csv', 'r') # Åpner filen Postnummerregister.csv i read

    for line in tqdm(f, total=5139): # Går gjennom hver linje i filen
        cur.execute('INSERT INTO post (postnummer, poststed, kommunenummer, kommunenavn, kategori) VALUES (?,?,?,?,?)', (line.split(','))) # Legger til hver linje i tabellen postnummer

    cur.execute("DELETE FROM post WHERE postnummer IS 'Postnummer'") # Sletter linja i tabellen postnummer som inneholder "Postnummer"
    print("Informasjon hentet om postnummer") # Printer ut at informasjonen er hentet

    conn.commit() # Lagrer endringene


def kunder(): # Lager funksjonen kunder
    f = open('randoms.csv', 'r') # Åpner filen randoms.csv i read

    for line in tqdm(f, total=200): # Går gjennom hver linje i filen
        cur.execute('INSERT INTO kunder (fnavn, enavn, epost, tlf, postnummer) VALUES (?,?,?,?,?)', (line.split(','))) # Legger til hver linje i tabellen kunder

    cur.execute("DELETE FROM kunder WHERE fnavn IS 'fname'") # Sletter linja i tabellen kunder som inneholder "fname"
    print("Informasjon hentet om kunder") # Printer ut at informasjonen er hentet

    conn.commit() # Lagrer endringene

def find(): # Lager funksjonen find
    knr=int(input("Hvilken kunde vil du se info om? (Kundenr): ")) # Spør brukeren om hvilken kunde de vil se info om
    if knr>201: # Sjekker om kundenr er større enn 200
        print("Vi har ikke så mange kunder, prøv et lavere nummer. (Maks 200 kunder)") # Printer ut at vi ikke har så mange kunder
        find() # Kaller på funksjonen find igjen

    if knr<2: # Sjekker om kundenr er mindre enn 2
        print("Dette tallet er for lavt, prøv et høyere nummer. (Minst 2)") # Printer ut at dette tallet er for lavt
        find() # Kaller på funksjonen find igjen

    cur.execute("SELECT post.postnummer, post.kommunenavn, post.kategori, post.kommunenummer, post.poststed, kunder.kundenr, Kunder.fnavn, Kunder.enavn, Kunder.epost, Kunder.tlf, Kunder.postnummer FROM post INNER JOIN Kunder ON Kunder.postnummer = post.postnummer WHERE Kunder.kundenr = ?",(knr,))
    print(cur.fetchall()) # Printer ut info om kunden

    conn.commit() # Lagrer endringene

def info(): # Lager funksjonen info
    svar=(input("Vil du se info om kunder? (Ja/Nei): ")) # Spør brukeren om de vil se info om kunder
    if svar == "Ja" or svar == "ja" or svar == "j" or svar == "J": # Sjekker om svaret er ja
        find() # Kaller på funksjonen find

    if svar == "Nei" or svar == "nei" or svar == "n" or svar == "N": # Sjekker om svaret er nei
        print("Ok, da avslutter vi programmet.") # Printer ut at vi avslutter programmet
        exit() # Avslutter programmet

    conn.commit



def main(): # Lager funksjonen main
    table() # Kaller på funksjonen table
    postnummer() # Kaller på funksjonen pnummer
    kunder() # Kaller på funksjonen kunder
    info() # Kaller på funksjonen info


if __name__ == '__main__': # Sjekker om programmet kjøres
    main() # Kaller på funksjonen main