class_a_range = (1, 126)
class_b_range = (128, 191)
class_c_range = (192, 223)
class_d_range = (224, 239)
class_e_range = (240, 255)

class_a_description = "Nagy hálózatok"
class_b_description = "Közepes hálózatok"
class_c_description = "Kis hálózatok"
class_d_description = "Multicast hálózatok"
class_e_description = "Kísérleti hálózatok"

ip_ranges = [class_a_range, class_b_range, class_c_range, class_d_range, class_e_range]
descriptions = [class_a_description, class_b_description, class_c_description, class_d_description, class_e_description]
class_labels = ["A", "B", "C", "D", "E"]

ip_classes = {
    class_label: {
        "range": ip_range,
        "description": description
    }
    for class_label, ip_range, description in zip(class_labels, ip_ranges, descriptions)
}
print(ip_classes)
print("Egy IP cím osztályát állapítjuk meg.")
full_ip = input("Adj meg egy teljes IP címet (x.x.x.x/x): ")

first_octet_str = full_ip.split('.')[0]
first_octet = int(first_octet_str)

found_class = "Speciális/Nem besorolt"

for label, data in ip_classes.items():
    min_val, max_val = data["range"]

    if min_val <= first_octet <= max_val:
        found_class = label
        break

print(f"A megadott IP cím osztálya: {found_class}")