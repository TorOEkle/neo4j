from sampler import sampler
from family import Person,set_family, Household,Family
import random

def assign_addresses_to_households(households, addresses):

    house_addresses = sampler._house_address()['kommune_adresse'].tolist()
    apartment_addresses = sampler._apartment_address()['kommune_adresse'].tolist()

    addresses = [dict(zip(addresses, t)) for t in zip(*addresses.values())]
    for household in households:
        num_people_in_household = len(household.members)

        suitable_address = next((addr for addr in addresses if addr['people'] >= num_people_in_household), None)
        a = random.choice(house_addresses) if suitable_address['type'] in ['house', 'terrace-house'] else random.choice(apartment_addresses)

        if suitable_address:
            household.set_address(a)
            addresses.remove(suitable_address)
        else:
            household.set_address("No suitable address found")
    return households

if __name__ == "__main__":
    N = 10
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex": sampler.sample_sex(N),
        "work": sampler.sample_work(ages),
        "student": sampler.sample_student(ages),
    }

    persons = [Person(age=data['age'][i], sex=data['sex'][i], work=data['work'][i]) for i in range(len(data['age']))]

    families, households = set_family(persons)
    caves = sampler.sample_household(len(households))
    households = assign_addresses_to_households(households, caves)

    # Print households for demonstration
    for household in households:
        print(household)

    

    # for household in households:
    #     print(household)

    # print("Families Overview:")
    # for family in families.values():
    #     print(family)

    # print("Households Overview:")
    # for household in households:
    #     print(household)