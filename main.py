from pprint import pprint
import csv
import re


def pars_contact(contact_list):

    pattern_number = r"(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})"
    pattern_ext_number = r"\s*\(*(доб.)\s*(\d*)\)*\s*"
    pattern_name = r"(^([А-я]+)\s([А-я]+)\s([А-я]+)\,\,)|(^([А-я]+)\,([А-я]+)\,([А-я]+))|(^([А-я]+)\s([А-я]+)(\,)\,)|(^([А-я]+)\,([А-я]+)\s([А-я]+)\,)"

    str_line = ','.join(contact_list)
    str_line = re.sub(pattern_name, r"\2\6\14\10,\3\7\11\15,\4\8\16", str_line)
    str_line = re.sub(pattern_number, r"+7(\2)\3-\4-\5", str_line)
    str_line = re.sub(pattern_ext_number, r" \1\2", str_line)
    return str_line.split(',')


with open("phonebook_raw.csv", encoding="UTF8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


# upl - update_contacts_list
upl = []
for contact in contacts_list:
    upl.append(pars_contact(contact))
out_contacts_list = []
contacts_list_length = len(upl)
pass_records = []

for i in range(contacts_list_length - 1):
    if i in pass_records:
        continue
    contact = upl[i]  # если встречается более 2 раз
    for j in range(i + 1, len(upl)):
        if contact[0] == upl[j][0] and contact[1] == upl[j][1]:
            pass_records.append(j)
            contact = [contact[_] if contact[_] != "" else upl[j][_]
                       for _ in range(len(contact))]
    out_contacts_list.append(contact)

# код для записи файла CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(out_contacts_list)
