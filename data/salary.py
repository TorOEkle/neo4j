from typing import List
from persons import Person
import pandas as pd
import numpy as np

def salary(companies_df:pd.DataFrame)-> None:
    ...

def main():
    industrial_codes_description = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/business_codes.csv"
    companies = "https://raw.githubusercontent.com/TorOEkle/neo4j/refs/heads/company_data/data/csv_files/enheter.csv"


    # Load industrial codes description
    code_description = pd.read_csv(industrial_codes_description)
    code_description.rename(columns={
        'naeringskode': 'industrial_code',
        'naeringsbeskrivelse': 'description'
    }, inplace=True)

    
if __name__ =="__main__":
    main()