from sampler import sampler
import random
from simulations import set_family 
from persons import Person


def assign_addresses_to_households(households, numberOfHousholds):
    addresses = sampler.sample_household(numberOfHousholds)
    house_addresses = sampler._house_address()["kommune_adresse"].tolist()
    apartment_addresses = sampler._apartment_address()["kommune_adresse"].tolist()

    addresses = [dict(zip(addresses, t)) for t in zip(*addresses.values())]
    for household in households:
        num_people_in_household = len(household.members)
        suitable_address = next(
            (addr for addr in addresses if addr["people"] >= num_people_in_household),
            None,
        )

        a = (
            random.choice(house_addresses)
            if suitable_address["type"] in ["house", "terrace-house"]
            else random.choice(apartment_addresses)
        )

        if suitable_address:
            household.set_address(a)
            addresses.remove(suitable_address)
        else:
            household.set_address("No suitable address found")


if __name__ == "__main__":
    N = 1100
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
    households = set_family(persons)

    assign_addresses_to_households(households)

    for household in households:
        print(household)

    