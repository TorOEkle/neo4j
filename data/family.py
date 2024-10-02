import random
from faker import Faker
from tqdm import tqdm
names = Faker(["no_NO","en_US","en","sv_SE"])

class Family:
    next_id = 1 
    def __init__(self):
        self.id = Family.next_id
        Family.next_id += 1 
        self.family_members = []

    def add_family(self, family,person):
        person.family_id = family.id 
        self.family_members.append(family)

    def __str__(self):
        family = "\n  ".join([str(member) for member in self.family_members])
        return f"Family members: \n{family}\n"
    
    @staticmethod
    def assign_parents(parents, child):
        parent_set = set(parents)
        couples_set = set()
        possible_parents = []

        for p1 in parents:
            p2 = p1.partner
            if p2 is not None and p2 in parent_set and p1 != p2:
                # Create a unique key for the couple to avoid duplicates
                couple_key = tuple(sorted([p1.personal_number, p2.personal_number]))
                if couple_key not in couples_set:
                    couples_set.add(couple_key)
                    if (
                        child not in p1.children and child not in p2.children
                        and p1.age >= child.age + 18 and p2.age >= child.age + 18
                        and len(p1.children) <= 5
                    ):
                        possible_parents.append((p1, p2))

        if possible_parents:
            selected_pair = random.choice(possible_parents)
            child.parents = list(selected_pair)

            if selected_pair[0].age < 55 and selected_pair[1].age < 55:
                if "-" in selected_pair[0].family_name:
                    child.set_family_name(selected_pair[0].family_name)
                else:
                    combined_names = sorted([selected_pair[0].family_name, selected_pair[1].family_name])
                    combined_name = f"{combined_names[0]}-{combined_names[1]}"
                    child.set_family_name(combined_name)
            else:
                male_parent = selected_pair[0] if selected_pair[0].sex == "Male" else selected_pair[1]
                if child.family_name != male_parent.family_name:
                    child.set_family_name(male_parent.family_name)

            if child not in selected_pair[0].children:
                selected_pair[0].add_child(child)
            if child not in selected_pair[1].children:
                selected_pair[1].add_child(child)
        else:
            print("No suitable parents found for", child.first_name, child.age)
            child.family_name = names.last_name()

    # def assign_parents(parents, child):
    #     possible_parents = [
    #         (p1, p2) for p1 in parents for p2 in parents
    #         if (
    #             p1.partner == p2 and p1 != p2 and p1.partner is not None
    #             and child not in p1.children and child not in p2.children
    #             and p1.age >= child.age + 18 and p2.age >= child.age + 18
    #             and len(p1.children) <= 5
    #         )
    #     ]

    #     if possible_parents:
    #         selected_pair = random.choice(possible_parents)
    #         child.parents = list(selected_pair)

    #         if selected_pair[0].age < 55 and selected_pair[1].age < 55:
    #             if "-" in selected_pair[0].family_name:
    #                 child.set_family_name(selected_pair[0].family_name)
    #             else:
    #                     combined_name = (
    #                         f"{selected_pair[0].family_name}-{selected_pair[1].family_name}"
    #                         if selected_pair[0].sex == "Female"
    #                         else f"{selected_pair[1].family_name}-{selected_pair[0].family_name}"
    #                     )
    #                     combined_names = sorted([selected_pair[0].family_name, selected_pair[1].family_name])
    #                     combined_name = f"{combined_names[0]}-{combined_names[1]}" if len(combined_names) >0 else combined_names[0]
    #                     child.set_family_name(combined_name)
    #         else:
    #             male_parent = selected_pair[0] if selected_pair[0].sex == "Male" else selected_pair[1]
    #             if child.family_name != male_parent.family_name:
    #                 child.set_family_name(male_parent.family_name)

    #         if child not in selected_pair[0].children:
    #             selected_pair[0].add_child(child)
    #         if child not in selected_pair[1].children:
    #             selected_pair[1].add_child(child)
    #     else:
    #         print("No suitable parents found for", child.first_name, child.age)
    #         child.family_name = names.last_name()


    @staticmethod
    def set_partners(persons):
        males,unpaired_males = [],[]
        females,unpaired_females = [],[]

        for person in persons:
            if person.sex == "Male" :
                males.append(person)
            elif person.sex == "Female":
                females.append(person)


            while males and females:
                male = males.pop(0)
                female = females.pop(0)
                if (len(male.parents) == 0 or len(female.parents) == 0 ) or (male.parents[0] not in female.parents):
                    male.set_partner(female)
                else:
                    unpaired_males.append(male)
                    unpaired_females.append(female)

        reminding = unpaired_males + unpaired_females
        for i in range(0, len(reminding), 2):
            if i + 1 < len(reminding):
                person1 = reminding[i]
                person2 = reminding[i+1]
                if (len(person1.parents)==0 or len(person2.parents) == 0 ) or (person1.parents[0] not in person2.parents):
                    person1.set_partner(person2)

    def __str__(self):
        family = "\n  ".join([f"{str(member)}" for member in self.family_members ])
        return f"Family members: \n{family}\n"
    
