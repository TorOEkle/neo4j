from typing import List
from persons import Person
import pandas as pd



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
