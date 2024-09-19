import pandas as pd
import numpy as np
from neo4j import GraphDatabase
from simulations import set_family 
from utils import people,get_names ,get_random_data, assign_addresses_to_households,assign_persons_to_companies

NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="123456789"
# Connect to Neo4j database
uri = NEO4J_URI
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def export_companies_to_neo4j(companies:pd.DataFrame)->None:
    with driver.session() as session:
        for _, company in companies.iterrows():
            session.run(
                "MERGE (c:Company {organisasjonsnummer: $organisasjonsnummer, navn: $navn, organisasjonsform: $organisasjonsform, "
                "registreringsdatoEnhetsregisteret: $registreringsdatoEnhetsregisteret, antallAnsatte: $antallAnsatte, "
                "forretningsadresse: $forretningsadresse, stiftelsesdato: $stiftelsesdato, vedtektsdato: $vedtektsdato, "
                "vedtektsfestetFormaal: $vedtektsfestetFormaal, aktivitet: $aktivitet, links: $links, "
                "sisteInnsendteAarsregnskap: $sisteInnsendteAarsregnskap, kommune: $kommune, overordnetEnhet: $overordnetEnhet})",
                organisasjonsnummer=company['orgnr'],
                navn=company['navn'],
                organisasjonsform=company['organisasjonsform'],
                registreringsdatoEnhetsregisteret=company['registreringsdatoEnhetsregisteret'],
                antallAnsatte=company['antallAnsatte'],
                forretningsadresse=company['forretningsadresse'],
                stiftelsesdato=company['stiftelsesdato'],
                vedtektsdato=company['vedtektsdato'],
                vedtektsfestetFormaal=company['vedtektsfestetFormaal'],
                aktivitet=company['aktivitet'],
                links=company['links'],
                sisteInnsendteAarsregnskap=company['sisteInnsendteAarsregnskap'],
                kommune=company['kommune'],
                overordnetEnhet=company['overordnetEnhet']
            )
def export_idustrial_codes_to_neo4j(code_description:pd.DataFrame)->None:
    with driver.session() as session:
        for _, code in code_description.iterrows():
            session.run(
                "CREATE (i:IndustrialCode {Code: $code, Description: $description})",
                code=code['industrial_code'],
                description=code['description']

            )
def company_industrialCode_relationship(company:pd.DataFrame)->None:
    with driver.session() as session:
        for _, c in company.iterrows():
            
            session.run(
            "MATCH(c:Company {organisasjonsnummer:$orgnr}), (i:IndustrialCode {Code: $industrial_code})"
            "CREATE(c)-[:BELONGSTO]->(i)",
            orgnr=c['orgnr'],
            industrial_code=c['industrial_code']
            )


def assign_persons_to_companies(persons, companies_df, management_counts):

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
            if  person.occupation:  # Person is available for assignment
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
            if  person.occupation:  # Person is available for assignment
                person.occupation = company['navn']
                person.position = 'employee'
                company_employee_count[company_id] += 1
                assigned_employees += 1






def main():
    næringskoder_1 = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/rel_business_1.csv"
    næringskoder_2 = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/rel_business_2.csv"
    næringskoder_3 = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/rel_business_3.csv"
    industrial_codes_description = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/business_codes.csv"
    companies = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/enheter.csv"
    roles_in_companies = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/roles_persons.csv"

    # Load industrial codes description
    code_description = pd.read_csv(industrial_codes_description)
    code_description.rename(columns={
        'naeringskode': 'industrial_code',
        'naeringsbeskrivelse': 'description'
    }, inplace=True)

    # List of næringskoder files and their corresponding code columns
    næringskoder_files = [næringskoder_1, næringskoder_2, næringskoder_3]
    code_columns = ['naeringskode_1', 'naeringskode_2', 'naeringskode_3']

    # Load and rename industrial codes data
    industrial_codes_list = []
    for file, code_col in zip(næringskoder_files, code_columns):
        df = pd.read_csv(file)
        df.rename(columns={
            'organisasjonsnummer': 'orgnr',
            code_col: 'industrial_code'
        }, inplace=True)
        industrial_codes_list.append(df)

    # Concatenate all industrial codes DataFrames
    industrial_codes = pd.concat(industrial_codes_list, ignore_index=True)

    # # Load and process company data
    company_df = pd.read_csv(companies)
    company_df.fillna('Unknown', inplace=True)
    company_df.rename(columns={'organisasjonsnummer': 'orgnr'}, inplace=True)

    # Merge company data with industrial codes
    merged = company_df.merge(industrial_codes, on='orgnr', how='left')

    roles = pd.read_csv(roles_in_companies).drop(['role'],axis=1).drop_duplicates(subset=['orgnr', 'personal_number'])

    management_counts = roles.groupby('orgnr')['personal_number'].nunique().reset_index()
    management_counts.columns = ['orgnr', 'management_count']
    
    #people
    N = 300000
    data = get_random_data(N)

    female_firstname, male_firstname = get_names(data)

    persons = people(data=data, N=N, female_names=female_firstname, male_names=male_firstname)
    families, households = set_family(persons)
    numberOfHouseholds = len(households)

    assign_addresses_to_households(households, numberOfHouseholds)
    assign_persons_to_companies(persons=persons,companies_df=merged,management_counts=management_counts)



    # # Export to neo4j
    # export_companies_to_neo4j(merged)
    # export_idustrial_codes_to_neo4j(code_description)
    # company_industrialCode_relationship(merged)

 

if __name__ == "__main__":
    main()
