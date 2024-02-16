from faker import Faker
from sampler import sampler
import random

names = Faker("no_NO")

# class Person:
#     def __init__(self, age, sex, work, name=None):
#         self.age = age
#         self.sex = "Male" if sex ==1 else "Female"
#         self.occupation = work
#         self.marital_status = "single"
#         self.family_name = None
#         self.first_name = name
#         self.partner = None
#         self.children = []
#         self.parents = []

#     def set_partner(self, partner):
#         self.partner = partner
#         partner.partner = self

#     def set_family_name(self, new_name):
#         self.family_name = new_name

#     def add_child(self, child):
#         if child not in self.children:
#             self.children.append(child)

#         if self.partner and child not in self.partner.children:
#             self.partner.children.append(child)

#     @staticmethod
#     def sort_people_by_first_name(people):
#         return sorted(people, key=lambda person: person.first_name)


#     def __str__(self):
#         partner_info = (
#             f"Partner: {self.partner.first_name} {self.partner.age}"
#             if self.partner
#             else "No Partner"
#         )
#         parent_names = ", ".join(
#             [p.first_name for p in self.parents]
#         )
#         children_names = ", ".join(
#             [c.first_name for c in self.children]
#         )
#         return (f"{self.first_name} {self.family_name} 
#                 (Age: {self.age}, 
#                 Sex: {self.sex}, 
#                 {partner_info}, 
#                 Parents: [{parent_names}], 
#                 Children: [{children_names}])")
    
# class Family:
#     def __init__(self):
#         self.family_members = []

#     def add_family(self, family):
#         self.family_members.append(family)

#     def __str__(self):
#         family = "\n  ".join([str(member) for member in self.family_members])
#         return f"Family members: \n{family}\n"

# class Household:
#     def __init__(self, Family):
#         self.members = []
#         self.address = None
#         self.children_limit = 5
#         self.extended_family = Family

#     def add_member(self, person):
#         if person.age < 18:
#             if not self.can_add_child():
#                 return False

#         if not any(m.age >= 18 for m in self.members):
#             self.family_name = person.family_name
#         self.members.append(person)
#         return True

#     def can_add_child(self):
#         return (
#             len([member for member in self.members if member.age < 18])
#             < self.children_limit
#         )

#     def set_address(self, address):
#         self.address = address

#     def __str__(self):
#         address_description = (
#             f"Address: {self.address}" if self.address else "No Address"
#         )
#         household_members = "\n  ".join([str(member) for member in self.members])
#         return f"Household of the Family living in \n  {address_description}\n  Members:\n{household_members} \n"
    
# def create_households(persons):
#     households = []
#     added_to_household = set() 

#     def add_to_new_household(primary_person):
#         if primary_person in added_to_household:
#             return  

#         household = Household(Family())
#         household.add_member(primary_person)
#         added_to_household.add(primary_person)

#         if primary_person.partner and primary_person.partner not in added_to_household:
#             household.add_member(primary_person.partner)
#             added_to_household.add(primary_person.partner)

#         for child in primary_person.children:
#             if child not in added_to_household and child.age < 18:
#                 household.add_member(child)
#                 added_to_household.add(child)

#         households.append(household)

#     for adult in filter(lambda p: 18 <= p.age and p not in added_to_household, persons):
#         add_to_new_household(adult)


    # return households

# def create_households(children, young_adults, adults, seniors):
#     households = []

#     added_to_household = set()

#     def add_to_new_household(person):
#         household = Household(Family())
#         household.add_member(person)
#         added_to_household.add(person)

#         if person.partner:
#             household.add_member(person.partner)
#             added_to_household.add(person.partner)
        
#         for child in person.children:
#             if child not in added_to_household and child.age <18:
#                 household.add_member(child)
#                 added_to_household.add(child)
        
#         households.append(household)


#     for person in [p for p in seniors if  p not in added_to_household]:
#         if person.partner and all(p not in added_to_household for p in [person, person.partner]):
#             add_to_new_household(person)


#     for person in [p for p in adults if p not in added_to_household]:
#         add_to_new_household(person)

#     for person in [p for p in young_adults if  p not in added_to_household]:
#         if person.partner and random.choice([True, False]):
#             add_to_new_household(person)


#     return households

# def segregate_persons_by_age(persons):
#     children, young_adults, adults, seniors = [],[],[],[]
#     for p in persons:
#         if p.age < 18:
#             children.append(p)
#         elif 18 <= p.age <= 25 :
#             young_adults.append(p)

#         elif 26 <= p.age < 55:
#             adults.append(p)
#         else:
#             seniors.append(p)

#     return children, young_adults, adults, seniors

# def assign_parents(parents, child):
#     possible_parents = [
#         (p1, p2) for p1 in parents for p2 in parents
#         if p1.partner == p2 and p1 != p2 and p1.partner is not None
#         and child not in [p1, p2, p1.children + p2.children]
#     ]
#     if possible_parents:
#         selected_pair = random.choice(possible_parents)
#         child.parents = list(selected_pair)

#         if selected_pair[0].age < 55 and selected_pair[1].age < 55:

#             if "-" in selected_pair[0].family_name:
#                 child.set_family_name(selected_pair[0].family_name)
#             else:
#                 combined_name = (
#                     f"{selected_pair[0].family_name}-{selected_pair[1].family_name}"
#                     if selected_pair[0].sex == "Female"
#                     else f"{selected_pair[1].family_name}-{selected_pair[0].family_name}"
#                 )
#                 combined_names = sorted([selected_pair[0].family_name, selected_pair[1].family_name])
#                 combined_name = f"{combined_names[0]}-{combined_names[1]}"
#                 child.set_family_name(combined_name)

#                 child.set_family_name(combined_name)

#         else:
#             male_parent = (
#                 selected_pair[0] if selected_pair[0].sex == "Male" else selected_pair[1]
#             )
#             if child.family_name is not male_parent.family_name:
#                 child.set_family_name(male_parent.family_name)

#         if child not in selected_pair[0].children:
#             selected_pair[0].children.append(child)
#         if child not in selected_pair[1].children:
#             selected_pair[1].children.append(child)
#     else:
#         print("No suitable parents found for", child.first_name)

# def set_partners(persons):
#     males,unpaired_males = [],[]
#     females,unpaired_females = [],[]

#     for person in persons:
#         if person.sex == "Male" :
#             males.append(person)
#         elif person.sex == "Female":
#             females.append(person)

#     while males and females:
#         male = males.pop(0)
#         female = females.pop(0)
#         if len(male.parents) == 0 and len(female.parents) == 0 or male.parents != female.parents:
#             male.set_partner(female)
#         else:
#             unpaired_males.append(male)
#             unpaired_females.append(female)

#     for remaining in (unpaired_males, unpaired_females):
#         while len(remaining) > 1:
#             person1 = remaining.pop()
#             person2 = remaining.pop()
#             if person1.parents != person2.parents:
#                 person1.set_partner(person2)
#             elif len(person1.parents)==0 and len(person2.parents) == 0:
#              person1.set_partner(person2) 
  
# def get_last_names(N):
    # return [names.last_name() for _ in range(N)]
             
# def create_families(persons):
#     families = {}

#     def add_person_and_descendants(person, family):
#         if person not in family.family_members:
#             family.add_family(person)
#             for child in person.children:
#                 add_person_and_descendants(child, family)

#     for person in persons:
#         if any(person in family.family_members for family in families.values()):
#             continue


#         if person.family_name not in families:
#             families[person.family_name] = Family()
        
#         add_person_and_descendants(person, families[person.family_name])

#     return list(families.values())

# def set_family(persons):
#     children, young_adults, adults, seniors = segregate_persons_by_age(persons)
#     last_names = get_last_names(len(seniors))
    
#     print(f"Num seniors: {len(seniors)}\nNum adults: {len(adults)}\nNum young adults: {len(young_adults)}\n Num children: {len(children)}")

#     set_partners(seniors)

#     for i,p1 in enumerate(seniors):
#         if p1.family_name == None and p1.partner != None:
#             p1.set_family_name(last_names[i])
#             p1.partner.set_family_name(last_names[i])

#     [assign_parents(seniors, adult) for adult in adults]
#     set_partners(adults)

#     set_partners(young_adults)
#     [assign_parents(adults, child) for child in children + young_adults ]


#     families = create_families(persons)

#     households = create_households(persons)

#     return families, households

if __name__ == "__main__":
    N = 100
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex": sampler.sample_sex(N),
        "work": sampler.sample_work(ages),
        "student": sampler.sample_student(ages),
    }

    persons = [
        Person(age=data["age"][i], sex=data["sex"][i], work=data["work"][i])
        for i in range(len(data["age"]))
    ]

    families, households = set_family(persons)

    print("Families Overview:")
    for family in families.values():
        print(family)

    print("Households Overview:")
    for household in households:
        print(household)
