
import numpy as np
from faker import Faker
import pandas as pd
from sampler import sampler
names = Faker('no_NO')


class Person:
    def __init__(self, age, sex, work, student, family_name=None, partner=None):
        self.age = age
        self.sex = sex
        self.work = work
        self.student = student
        self.marital_status = "single"
        self.family_name = family_name if family_name else names.last_name()
        self.first_name = names.first_name_male() if self.sex == 1 else names.first_name_female()
        self.partner = partner
        self.children = []
        self.parents = []

    def set_partner(self, partner, is_married=False):
        self.partner = partner
        partner.partner = self
        if is_married:
            self.marital_status = partner.marital_status = "married"
            if self.sex != partner.sex:  
                male_partner = self if self.sex == 1 else partner
                self.family_name = partner.family_name = male_partner.family_name
            else: 
                chosen_family_name = np.random.choice([self.family_name, partner.family_name])
                self.family_name = partner.family_name = chosen_family_name

    def add_child(self, child):
        self.children.append(child)
        child.parents.append(self)
        if self.partner:
            self.partner.children.append(child)
            child.parents.append(self.partner)

    def __str__(self):
        return f"{self.first_name} {self.family_name} ({'M' if self.sex == 1 else 'F'}, {self.age})"

class ExtendedFamily:
    def __init__(self, family_name):
        self.family_name = family_name
        self.families = []

    def add_family(self, family):
        self.families.append(family)


class Family:
    def __init__(self, extended_family):
        self.members = []
        self.address = None
        self.children_limit = 5
        self.extended_family = extended_family

    def add_member(self, person):
        if not any(m.age >= 18 for m in self.members):
            self.family_name = person.family_name
        self.members.append(person)

    def can_add_child(self):
        return len([member for member in self.members if member.age < 18]) < self.children_limit

    def set_address(self, address):
        self.address = address

    def __str__(self):
        member_descriptions = ', '.join(str(member) for member in self.members)
        address_description = f" at {self.address}" if self.address else ""
        return f"Family {self.family_name}. With members: {member_descriptions}{address_description} \n"


def create_families_from_persons(persons):
    families = []
    family = Family()
    possible_grand_parents = [p for p in persons if p.age>55]
    possible_parents = []
    return possible_grand_parents


    # for person in persons:
    #     family.add_member(person)
    #     if len([p for p in family.members if p.age > 18]) >= 2:
    #         families.append(family)
    #         family = Family()
    # if family.members:
    #     families.append(family)
    # return families

if __name__ == "__main__":
    N = 10
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex": sampler.sample_sex(N),
        "work": sampler.sample_work(ages),
        "student": sampler.sample_student(ages),
    }

persons = [Person(age=data['age'][i], sex=data['sex'][i], work=data['work'][i],student= data['student'][i]) for i in range(len(data['age']))]
families = create_families_from_persons(persons=persons)

for f in families:
    print(f)