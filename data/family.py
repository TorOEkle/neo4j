import numpy as np
from sampler import sampler
from faker import Faker
import pandas as pd
names = Faker('no_NO')

class Person:
    def __init__(self, age, sex, work, student, family_name=None):
        self.age = age
        self.sex = sex
        self.work = work
        self.student = student
        self.family_name = family_name
        self.first_name = names.first_name_male() if self.sex == 1 else names.first_name_female() 

    def __str__(self):
        return f"{self.first_name} {self.family_name}" if self.family_name else self.first_name

class Family:
    def __init__(self):
        self.members = []
        self.address = None
        self.family_name = names.last_name()

    def add_member(self, person):
        person.family_name = self.family_name
        self.members.append(person)

    def give_family_name(self):
        for person in self.members:
            person.family_name = self.family_name

    def set_address(self, address):
        self.address = address

    def __str__(self):
        member_descriptions = ', '.join(str(member) for member in self.members)
        address_description = f" at {self.address}" if self.address else ""
        return f"Family {self.family_name} with members: {member_descriptions}{address_description}"

def create_and_assign_families(data, household_data, house_addresses, apartment_addresses):
    persons = [Person(data['age'][i], data['sex'][i], data['work'][i], data['student'][i]) for i in range(len(data['age']))]

    if isinstance(house_addresses, pd.DataFrame):
        house_addresses = house_addresses['adressenavn'].tolist() 

    if isinstance(apartment_addresses, pd.DataFrame):
        apartment_addresses = apartment_addresses['kommune_adresse'].tolist()

    households = []
    for i in range(len(household_data['type'])):
        house_type = household_data['type'][i]
        # Assign an address based on house type
        if house_type == 'house':
            address = np.random.choice(house_addresses)
        else:
            address = np.random.choice(apartment_addresses)

        house = {
            'type': house_type,
            'share': household_data['share'][i],
            'rooms': household_data['rooms'][i],
            'bathrooms': household_data['bathrooms'][i],
            'size': household_data['size'][i],
            'lot_size': household_data['lot_size'][i],
            'build_year': household_data['build_year'][i],
            'people': household_data['people'][i],
            'address': address
        }
        households.append(house)

    # Create and assign families to houses
    families = []
    family = Family()
    for person in persons:
        family.add_member(person)
        if len([p for p in family.members if p.age > 18]) >= 2:
            families.append(family)
            family = Family()

    if family.members:
        families.append(family)

    for family in families:
        suitable_house = next((house for house in households if len(family.members) <= house['people']), None)
        if suitable_house:
            family.set_address(suitable_house['address'])
            households.remove(suitable_house)  # Remove the assigned house

    return families

if __name__ == "__main__":
    N = 5
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex": sampler.sample_sex(N),
        "work": sampler.sample_work(ages),
        "student": sampler.sample_student(ages),
    }

    # Generate addresses
    house_addresses = sampler._house_address()
    apartment_addresses = sampler._apartment_address()

    # Generate households
    household_data = sampler.sample_household(N)

    # Create and assign families
    families = create_and_assign_families(data, household_data, house_addresses, apartment_addresses)

    for family in families:
        print(family)