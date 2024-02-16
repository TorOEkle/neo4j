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
    return [names.first_name() for i in range(N)]


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
def count_and_print_same_sex_partnerships(persons):
    same_sex_partnerships = []
    others = []
    for person in persons:
        if person.partner and person.sex == person.partner.sex:
            same_sex_partnerships.append((person, person.partner))
        else:
            others.append((person, person.partner))

    count = len(same_sex_partnerships)
    count1 = len(others)

    print(count, count1)

@time_it
def get_random_data(N):
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex":  sampler.sample_sex(N) ,
        "work": sampler.sample_work(ages),
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
        person = Person(age=data["age"][i], sex=data["sex"][i], work=data["work"][i], name=name)
        persons.append(person)
    return persons

@time_it
def get_names(data):
    males = np.count_nonzero(data['sex'] == 1)
    females = len(data["sex"]) - males
    male_firstname = [names.first_name_male() for _ in range(males)]
    female_firstname = [names.first_name_female() for _ in range(females)]

    return female_firstname,male_firstname