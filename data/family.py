import numpy as np
from faker import Faker
import pandas as pd
from sampler import sampler
from typing import List
import random

np.random.seed(42)
names = Faker('no_NO')

class Person:
    def __init__(self, age, sex, work, family_name=None):
        self.age = age
        self.sex = "Male" if sex == 1 else "Female"
        self.occupation = "work" if work ==1 else "Student"
        self.marital_status = "single"
        self.family_name = family_name if family_name else names.last_name()
        self.first_name = names.first_name_male() if sex == 1 else names.first_name_female()
        self.partner = None
        self.children = []
        self.parents = []
        
    def set_partner(self, partner):
        self.partner = partner
        partner.partner = self

        if self.age >= 55 and partner.age >= 55:
            if self.sex == "Male" and partner.sex == "Male":
                chosen_name = random.choice([self.family_name, partner.family_name])
                self.family_name = partner.family_name = chosen_name
            elif self.sex == "Female" and partner.sex == "Female":
                chosen_name = random.choice([self.family_name, partner.family_name])
                self.family_name = partner.family_name = chosen_name
            elif self.sex == "Male":
                partner.family_name = self.family_name
            else:
                self.family_name = partner.family_name

        elif (self.age < 55 and self.age >=18) and (partner.age < 55 and partner.age >= 18):
                combined_name = f"{self.family_name}-{partner.family_name}" if self.sex == "Female" else f"{partner.family_name}-{self.family_name}"
                if combined_name not in self.family_name:
                    self.set_family_name(combined_name)
                    partner.set_family_name(combined_name)
                    
    def set_family_name(self, new_name):
        self.family_name = new_name

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

        if self.partner and child not in self.partner.children:
            self.partner.children.append(child)

    def __str__(self):
        partner_info = f"Partner: {self.partner.first_name} {self.partner.age}" if self.partner else "No Partner"
        parent_names = ', '.join([p.first_name + " "+ p.family_name for p in self.parents])
        children_names = ', '.join([c.first_name +" " +c.family_name for c in self.children])
        return f"{self.first_name} {self.family_name} (Age: {self.age}, Sex: {self.sex}, {partner_info}, Parents: [{parent_names}], Children: [{children_names}])"

class Family:
    def __init__(self, family_name):
        self.family_name = family_name
        self.families = []

    def add_family(self, family):
        self.families.append(family)

    def __str__(self):
        family_members = '\n  '.join([str(member) for member in self.families])
        return f"Family: {self.family_name}\n  Members:\n  {family_members}\n"

class Household:
    def __init__(self, Family):
        self.members = []
        self.address = None
        self.children_limit = 5
        self.extended_family = Family

    def add_member(self, person):
        if not any(m.age >= 18 for m in self.members):
            self.family_name = person.family_name
        self.members.append(person)

    def can_add_child(self):
        return len([member for member in self.members if member.age < 18]) < self.children_limit

    def set_address(self, address):
        self.address = address

    def __str__(self):
        address_description = f"Address: {self.address}" if self.address else "No Address"
        household_members = '\n  '.join([str(member) for member in self.members])
        return f"Household of the {self.extended_family.family_name} Family\n  {address_description}\n  Members:\n  {household_members}\n"
    
def create_families(persons):
    families = {}
    for person in persons:
        if person.family_name not in families:
            families[person.family_name] = Family(person.family_name)
        families[person.family_name].add_family(person)

    for family in families.values():
        oldest_male = sorted([p for p in family.families if p.age >= 55 and p.sex == "Male"], key=lambda x: x.age, reverse=True)
        if oldest_male:
            family_name = oldest_male[0].family_name
            for member in family.families:
                if member.age < 55: 
                    member.set_family_name(family_name)

    return families

def create_households(persons):
    households = []
    included = set()

    for person in persons:
        if person.age >= 18 and person.age < 55 and person not in included:
            household = Household(Family(person.family_name))
            household.add_member(person)
            included.add(person)
            if person.partner:
                household.add_member(person.partner)
                included.add(person.partner)
            for child in person.children:
                if child not in included:
                    household.add_member(child)
                    included.add(child)
            households.append(household)

    for person in persons:
        if person.age >= 55 and person not in included:
            household = Household(Family(person.family_name))
            household.add_member(person)
            included.add(person)
            if person.partner:
                household.add_member(person.partner)
                included.add(person.partner)
            households.append(household)

    return households

def assign_parents(parents, child):
    possible_parents = [
        (p1, p2) for p1 in parents for p2 in parents 
        if p1.partner == p2 and p1 != p2 and p1.partner is not None
    ]

    if possible_parents:
        selected_pair = random.choice(possible_parents)
        child.parents = list(selected_pair)

        if selected_pair[0].age < 55 and selected_pair[1].age < 55:

            if "-" in selected_pair[0].family_name:
                child.set_family_name(selected_pair[0].family_name)
            else:
                combined_name = f"{selected_pair[0].family_name}-{selected_pair[1].family_name}" if selected_pair[0].sex == "Female" else f"{selected_pair[1].family_name}-{selected_pair[0].family_name}"
                child.set_family_name(combined_name)

        else:
            male_parent = selected_pair[0] if selected_pair[0].sex == "Male" else selected_pair[1]
            if child.family_name is not male_parent.family_name:
                child.set_family_name(male_parent.family_name)  

        if child not in selected_pair[0].children:
            selected_pair[0].children.append(child)
        if child not in selected_pair[1].children:
            selected_pair[1].children.append(child)
    else:
        print("No suitable parents found for", child.first_name)
           
def set_partners(persons):
    males = [p for p in persons if p.sex == "Male"]
    females = [p for p in persons if p.sex == "Female"]

    # Form heterosexual partnerships first
    while males and females:
        male = males.pop(0)
        for female in females:
            if not set(male.parents).intersection(set(female.parents)):
                male.set_partner(female)
                females.remove(female)
                break

    # If any individuals are left, form same-sex partnerships
    remaining_individuals = males + females
    while len(remaining_individuals) > 1:
        partner1 = remaining_individuals.pop(0)
        for partner2 in remaining_individuals:
            if not set(partner1.parents).intersection(set(partner2.parents)):
                partner1.set_partner(partner2)
                remaining_individuals.remove(partner2)
                break

def set_family(persons):
    grandparents = [p for p in persons if p.age >= 55]
    adults = [p for p in persons if 18 <= p.age < 55]
    children = [p for p in persons if p.age < 18]

    set_partners(grandparents)
    [assign_parents(grandparents, adult) for adult in adults]
    
    set_partners(adults)
    [assign_parents(adults, child) for child in children] 

    
    families = create_families(persons)
    households = create_households(persons)
    return families, households

if __name__ == "__main__":
    N = 100
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex": sampler.sample_sex(N),
        "work": sampler.sample_work(ages),
        "student": sampler.sample_student(ages),
    }

    persons = [Person(age=data['age'][i], sex=data['sex'][i], work=data['work'][i]) for i in range(len(data['age']))]
    families, households = set_family(persons)

    print("Families Overview:")
    for family in families.values():
        print(family)

    print("Households Overview:")
    for household in households:
        print(household)
        