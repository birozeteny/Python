import random
import datetime
import os


class IdojarasAdat:

    def __init__(self, datum, idojaras, homerseklet, varhato_eso):
        self.datum = datum
        self.idojaras = idojaras
        self.homerseklet = homerseklet
        self.varhato_eso = varhato_eso

    def get_datum_str(self):
        return self.datum.strftime('%Y-%m-%d')


class AdatFeldolgozo:
    FILE_NAME = "idojaras_adatok.txt"
    START_DATE = datetime.date(2024, 12, 1)
    END_DATE = datetime.date(2025, 11, 24)
    WEATHER_OPTIONS = ["szeles", "napos", "esős", "ködös", "semillen"]
    MIN_TEMP = 0.0
    MAX_TEMP = 20.0
    MIN_RAIN = 0
    MAX_RAIN = 100

    def __init__(self):
        self.__adatok = {}
        self._generate_if_not_exists()
        self._load_data()

    def _get_date_range(self):
        dates = []
        current_date = self.START_DATE
        while current_date <= self.END_DATE:
            dates.append(current_date)
            current_date += datetime.timedelta(days=1)
        return dates

    def _generate_if_not_exists(self):
        if os.path.exists(self.FILE_NAME):
            return

        random.seed(42)

        print("Időjárás adatok generálása...")
        dates = self._get_date_range()

        try:
            with open(self.FILE_NAME, 'w', encoding='utf-8') as f:
                for date in dates:
                    weather = random.choice(self.WEATHER_OPTIONS)
                    temperature = round(random.uniform(self.MIN_TEMP, self.MAX_TEMP), 1)
                    rain_chance = random.randint(self.MIN_RAIN, self.MAX_RAIN)

                    data = [
                        f"Dátum: {date.strftime('%Y-%m-%d')}",
                        f"Időjárás: {weather}",
                        f"Hőmérséklet: {temperature:.1f}C",
                        f"Várható eső: {rain_chance}%"
                    ]
                    f.write('\n'.join(data) + '\n')

            print(f"Adatok generálása befejeződött, mentve a **{self.FILE_NAME}** fájlba.")
        except Exception as e:
            print(f"Hiba a fájlba írás közben: {e}")

    def _load_data(self):
        if not os.path.exists(self.FILE_NAME):
            print(f"Hiba: A fájl ({self.FILE_NAME}) nem található.")
            return

        print(f"Adatok beolvasása a(z) **{self.FILE_NAME}** fájlból...")
        try:
            with open(self.FILE_NAME, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i in range(0, len(lines), 4):
                if i + 3 >= len(lines):
                    break

                date_str = lines[i].strip().split(': ')[1]
                weather = lines[i + 1].strip().split(': ')[1]
                temperature = float(lines[i + 2].strip().split(': ')[1].replace('C', '').replace(',', '.'))
                rain_chance = int(lines[i + 3].strip().split(': ')[1].replace('%', ''))

                datum_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                adat_obj = IdojarasAdat(datum_obj, weather, temperature, rain_chance)
                self.__adatok[date_str] = adat_obj

            print("Adatok beolvasva és objektumokká töltve.")
        except Exception as e:
            print(f"Súlyos hiba az adatok beolvasása/konvertálása során: {e}")
            self.__adatok = {}

    def get_data(self):
        return self.__adatok

    def get_napi_jelentes(self, datum_str):
        return self.__adatok.get(datum_str)

    def get_havi_jelentes(self, year, month):
        prefix = f"{year}-{month:02d}"
        return {
            date_str: obj for date_str, obj in self.__adatok.items()
            if date_str.startswith(prefix)
        }

    def get_intervallum_adatok(self, start_date, end_date):
        data_list = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in self.__adatok:
                data_list.append(self.__adatok[date_str])
            current_date += datetime.timedelta(days=1)
        return data_list

    @staticmethod
    def calculate_stats(data_list):
        if not data_list:
            return None

        temperatures = [data.homerseklet for data in data_list]
        weather_counts = {}

        for data in data_list:
            weather = data.idojaras
            weather_counts[weather] = weather_counts.get(weather, 0) + 1

        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        rainy_days = weather_counts.get("esős", 0)
        semillen_days = weather_counts.get("semillen", 0)

        return {
            "napok_szama": len(data_list),
            "atlag_homerseklet": avg_temp,
            "max_homerseklet": max_temp,
            "esos_napok": rainy_days,
            "semillen_napok": semillen_days,
            "osszes_idojaras": weather_counts
        }


class MenuVezerlo:

    def __init__(self):
        self.adat_feldolgozo = AdatFeldolgozo()
        if not self.adat_feldolgozo.get_data():
            print("\nNincs adat a feldolgozáshoz. Program leáll.")
            exit()

    @staticmethod
    def _safe_input(prompt, data_type=str):
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input.lower() in ['q', 'quit', 'end']:
                    return "QUIT"

                if data_type == datetime.date:
                    return datetime.datetime.strptime(user_input, "%Y-%m-%d").date()

                if data_type == int:
                    return int(user_input)

                if data_type == str and user_input.lower() in ['nap', 'hónap', 'honap']:
                    return user_input.lower().replace('honap', 'hónap')

                return user_input

            except ValueError:
                print("\nHelytelen formátum! Kérjük, próbálja újra.")
            except Exception as e:
                print(f"\nIsmeretlen hiba történt: {e}")
                return "ERROR"

    def _display_napi_report(self):
        date_input = self._safe_input("Add meg a dátumot (YYYY-MM-DD): ", datetime.date)
        if date_input in ["QUIT", "ERROR"]: return

        datum_str = date_input.strftime("%Y-%m-%d")
        adat = self.adat_feldolgozo.get_napi_jelentes(datum_str)

        if adat:
            print(f"\nIdőjárás {datum_str} napján:")
            print(f"Időjárás: {adat.idojaras}")
            print(f"Hőmérséklet: {adat.homerseklet:.1f}C")
            print(f"Várható eső: {adat.varhato_eso}%")
        else:
            print(f"\nNincs adat a megadott dátumra: **{datum_str}**.")

    def _display_havi_report(self):
        date_input = self._safe_input("Add meg a hónapot (YYYY-MM): ")
        if date_input in ["QUIT", "ERROR"]: return

        try:
            year, month = map(int, date_input.split('-'))
        except ValueError:
            print("\nHelytelen YYYY-MM formátum.")
            return

        if not (1 <= month <= 12):
            print("\nHelytelen hónap szám (1-12).")
            return

        monthly_data = self.adat_feldolgozo.get_havi_jelentes(year, month)

        if not monthly_data:
            print(f"\nNincs adat a megadott hónapra: **{date_input}**.")
            return

        print(f"\nIdőjárás jelentés a {date_input} hónapra:")

        for date_str in sorted(monthly_data.keys()):
            data_obj = monthly_data[date_str]
            print(f"{date_str}: {data_obj.idojaras}, {data_obj.homerseklet:.1f}C, eső: {data_obj.varhato_eso}%")

    def _display_stats(self):
        start_date = self._safe_input("Add meg a kezdő dátumot (YYYY-MM-DD): ", datetime.date)
        if start_date in ["QUIT", "ERROR"]: return

        end_date = self._safe_input("Add meg a végdátumot (YYYY-MM-DD): ", datetime.date)
        if end_date in ["QUIT", "ERROR"]: return

        if start_date > end_date:
            print("\nHiba: A kezdő dátum nem lehet későbbi, mint a végdátum.")
            return

        data_in_range = self.adat_feldolgozo.get_intervallum_adatok(start_date, end_date)

        if not data_in_range:
            print("\nA megadott intervallumban nincs elérhető időjárási adat.")
            return

        stats = AdatFeldolgozo.calculate_stats(data_in_range)

        if stats:
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")

            print(f"\nStatisztika {start_str} és {end_str} között:")
            print(f"Átlaghőmérséklet: {stats['atlag_homerseklet']:.2f}C")
            print(f"Maximális hőmérséklet: {stats['max_homerseklet']:.1f}C")
            print(f"Esős napok száma: {stats['esos_napok']}")
            print(f"Semillen napok száma: {stats['semillen_napok']}")

    def run(self):
        while True:
            print("\nMenü:")
            print("1. Napi/havi jelentés")
            print("2. Két időpont közötti statisztika")
            print("3. Kilépés (end/q/quit)")

            choice = self._safe_input("Választás: ")

            if choice == "QUIT" or choice.lower() in ['3', 'end', 'q', 'quit']:
                print("\nViszlát!")
                break

            if choice == "1":
                self._menu_report_sub()
            elif choice == "2":
                self._display_stats()
            elif choice == "ERROR":
                pass
            else:
                print("\nÉrvénytelen menüpont. Kérem, válasszon 1, 2 vagy 3 közül.")

    def _menu_report_sub(self):

        choice = self._safe_input("Napra vagy hónapra keresel? (nap/hónap): ", str)

        if choice in ["QUIT", "ERROR"]:
            return

        if choice == "nap":
            self._display_napi_report()

        elif choice == "hónap":
            self._display_havi_report()
        else:
            print("\nÉrvénytelen választás. Kérjük, válasszon 'nap' vagy 'hónap' közül.")


def main():
    menu_vezerlo = MenuVezerlo()
    menu_vezerlo.run()


if __name__ == "__main__":
    main()