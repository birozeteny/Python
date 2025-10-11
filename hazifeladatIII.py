from collections import Counter, defaultdict

data_list_string_format = "Név;Életkor;Város Németh Kamilla;19;Debrecen Fekete Géza;18;Pécs Kovács Péter;27;Budapest Kiss Tibor;20;Debrecen Szabó Erzsébet;21;Budapest Szilágyi Ede;18;Pécs Agárdi Pál;26;Budapest Pálosi Richárd;23;Budapest Budai Máté;19;Debrecen Karácsony Antal;20;Budapest Aradi Márta;27;Pécs Piros Adél;29;Debrecen Bíró Zsolt;16;Budapest Szabados Attila;25;Debrecen Román Sarolta;24;Budapest Virág Bertalan;22;Pécs Varga Imre;18;Budapest Tóth Sándor;22;Debrecen Nagy Ibolya;23;Pécs Horváth Ferenc;17;Budapest Balogh Edina;26;Budapest"

records_raw = data_list_string_format.split(' ')[1:]
data_list = [
    record.split(';')
    for record in records_raw
    if len(record.split(';')) == 3
]

print("## 1. Adatlista (List Comprehension)")
print(data_list)

def print_data(data, show_name=True, show_age=True, show_city=True):
    header = []
    if show_name: header.append("Név")
    if show_age: header.append("Életkor")
    if show_city: header.append("Város")

    if not header: return


    print(f"\nFejléc: {', '.join(header)}")


   
    for row in data:
        output_row_values = []
        if show_name: output_row_values.append(row[0])
        if show_age: output_row_values.append(row[1])
        if show_city: output_row_values.append(row[2])

        print(f"{', '.join(output_row_values)}")


print("\n## 2. Kiírás (csak kor)")
print_data(data_list, show_name=False, show_city=False)

# 3. Lista szótárrá alakítása (dict comprehension)
data_dict_list = [
    {'nev': row[0], 'age': int(row[1]), 'city': row[2], 'other': []}
    for row in data_list
]
print("\n## 3. Szótár lista (Dict Comprehension)")
print(data_dict_list[:2])


# 4. Rendszerező és elemző függvények
def group_by_age(data):
    age_groups = defaultdict(list)
    for p in data:
        age = p['age']
        if 12 <= age <= 20:
            group = '12-20'
        elif 21 <= age <= 25:
            group = '21-25'
        elif 26 <= age <= 32:
            group = '26-32'
        else:
            group = '33+'
        age_groups[group].append(p['nev'])
    return dict(age_groups)


def format_name(full_name):
    parts = full_name.split(' ')
    if len(parts) >= 2:
        return f"{parts[0]} {parts[1][0]}."
    return full_name


# Rendszerezés és statisztikák
grouped_data = group_by_age(data_dict_list)
cities = [p['city'] for p in data_dict_list]
city_counts = Counter(cities)
most_common_city, count = city_counts.most_common(1)[0]
average_age = sum(p['age'] for p in data_dict_list) / len(data_dict_list)

print("\n## 4. Elemzés")


print("\n### Életkor Szerinti Rendszerezés:")
for group, people in grouped_data.items():
    print(f"**{group} évesek ({len(people)} fő):** {', '.join(people)}")


print("\n### Statisztikai Adatok:")
print(f"A **leggyakoribb város** a(z) **{most_common_city}** ({count} fő).")
print(f"Az adathalmaz **átlagéletkora**: **{average_age:.2f}** év.")

people_by_city = defaultdict(list)
for person in data_dict_list:
    people_by_city[person['city']].append(format_name(person['nev']))

print("\n### Azonos Városban Élők (Vezetéknév K. formátum):")
for city, people in people_by_city.items():
    if len(people) > 1:

        print(f"**{city}** lakói: {', '.join(people)}")
