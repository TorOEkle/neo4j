import pandas as pd

from simulations import set_family
from utils import people,get_names ,get_random_data, assign_addresses_to_households,segregate_persons_by_age,workForce,assign_persons_to_companies
from neo4j_connect import export_person_company_relationships_to_neo4j,export_persons_to_neo4j, export_families_to_neo4j, export_households_to_neo4j, export_parent_child_to_neo4j,export_partners_to_neo4j,export_activities_to_neo4j, export_companies_to_neo4j,export_idustrial_codes_to_neo4j,company_industrialCode_relationship

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

    N = 100000
    data = get_random_data(N)
    female_firstname, male_firstname = get_names(data)

    persons = people(data=data, N=N, female_names=female_firstname, male_names=male_firstname)

    children, young_adults, adults, seniors = segregate_persons_by_age(persons)
    workForce(young_adults, adults)

    families, households = set_family(children, young_adults, adults, seniors)
    numberOfHouseholds = len(households)

    assign_addresses_to_households(households, numberOfHouseholds)
    assign_persons_to_companies(persons=persons,companies_df=merged,management_counts=management_counts)

    print("loading to Neo4j")
    ## Write data to Neo4j
    export_persons_to_neo4j(persons)
    export_families_to_neo4j(families)
    export_households_to_neo4j(households)
    export_parent_child_to_neo4j(persons)
    export_partners_to_neo4j(persons)
    export_activities_to_neo4j(persons)
    export_companies_to_neo4j(merged)
    export_person_company_relationships_to_neo4j(persons=persons)
    export_idustrial_codes_to_neo4j(code_description)
    company_industrialCode_relationship(merged)

if __name__ == "__main__":
    main()
