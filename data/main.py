from simulations import set_family 
from utils import people,get_names ,get_random_data, assign_addresses_to_households, write_to_csv
from neo4j_connect import export_persons_to_neo4j, export_families_to_neo4j, export_households_to_neo4j, export_parent_child_to_neo4j,export_partners_to_neo4j,export_activities_to_neo4j

def main():
    N = 500
    data = get_random_data(N)
    female_firstname, male_firstname = get_names(data)

    persons = people(data=data, N=N, female_names=female_firstname, male_names=male_firstname)
    families, households = set_family(persons)
    numberOfHouseholds = len(households)

    assign_addresses_to_households(households, numberOfHouseholds)
    
    #write_to_csv(persons=persons,families=families,households=households)

    # Write data to Neo4j
    export_persons_to_neo4j(persons)
    export_families_to_neo4j(families)
    export_households_to_neo4j(households)
    export_parent_child_to_neo4j(persons)
    export_partners_to_neo4j(persons)
    export_activities_to_neo4j(persons)

 
if __name__ == "__main__":
    main()
