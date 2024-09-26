from family import Family
from household import Household
from utils import get_last_names

def create_families(persons):
    families = {}

    def add_person_and_descendants(person, family):
        if person not in family.family_members:
            family.family_members.append(person)
            person.family_id = family.id
            for child in person.children:
                add_person_and_descendants(child, family)

    for person in persons:
        if any(person in family.family_members for family in families.values()):
            continue

        if person.family_name not in families:
            families[person.family_name] = Family()

        add_person_and_descendants(person, families[person.family_name])

    return list(families.values())

def create_households(young_adults, adults, seniors):
    households = []
    added_to_household = set()

    def add_to_new_household(person):
        if person in added_to_household:
            return

        household = Household(Family())
        household.add_member(person)
        added_to_household.add(person)

        if person.partner and person.partner not in added_to_household:
            household.add_member(person.partner)
            added_to_household.add(person.partner)
        
        for child in person.children:
            if child not in added_to_household and child.age <= 18:
                household.add_member(child)
                added_to_household.add(child)
        
        households.append(household)

    all_individuals = seniors + adults + young_adults
    for person in all_individuals:
        if person not in added_to_household:
            add_to_new_household(person)

    return households

def set_family(children, young_adults, adults, seniors):

    persons = children + young_adults+ adults+ seniors
    last_names = get_last_names(len(seniors))

    Family.set_partners(seniors)
    for i,p1 in enumerate(seniors):
        if p1.family_name == None and p1.partner != None:
            p1.set_family_name(last_names[i])
            p1.partner.set_family_name(last_names[i])
        if p1.partner == None:
            p1.set_family_name(last_names[i])


    for adult in adults:
        Family.assign_parents(seniors,adult)
    Family.set_partners(adults)

    for child in children + young_adults:
        Family.assign_parents(adults,child)
    Family.set_partners(young_adults)

    ## persons with no parents
    no_parents = [p for p in persons if p.parents == []]
    families = create_families(no_parents)
    households = create_households(young_adults, adults, seniors)

    return families, households
