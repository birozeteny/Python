import random
import sys

# A szótár elkészítése (1. és 2. feladat)
fogalmak = ['majorság', 'hűbéres', 'jobbágy', 'nemes', 'tized', 'kilenced', 'robot',
            'szügyhám', 'vetésforgó', 'ugar', 'lovag']

meghatarozasok = ['Egy-egy nagybirtok vagy valamely részének igazgatási központja.',
                  'Aki örökletes használatra megkapja a földet.',
                  'Telkes paraszt, aki a földesúrtól kapott földön gazdálkodik.',
                  'Kiváltságos réteg.',
                  'Egyházi adó.',
                  'Földesúrnak beszolgáltatott adó.',
                  'Ötvenkét igás, vagy 104 kézimunka nap kötelezettség.',
                  'Igavonási találmány, melynek köszönhetően nem az állat nyakában van a húzó eszköz.',
                  'A termőföld használata évszakonként más és más.',
                  'Művelés alá nem vont terület.',
                  'Vagyonos katonai szolgálattevő lóval, páncéllal.']

szotar = {
    fogalom: meghatarozas
    for fogalom, meghatarozas in zip(fogalmak, meghatarozasok)
}

# 3. feladat (a véletlen elem kiírását eltávolítottam a fő kvíz elől, ha nem kérik külön,
#            mert zavarja a kvíz formátumát)

# A kvíz logika és segédfüggvények
helyes_valaszok = 0
helytelen_valaszok = 0
osszes_kerdes = len(szotar)
kviz_eredmenyek = []

# Kevert kulcslista, hogy mindenre rákérdezzünk egyszer (7. pont)
kerdesek_listaja = list(szotar.keys())
random.shuffle(kerdesek_listaja)


def ellenoriz_kilepest(valasz):
    tisztitott_valasz = valasz.strip().upper()
    return tisztitott_valasz in ["END", "Q", "QUIT"]


def kiir_statisztika(helyes, helytelen):
    osszes_valasz = helyes + helytelen
    if osszes_valasz == 0:
        return  # Nem ír ki semmit, ha nincs válasz

    szazalek = (helyes / osszes_valasz) * 100

    # Képen látható kiírás:
    print(f"\nA program írja ki, hány helyes és hány helytelen választ adott, százalékosan is tegye ezt meg.")
    print(f"Helyes válaszok száma: {helyes}")
    print(f"Helytelen válaszok száma: {helytelen}")
    print(f"Teljesítmény: {szazalek:.2f}%")


def file_kiiras(adatok, fajlnev="kviz_eredmenyek.txt"):
    try:
        with open(fajlnev, 'w', encoding='utf-8') as f:
            f.write("--- Kvíz eredmények ---\n")
            for item in adatok:
                f.write(f"\nKérdés: {item['kerdes']}\n")
                f.write(f"Felhasználó válasza: {item['felhasznalo_valasz']}\n")
                f.write(f"Helyes válasz: {item['helyes_valasz']}\n")
                f.write(f"Eredmény: {item['eredmeny']}\n")
        print(f"\n Eredmények sikeresen kiírva a '{fajlnev}' fájlba.")
    except Exception as e:
        print(f"\n Hiba történt a fájlba írás során: {e}")


# Fő kvíz ciklus (4., 5., 6., 7., 8. feladat)
print("Középkori történelem fogalmakat kérdezünk ki.")

for fogalom in kerdesek_listaja:
    meghatarozas = szotar[fogalom]

    # A képen lévő minta szerint a kérdés ismétlődik minden kérdés előtt
    print("\nKözépkori történelem fogalmakat kérdezünk ki.")
    print("Milyen fogalmat ír le az alábbi meghatározás:")
    print(f"{meghatarozas}")

    felhasznalo_valasz = input("Mi a fogalom: ")

    if ellenoriz_kilepest(felhasznalo_valasz):
        # Kilépés (8. pont)
        kiir_statisztika(helyes_valaszok, helytelen_valaszok)
        break

    # Válasz tisztítása (6. pont)
    tisztitott_valasz = felhasznalo_valasz.strip().lower()
    helyes_fogalom_tisztitva = fogalom.lower()

    eredmeny = ""
    if tisztitott_valasz == helyes_fogalom_tisztitva:
        # Helyes válasz (5. pont)
        print("Helyes válasz!")
        helyes_valaszok += 1
        eredmeny = "Helyes"
    else:
        # Rossz válasz (5. pont)
        print(f"Rossz válasz. Helyesen: {fogalom}")
        helytelen_valaszok += 1
        eredmeny = "Helytelen"

    # Eredmények gyűjtése a fájlba íráshoz (9. pont)
    kviz_eredmenyek.append({
        "kerdes": meghatarozas,
        "felhasznalo_valasz": felhasznalo_valasz,
        "helyes_valasz": fogalom,
        "eredmeny": eredmeny
    })

# Ha a ciklus végigfutott és nem kilépéssel fejeződött be, de van válasz
if len(kviz_eredmenyek) == osszes_kerdes:
    kiir_statisztika(helyes_valaszok, helytelen_valaszok)

# Fájlba írás (9. feladat)
if kviz_eredmenyek:
    file_kiiras(kviz_eredmenyek)