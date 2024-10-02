import csv
from pathlib import Path
csv_path = Path("data/csv")

def export_persons_to_csv(persons):
    with open(csv_path / 'persons.csv', 'w', newline='') as file:
        fieldnames = ['personal_number', 'first_name', 'family_name', 'age', 'sex', 'occupation', 'activity', 'partner_personal_number', 'family_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for person in persons:
            writer.writerow({
                'personal_number': person.personal_number,
                'first_name': person.first_name,
                'family_name': person.family_name,
                'age': person.age,
                'sex': person.sex,
                'occupation': person.occupation,
                'activity': person.activity,
                'partner_personal_number': person.partner.personal_number if person.partner else None,
                'family_id': person.family_id,

            })

def export_families_to_csv(families):
    with open(csv_path / 'families.csv', 'w', newline='') as file:
        fieldnames = ['family_id', 'family member']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for family in families:
            for member in family.family_members:
                writer.writerow({
                    'family_id': family.id,
                    'family member': member.personal_number
                })

def export_households_to_csv(households):
    with open(csv_path / 'households.csv', 'w', newline='') as file:
        fieldnames = ['household_id', 'address']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for household in households:
            writer.writerow({
                'household_id': household.id,
                'address': household.address,
            })

def export_household_members_to_csv(households):
    with open(csv_path / 'household_members.csv', 'w', newline='') as file:
        fieldnames = ['household_id', 'personal_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for household in households:
            for member in household.members:
                writer.writerow({
                    'household_id': household.id,
                    'personal_number': member.personal_number
                })      

def export_parent_child_to_csv(persons):
    with open(csv_path / 'csvparent_child.csv', 'w', newline='') as file:
        fieldnames = ['parent_personal_number', 'child_personal_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for person in persons:
            for child in person.children:
                writer.writerow({
                    'parent_personal_number': person.personal_number,
                    'child_personal_number': child.personal_number
                })

def write_to_csv(persons,families,households):
    export_persons_to_csv(persons)
    export_families_to_csv(families)
    export_households_to_csv(households)
    export_household_members_to_csv(households)
    export_parent_child_to_csv(persons)
