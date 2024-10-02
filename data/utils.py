import time
from faker import Faker
from sampler import sampler
import random
from persons import Person
import numpy as np 

from typing import List
import pandas as pd

names = Faker(["no_NO","en_US","en","sv_SE"])

def get_last_names(N):
    return [names.last_name() for _ in range(N)]

def extracurricular_activity(ages, p): 
    activities = ["Football", "American football", "Volleyball", "Tennis", "Basketball", "Chess"]

    # Dictionary to store assigned activities
    assigned_activities = {}

    # Assign a random activity to each student
    for person in range(len(ages)):
        if 6 <= ages[person] <= 25 and random.random() < p: # Set limit for age range (can change this) + prob p for activity. 
            assigned_activities[person] = random.choice(activities)
        else:
            assigned_activities[person] = None


    # print(len(np.array(list(assigned_activities.values()))))
    assigned_activities = np.array(list(assigned_activities.values())) # Create a array from the dict. 
    return assigned_activities

def segregate_persons_by_age(persons):
    children, young_adults, adults, seniors = [],[],[],[]
    for p in persons:
        if p.age <= 18:
            children.append(p)
        elif 19 <= p.age <= 24 :
            young_adults.append(p)
        elif 25 <= p.age < 62:
            adults.append(p)
        else:
            seniors.append(p)
            p.occupation = 'Retired'

    return children, young_adults, adults, seniors

def get_random_data(N):
    ages = sampler.sample_age(N)
    data = {
        "age": ages,
        "sex":  sampler.sample_sex(N) ,
        "activity": extracurricular_activity(ages, p = 0.8)
    }
    return data

def people(data, N, female_names, male_names):
    persons = []
    for i in range(N):
        if data["sex"][i] == 1:
            name = male_names.pop()
            sex = "Male"
        else:
            name = female_names.pop()
            sex = "Female"
        person = Person(age=data["age"][i], sex=sex,activity=data["activity"][i], name=name)
        persons.append(person)
    return persons

def get_names(data):
    males = np.count_nonzero(data['sex'] == 1)
    females = len(data["sex"]) - males
    male_firstname = [names.first_name_male() for _ in range(males)]
    female_firstname = [names.first_name_female() for _ in range(females)]

    return female_firstname,male_firstname

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

def workForce(young_adults, adults,):

    # Randomly select 39% of age_19_24_group to be students
    num_students = int(0.39 * len(young_adults))
    students = random.sample(young_adults, num_students)

    for p in students:
        p.occupation = 'Student'

    # Remove students from the main group
    remaining_group = [p for p in young_adults + adults if p not in students]
    
    num_unemployed = int(0.04 * len(remaining_group))
    unemployed = random.sample(remaining_group, num_unemployed)

    for p in unemployed:
        p.occupation = 'Unemployed'

    # The rest go into the workforce
    workforce = [p for p in remaining_group if p not in unemployed]

    for p in workforce:
        p.occupation = 'workforce'

def assign_persons_to_companies(persons:List[Person], companies_df:pd.DataFrame, management_counts:pd.DataFrame)-> None:

    # Merge companies_df with management_counts
    companies_df = companies_df.merge(management_counts, on='orgnr', how='left')

    # Fill missing management counts with 1 (assuming at least one manager)
    companies_df['management_count'] = companies_df['management_count'].fillna(1).astype(int)

    # Calculate the number of employee positions
    companies_df['employee_count'] = companies_df['antallAnsatte'] - companies_df['management_count']
    # Ensure no negative employee counts
    companies_df['employee_count'] = companies_df['employee_count'].apply(lambda x: max(0, x))

    # Initialize the employee count dictionary
    company_employee_count = {company['orgnr']: 0 for _, company in companies_df.iterrows()}

    # Shuffle the persons list to randomize assignments
    np.random.shuffle(persons)

    # Index to keep track of the current position in the persons list
    person_index = 0
    total_persons = len(persons)

    # Assign management positions first
    for _, company in companies_df.iterrows():
        company_id = company['orgnr']
        management_slots = company['management_count']
        assigned_management = 0

        while assigned_management < management_slots and person_index < total_persons:
            person = persons[person_index]
            person_index += 1
            if  person.occupation == 'workforce':
                person.occupation = company['navn']
                person.position = 'management'
                company_employee_count[company_id] += 1
                assigned_management += 1

    # Assign remaining employee positions
    for _, company in companies_df.iterrows():
        company_id = company['orgnr']
        employee_slots = company['employee_count']
        assigned_employees = 0

        while assigned_employees < employee_slots and person_index < total_persons:
            person = persons[person_index]
            person_index += 1
            if  person.occupation == 'workforce':
                person.occupation = company['navn']
                person.position = 'employee'
                company_employee_count[company_id] += 1
                assigned_employees += 1
