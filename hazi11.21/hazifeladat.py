import json
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, List, Tuple


class Motor:
    def __init__(self, tipus: str):
        self.tipus = tipus

    def __repr__(self):
        return f"Motor(tipus='{self.tipus}')"


class Jarmu(ABC):
    def __init__(self, gyarto: str, evjarat: int, szin: str, motor_tipus: str):
        self.gyarto = gyarto
        self.evjarat = evjarat
        self.szin = szin
        self.motor = Motor(motor_tipus)

    @abstractmethod
    def specifikaciok(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data['motor'] = self.motor.__dict__
        data['tipus'] = self.__class__.__name__
        return data


class Szemelygepkocsi(Jarmu):
    def __init__(self, gyarto: str, evjarat: int, szin: str, motor_tipus: str, ajtok_szama: int):
        super().__init__(gyarto, evjarat, szin, motor_tipus)
        self.ajtok_szama = ajtok_szama

    def specifikaciok(self):
        return f"Személygépkocsi: {self.gyarto}, Évjárat: {self.evjarat}, Ajtók: {self.ajtok_szama}"

    def __repr__(self):
        return f"Szemelygepkocsi(gyarto='{self.gyarto}', evjarat={self.evjarat}, ajtok_szama={self.ajtok_szama}, szin='{self.szin}')"


class Teherauto(Jarmu):
    def __init__(self, gyarto: str, evjarat: int, szin: str, motor_tipus: str, teherbiras_kg: float):
        super().__init__(gyarto, evjarat, szin, motor_tipus)
        self.teherbiras_kg = teherbiras_kg

    def specifikaciok(self):
        return f"Teherautó: {self.gyarto}, Évjárat: {self.evjarat}, Teherbírás: {self.teherbiras_kg} kg"

    def __repr__(self):
        return f"Teherauto(gyarto='{self.gyarto}', evjarat={self.evjarat}, teherbiras_kg={self.teherbiras_kg}, szin='{self.szin}')"


class Fajlkezelo:
    def __init__(self, fajlnev: str):
        self.fajlnev = fajlnev

    def betoltes(self) -> List[Jarmu]:
        jarmu_lista = []
        try:
            with open(self.fajlnev, 'r', encoding='utf-8') as f:
                adatok = json.load(f)
                for adat in adatok:
                    tipus = adat.pop('tipus')
                    motor_adat = adat.pop('motor')

                    if tipus == 'Szemelygepkocsi':
                        jarmu = Szemelygepkocsi(motor_tipus=motor_adat['tipus'], **adat)
                    elif tipus == 'Teherauto':
                        jarmu = Teherauto(motor_tipus=motor_adat['tipus'], **adat)
                    else:
                        continue
                    jarmu_lista.append(jarmu)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return jarmu_lista

    def mentes(self, jarmuvek: List[Jarmu]):
        adatok = [j.to_dict() for j in jarmuvek]
        with open(self.fajlnev, 'w', encoding='utf-8') as f:
            json.dump(adatok, f, indent=4, ensure_ascii=False)


class Autopark:
    def __init__(self, fajlnev: str):
        self.fajlkezelo = Fajlkezelo(fajlnev)
        self.jarmuvek: List[Jarmu] = self.fajlkezelo.betoltes()
        print(f"Az Autópark {len(self.jarmuvek)} járművel indult.")

    def jarmu_hozzaadasa(self, jarmu: Jarmu):
        self.jarmuvek.append(jarmu)
        self._allapot_mentese()

    def jarmu_eltavolitasa(self, index: int) -> bool:
        try:
            self.jarmuvek.pop(index)
            self._allapot_mentese()
            return True
        except IndexError:
            return False

    def osszes_jarmu_lekerdezese(self) -> List[Jarmu]:
        return self.jarmuvek

    def _allapot_mentese(self):
        self.fajlkezelo.mentes(self.jarmuvek)

    def listazas(self):
        print("\n--- Autópark Járművei ---")
        if not self.jarmuvek:
            print("Az autópark üres.")
            return

        for i, jarmu in enumerate(self.jarmuvek):
            print(f"[{i}] {jarmu!r}")



class DataProcess:
    def __init__(self, autopark: Autopark):
        self.autopark = autopark

    def szures_feltetel_alapjan(self, feltetel: Callable[[Jarmu], bool]) -> List[Jarmu]:
        return [j for j in self.autopark.osszes_jarmu_lekerdezese() if feltetel(j)]

    def eldontes_megfeleles(self, feltetel: Callable[[Jarmu], bool]) -> bool:
        van_megfelelo = any(feltetel(j) for j in self.autopark.osszes_jarmu_lekerdezese())
        if van_megfelelo:
            print("OK.")
        else:
            print("Nincs megfelelő jármű.")
        return van_megfelelo

    def szetvalogatas(self, feltetel: Callable[[Jarmu], bool]) -> Tuple[List[Jarmu], List[Jarmu]]:
        megfelelo_lista = []
        nem_megfelelo_lista = []

        for jarmu in self.autopark.osszes_jarmu_lekerdezese():
            if feltetel(jarmu):
                megfelelo_lista.append(jarmu)
            else:
                nem_megfelelo_lista.append(jarmu)

        return megfelelo_lista, nem_megfelelo_lista


if __name__ == "__main__":
    FAJL_NEV = "autopark_adatok.json"

    park = Autopark(FAJL_NEV)

    uj_szemely_gepkocsi = Szemelygepkocsi(
        gyarto="Toyota", evjarat=2024, szin="piros", motor_tipus="Benzin", ajtok_szama=5
    )
    uj_teherauto = Teherauto(
        gyarto="MAN", evjarat=2021, szin="fehér", motor_tipus="Dízel", teherbiras_kg=7500.0
    )

    park.jarmu_hozzaadasa(uj_szemely_gepkocsi)
    park.jarmu_hozzaadasa(uj_teherauto)

    park.listazas()

    dp = DataProcess(park)

    piros_feltetel = lambda j: j.szin.lower() == 'piros'
    piros_jarmuvek = dp.szures_feltetel_alapjan(piros_feltetel)

    for j in piros_jarmuvek:
        print(f"Szűrt piros jármű: {j.gyarto}")

    teherauto_feltetel = lambda j: isinstance(j, Teherauto)
    dp.eldontes_megfeleles(teherauto_feltetel)

    modern_feltetel = lambda j: j.evjarat > 2022
    modern_jarmuvek, regi_jarmuvek = dp.szetvalogatas(modern_feltetel)
    print(f"Modern járművek: {[j.gyarto for j in modern_jarmuvek]}")
    print(f"Régi járművek: {[j.gyarto for j in regi_jarmuvek]}")

    if len(park.osszes_jarmu_lekerdezese()) > 0:
        park.jarmu_eltavolitasa(0)

    park.listazas()
