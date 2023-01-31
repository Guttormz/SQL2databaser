import sqlite3 as sq
from tqdm import tqdm # pip install tqdm
import csv
import pandas as pd # pip install pandas

conn = sq.connect('kunde.db') # Lager en database
cur = conn.cursor() # Lager en cursor


def table():

    if cur.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='post'"): # Sjekker om tabellen post eksisterer
        try:
            cur.execute("DROP TABLE post") # Prøver å slette tabellen post
        except:
           sq.OperationalError # Hvis tabellen ikke eksisterer, så får vi en feilmelding. Da hopper den til neste linje

    cur.execute('CREATE TABLE IF NOT EXISTS post (\
                    postnummer      TEXT PRIMARY KEY,\
                    Poststed      TEXT    NOT NULL, \
                    Kommunenr TEXT NOT NULL, \
                    Kommunenavn TEXT NOT NULL,\
                    kategori TEXT NOT NULL);') # Lager tabellen post hvor postnummer er primærnøkkel

    if cur.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name='kunder'"): # Sjekker om tabellen kunder eksisterer
        try:
            cur.execute("DROP TABLE kunder") # Prøver å slette tabellen kunder
        except:
            sq.OperationalError # Hvis tabellen ikke eksisterer, så får vi en feilmelding. Da hopper den til neste linje
            
    cur.execute('CREATE TABLE IF NOT EXISTS kunder (\
                    Kundenr    INTEGER PRIMARY KEY AUTOINCREMENT,\
                    fnavn      TEXT    NOT NULL,\
                    enavn      TEXT    NOT NULL,\
                    epost      TEXT    NOT NULL,\
                    tlf        TEXT    ,\
                    postnummer TEXT NOT NULL,\
                    FOREIGN    KEY (postnummer) REFERENCES postnummer (post));') # Lager tabellen kunder hvor kundenr er primænøkkel og postnummer er en fremmednøkkel til postnummer på post tabellen

def postnummer():
    with open('postnummerregister.csv', 'r') as f: # Åpner filen postnummerregister.csv i read
        reader = csv.reader(f) # Leser filen
        next(reader) # Hopper over første linje
        for row in tqdm(reader, total=5139): # Går gjennom hver linje i filen, og lager en progressbar
            cur.execute('INSERT INTO post (postnummer, Poststed, Kommunenr, Kommunenavn, kategori) VALUES (?,?,?,?,?)', row,) # Legger til hver linje i tabellen post
    print("Informasjon hentet om postnummer") # Sier ifra at informasjonen er hentet

    conn.commit() # Committer endringene

def kunder():
    with open('randoms.csv', 'r') as f: # Åpner filen randoms.csv i read
        reader = csv.reader(f) # Leser filen
        next(reader) # Hopper over første linje
        for line in tqdm(reader, total=200): # Går gjennom hver linje i filen, og lager en progressbar
            cur.execute('INSERT INTO kunder (fnavn, enavn, epost, tlf, postnummer) VALUES (?,?,?,?,?)', line,) # Legger til hver linje i tabellen kunder
    print("Informasjon hentet om kunder") # Sier ifra at informasjonen er hentet

    conn.commit() # Committer endringene

def info():
    svar=(input("Vil du se info om kunder? (Ja/Nei): ")) # Spør brukeren om han vil se info om kunder
    if svar == "Ja" or svar == "ja" or svar == "j" or svar == "J": # Hvis brukeren svarer ja, så kjører vi funksjonen find()
        find()

    if svar == "Nei" or svar == "nei" or svar == "n" or svar == "N": # Hvis brukeren svarer nei, så avslutter vi programmet
        print("Ok, da avslutter vi programmet.") # Sier ifra at programmet avsluttes
        exit()

def find():
    knr=int(input("Hvilken kunde vil du se info om? (Kundenr): ")) # Spør brukeren om hvilken kunde han vil se info om
    if knr>200: # Hvis brukeren skriver et nummer som er høyere enn antall kunder, så får han en feilmelding
        print("Vi har ikke så mange kunder, prøv et lavere nummer. (Maks 200 kunder)") # Sier ifra at vi ikke har så mange kunder
        find()

    if knr<1: # Hvis brukeren skriver et nummer som er lavere enn 1, så får han en feilmelding
        print("Dette tallet er for lavt, prøv et høyere nummer. (Minst 2)") # Sier ifra at tallet er for lavt
        find()

    resultat=cur.execute("SELECT kunder.kundenr, Kunder.fnavn, Kunder.enavn, Kunder.epost, Kunder.tlf, Kunder.postnummer, post.postnummer, post.poststed, post.kommunenr, post.kommunenavn, post.kategori FROM post INNER JOIN Kunder ON Kunder.[postnummer] = post.[postnummer] WHERE Kunder.kundenr = ?",(knr,)) # Henter info om kunden fra tabellene kunder og post
    print(resultat.fetchall()) # Printer ut info om kunden
    if resultat.fetchall() == (""):
        print("Denne kunden har ikke ett gyldig postnummer")

    info() # Kjører funksjonen info() igjen

def main():
    table()
    postnummer()
    kunder()
    info()


if __name__ == '__main__':
    main()