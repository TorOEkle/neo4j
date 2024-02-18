import time
from faker import Faker
from sampler import sampler
import random
from persons import Person
import numpy as np 

names = Faker(["no_NO","en_US","en","sv_SE"])

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {(end - start):.4f} seconds.")
        return result

    return wrapper

@time_it
def get_last_names(N):
    return [names.last_name() for _ in range(N)]

@time_it
def extracurricular_activity(ages, p): 
    activity = np.zeros(len(ages))  # Initialize all as 0
    print(activity)

    # List of possible extracurricular activities
    activities = ["Football", "American football", "Volleyball", "Tennis", "Basketball", "Chess"]

    # Dictionary to store assigned activities
    assigned_activities = {}

    # Assign a random activity to each student
    for person in range(len(ages)):
        if 6 <= ages[person] <= 18 and random.random() < p: # Set limit for age range (can change this) + prob p for activity. 
            assigned_activities[person] = random.choice(activities)
        else:
            assigned_activities[person] = None


    # print(len(np.array(list(assigned_activities.values()))))
    assigned_activities = np.array(list(assigned_activities.values())) # Create a array from the dict. 
    return assigned_activities

@time_it
def segregate_persons_by_age(persons):
    children, young_adults, adults, seniors = [],[],[],[]
    for p in persons:
        if p.age < 18:
            children.append(p)
        elif 18 <= p.age <= 25 :
            young_adults.append(p)

        elif 26 <= p.age < 55:
            adults.append(p)
        else:
            seniors.append(p)

    return children, young_adults, adults, seniors

@time_it
def get_random_data(N):
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex":  sampler.sample_sex(N) ,
        "work": sampler.sample_work(ages),
        "activity": extracurricular_activity(ages, p = 0.8)
    }
    return data

@time_it
def people(data, N, female_names, male_names):
    persons = []
    for i in range(N):
        if data["sex"][i] == 1:
            name = male_names.pop()
        else:
            name = female_names.pop()
        person = Person(age=data["age"][i], sex=data["sex"][i], work=data["work"][i],activity=data["activity"][i], name=name)
        persons.append(person)
    return persons

@time_it
def get_names(data):
    males = np.count_nonzero(data['sex'] == 1)
    females = len(data["sex"]) - males
    male_firstname = [names.first_name_male() for _ in range(males)]
    female_firstname = [names.first_name_female() for _ in range(females)]

    return female_firstname,male_firstname

@time_it
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