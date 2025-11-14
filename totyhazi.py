import json
import os
from typing import List, Dict, Callable, Any


class JsonKezelo:

    def load_json(self, filename: str) -> Dict[str, Any]:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f'Hiba: A fájl ({filename}) nem található.')
            return {}
        except json.JSONDecodeError:
            print(f"Hiba: A fájl ({filename}) dekódolása sikertelen. Ellenőrizze a JSON formátumot.")
            return {}
        except Exception as e:
            print(f"Ismeretlen hiba a betöltés során: {e}")
            return {}

    def save_json(self, data: Dict[str, Any], filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            print(f'Adatok mentve a(z) {filename} fájlba.')
        except IOError as e:
            print(f'Hiba: Nem sikerült menteni a fájlt ({filename}). {e}')


class MeccsAnalyzator:

    def __init__(self, json_kezelo: JsonKezelo, filename: str = "adatok/data.json"):
        self.__json_kezelo = json_kezelo

        raw_data = self.__json_kezelo.load_json(filename)
        self.__osszes_meccs = raw_data.get("matches", [])
        self.__valid_meccsek = self.filter_invalid_matches(self.__osszes_meccs)

        if not self.__valid_meccsek:
            print("Nincs feldolgozható érvényes mérkőzés.")
            exit()

    def filter_invalid_matches(self, matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        valid_matches = []
        invalid_matches = []

        for match in matches:
            try:
                if 'score' not in match or 'ht' not in match['score']:
                    raise KeyError('Hiányzó "score" vagy "ht" kulcs.')
                valid_matches.append(match)
            except KeyError:
                invalid_matches.append(match)

        if invalid_matches:
            self.__json_kezelo.save_json({"invalid_matches": invalid_matches}, "hibas.json")
            print("Érvénytelen meccsek mentve a hibas.json fájlba.")

        return valid_matches

    def _process_matches(self, matches: List[Dict[str, Any]], condition: Callable[[Dict], bool], error_label: str) -> \
    List[Dict[str, Any]]:
        results = []
        for match in matches:
            try:
                if condition(match):
                    results.append(match)
            except KeyError as e:
                print(f'[{error_label}] - Hiba a meccs feldolgozásakor: Hiányzó kulcs {e} -> {match}')
                return []
        return results

    def home_losing_at_halftime_but_wins(self, matches: List[Dict]) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: (m["score"]["ht"][0] < m["score"]["ht"][1]) and (m["score"]["ft"][0] > m["score"]["ft"][1]),
            "Forditas_hiba"
        )

    def home_losing_at_halftime_but_draws(self, matches: List[Dict]) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: (m["score"]["ht"][0] < m["score"]["ht"][1]) and (m["score"]["ft"][0] == m["score"]["ft"][1]),
            "Dontetlen_hiba"
        )

    def home_concedes_more_than_three_goals(self, matches: List[Dict]) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: (m["score"]["ft"][1] > 3),
            "Sok_kapott_gol_hiba"
        )

    def home_score_more_than_three_goals(self, matches: List[Dict]) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: (m["score"]["ft"][0] > 3),
            "Sok_rugott_gol_hiba"
        )

    def filter_by_matchday(self, matches: List[Dict], matchday: str) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: m.get("round", "").lower() == f'matchday {matchday}'.lower(),
            "Fordulo_szures_hiba"
        )

    def filter_by_date(self, matches: List[Dict], date: str) -> List[Dict]:
        return self._process_matches(
            matches,
            lambda m: m.get("date") == date,
            "Datum_szures_hiba"
        )

    def get_valid_matches(self):
        return self.__valid_meccsek


class MenuVezerlo:

    def __init__(self, analyzator: MeccsAnalyzator):
        self.__analyzator = analyzator
        self.__valid_meccsek = analyzator.get_valid_matches()

    def _print_results(self, title: str, matches: List[Dict]):
        print("-" * 50)
        print(title)

        if matches:
            for match in matches:
                ht_score = match["score"].get("ht", "N/A")
                ft_score = match["score"].get("ft", "N/A")

                print(f'{match.get("round", "N/A")}: {match.get("team1", "N/A")} vs {match.get("team2", "N/A")}'
                      f' | Dátum: {match.get("date", "N/A")}, Félidő: {ht_score}'
                      f', Végeredmény: {ft_score}')
            print("-" * 50)
        else:
            print("Nincs találat.")
            print("-" * 50)

    def _run_analysis(self, matches_to_analyze: List[Dict]):

        halftime_loss_to_win = self.__analyzator.home_losing_at_halftime_but_wins(matches_to_analyze)
        halftime_loss_to_draw = self.__analyzator.home_losing_at_halftime_but_draws(matches_to_analyze)
        home_concede_3_or_more = self.__analyzator.home_concedes_more_than_three_goals(matches_to_analyze)
        home_score_3_or_more = self.__analyzator.home_score_more_than_three_goals(matches_to_analyze)

        self._print_results("1) Hazai félidőben vereségre áll, de fordít", halftime_loss_to_win)
        self._print_results("2) Hazai félidőben vereségre áll, de X lesz", halftime_loss_to_draw)
        self._print_results("3) Hazai 3 gólnál többet kap", home_concede_3_or_more)
        self._print_results("4) Hazai 3 gólnál többet rúg", home_score_3_or_more)

    def run(self):
        while True:
            options = [
                "1. Szűrés Forduló (Matchday) alapján",
                "2. Szűrés Dátum alapján",
                "3. Összes meccs elemzése (Nincs szűrés)",
                "end, q, quit - Kilépés"
            ]

            print("\nMenü:")
            for opt in options:
                print(opt)

            choice = input("Választás (1/2/3/q): ").lower()

            if choice in ["end", "q", "quit"]:
                print("\nViszlát!")
                break

            filtered_matches = []
            matches_to_analyze = self.__valid_meccsek

            if choice == "1":
                matchday = input("Add meg a fordulót (pl. 1): ")
                filtered_matches = self.__analyzator.filter_by_matchday(self.__valid_meccsek, matchday)
                matches_to_analyze = filtered_matches
            elif choice == "2":
                date = input("Add meg a dátumot (YYYY-MM-DD): ")
                filtered_matches = self.__analyzator.filter_by_date(self.__valid_meccsek, date)
                matches_to_analyze = filtered_matches
            elif choice == "3":
                print("--- Összes érvényes mérkőzés elemzése ---")
                matches_to_analyze = self.__valid_meccsek
            else:
                print("Érvénytelen választás. Kérem, válasszon 1, 2, 3 vagy q közül.")
                continue

            self._run_analysis(matches_to_analyze)


def main():
    json_kezelo = JsonKezelo()
    analyzator = MeccsAnalyzator(json_kezelo)
    menu_vezerlo = MenuVezerlo(analyzator)
    menu_vezerlo.run()


if __name__ == "__main__":
    main()