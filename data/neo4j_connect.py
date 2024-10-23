from neo4j import GraphDatabase
import pandas as pd


NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="123456789"
AURA_INSTANCEID="1fb1cc99"
AURA_INSTANCENAME="Instance01"

# Connect to Neo4j database
uri = NEO4J_URI
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Connect to Neo4j database
uri = NEO4J_URI
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Optimized Neo4j export functions
def export_persons_to_neo4j(persons):
    with driver.session() as session:
        # Prepare data for batch insertion
        persons_data = [
            {
                'personal_number': person.personal_number,
                'first_name': person.first_name,
                'family_name': person.family_name,
                'age': person.age,
                'sex': person.sex,
                'occupation': person.occupation
            }
            for person in persons
        ]

        # Batch insert persons using UNWIND
        query = """
        UNWIND $persons AS person
        MERGE (p:Person {personal_number: person.personal_number})
        SET p.first_name = person.first_name,
            p.family_name = person.family_name,
            p.age = person.age,
            p.sex = person.sex,
            p.occupation = person.occupation
        """

        # Run the query in a transaction
        session.write_transaction(lambda tx: tx.run(query, persons=persons_data))

def export_families_to_neo4j(families):
    with driver.session() as session:
        families_data = [
            {
                'family_id': family.id,
                'member_personal_numbers': [member.personal_number for member in family.family_members]
            }
            for family in families
        ]

        # Create families and relationships in batches
        query = """
        UNWIND $families AS family
        MERGE (f:Family {family_id: family.family_id})
        WITH f, family.member_personal_numbers AS member_personal_numbers
        UNWIND member_personal_numbers AS personal_number
        MATCH (p:Person {personal_number: personal_number})
        MERGE (p)-[:MEMBER_OF_FAMILY]->(f)
        """

        session.write_transaction(lambda tx: tx.run(query, families=families_data))

def export_households_to_neo4j(households):
    with driver.session() as session:
        households_data = [
            {
                'household_id': household.id,
                'address': household.address,
                'member_personal_numbers': [member.personal_number for member in household.members]
            }
            for household in households
        ]

        query = """
        UNWIND $households AS household
        MERGE (h:Household {household_id: household.household_id})
        SET h.address = household.address
        WITH h, household.member_personal_numbers AS member_personal_numbers
        UNWIND member_personal_numbers AS personal_number
        MATCH (p:Person {personal_number: personal_number})
        MERGE (p)-[:MEMBER_OF_HOUSEHOLD]->(h)
        """

        session.write_transaction(lambda tx: tx.run(query, households=households_data))

def export_parent_child_to_neo4j(persons):
    with driver.session() as session:
        relationships = []
        for person in persons:
            for child in person.children:
                relationships.append({
                    'parent_personal_number': person.personal_number,
                    'child_personal_number': child.personal_number
                })

        query = """
        UNWIND $relationships AS rel
        MATCH (p:Person {personal_number: rel.parent_personal_number})
        MATCH (c:Person {personal_number: rel.child_personal_number})
        MERGE (p)-[:PARENT_OF]->(c)
        """

        session.write_transaction(lambda tx: tx.run(query, relationships=relationships))

def export_partners_to_neo4j(persons):
    with driver.session() as session:
        partners = []
        processed_pairs = set()

        for person in persons:
            if person.partner:
                pair = tuple(sorted([person.personal_number, person.partner.personal_number]))
                if pair not in processed_pairs:
                    processed_pairs.add(pair)
                    partners.append({
                        'p1_personal_number': person.personal_number,
                        'p2_personal_number': person.partner.personal_number
                    })

        query = """
        UNWIND $partners AS pair
        MATCH (p1:Person {personal_number: pair.p1_personal_number})
        MATCH (p2:Person {personal_number: pair.p2_personal_number})
        MERGE (p1)-[:PARTNER_OF]-(p2)
        """

        session.write_transaction(lambda tx: tx.run(query, partners=partners))

def export_activities_to_neo4j(persons):
    with driver.session() as session:
        activities = set()
        person_activities = []

        for person in persons:
            if person.activity:
                activities.add(person.activity)
                person_activities.append({
                    'personal_number': person.personal_number,
                    'activity_name': person.activity
                })

        # Create Activity nodes
        query_activities = """
        UNWIND $activities AS activity_name
        MERGE (:Activity {name: activity_name})
        """

        # Create relationships
        query_relationships = """
        UNWIND $person_activities AS pa
        MATCH (p:Person {personal_number: pa.personal_number})
        MATCH (a:Activity {name: pa.activity_name})
        MERGE (p)-[:ENGAGES_IN]->(a)
        """

        session.write_transaction(lambda tx: tx.run(query_activities, activities=list(activities)))
        session.write_transaction(lambda tx: tx.run(query_relationships, person_activities=person_activities))

def export_companies_to_neo4j(companies: pd.DataFrame) -> None:
    with driver.session() as session:
        companies_data = companies.to_dict('records')

        query = """
        UNWIND $companies AS company
        MERGE (c:Company {organisasjonsnummer: company.orgnr})
        SET c.navn = company.navn,
            c.organisasjonsform = company.organisasjonsform,
            c.registreringsdatoEnhetsregisteret = company.registreringsdatoEnhetsregisteret,
            c.antallAnsatte = company.antallAnsatte,
            c.forretningsadresse = company.forretningsadresse,
            c.stiftelsesdato = company.stiftelsesdato,
            c.vedtektsdato = company.vedtektsdato,
            c.vedtektsfestetFormaal = company.vedtektsfestetFormaal,
            c.aktivitet = company.aktivitet,
            c.links = company.links,
            c.sisteInnsendteAarsregnskap = company.sisteInnsendteAarsregnskap,
            c.kommune = company.kommune,
            c.overordnetEnhet = company.overordnetEnhet
        """

        session.write_transaction(lambda tx: tx.run(query, companies=companies_data))

def export_person_company_relationships_to_neo4j(persons):
    with driver.session() as session:
        employments = []
        for person in persons:
            if person.occupation:
                employments.append({
                    'personal_number': person.personal_number,
                    'company_name': person.occupation
                })

        query = """
        UNWIND $employments AS job
        MATCH (p:Person {personal_number: job.personal_number})
        MATCH (c:Company {navn: job.company_name})
        MERGE (p)-[:WORKS_AT]->(c)
        """

        session.write_transaction(lambda tx: tx.run(query, employments=employments))

def export_industrial_codes_to_neo4j(code_description: pd.DataFrame) -> None:
    with driver.session() as session:
        codes_data = code_description.to_dict('records')

        query = """
        UNWIND $codes AS code
        MERGE (i:IndustrialCode {Code: code.industrial_code})
        SET i.Description = code.description
        """

        session.write_transaction(lambda tx: tx.run(query, codes=codes_data))

def company_industrialCode_relationship(companies: pd.DataFrame) -> None:
    with driver.session() as session:
        relationships = companies[['orgnr', 'industrial_code']].dropna().to_dict('records')

        query = """
        UNWIND $relationships AS rel
        MATCH (c:Company {organisasjonsnummer: rel.orgnr})
        MATCH (i:IndustrialCode {Code: rel.industrial_code})
        MERGE (c)-[:BELONGS_TO]->(i)
        """

        session.write_transaction(lambda tx: tx.run(query, relationships=relationships))



# def export_persons_to_neo4j(persons):
#     with driver.session() as session:
#         for person in persons:
#             session.run(
#                 "CREATE (p:Person {personal_number: $personal_number, first_name: $first_name, family_name: $family_name, "
#                 "age: $age, sex: $sex, occupation: $occupation})",
#                 personal_number=person.personal_number,
#                 first_name=person.first_name,
#                 family_name=person.family_name,
#                 age=person.age,
#                 sex=person.sex,
#                 occupation=person.occupation
#             )

# def export_families_to_neo4j(families):
#     with driver.session() as session:
#         for family in families:
#             session.run(
#                 "CREATE (f:Family {family_id: $family_id})",
#                 family_id=family.id
#             )
#             for member in family.family_members:
#                 session.run(
#                     "MATCH (p:Person {personal_number: $personal_number}), (f:Family {family_id: $family_id}) "
#                     "CREATE (p)-[:MEMBER_OF_FAMILY]->(f)",
#                     personal_number=member.personal_number,
#                     family_id=family.id
#                 )

# def export_households_to_neo4j(households):
#     with driver.session() as session:
#         for household in households:
#             session.run(
#                 "CREATE (h:Household {household_id: $household_id, address: $address})",
#                 household_id=household.id,
#                 address=household.address
#             )
#             for member in household.members:
#                 session.run(
#                     "MATCH (p:Person {personal_number: $personal_number}), (h:Household {household_id: $household_id}) "
#                     "CREATE (p)-[:MEMBER_OF_HOUSEHOLD]->(h)",
#                     personal_number=member.personal_number,
#                     household_id=household.id
#                 )

# def export_parent_child_to_neo4j(persons):
#     with driver.session() as session:
#         for person in persons:
#             for child in person.children:
#                 session.run(
#                     "MATCH (p:Person {personal_number: $parent_personal_number}), (c:Person {personal_number: $child_personal_number}) "
#                     "CREATE (p)-[:PARENT_OF]->(c)",
#                     parent_personal_number=person.personal_number,
#                     child_personal_number=child.personal_number
#                 )

# def export_partners_to_neo4j(persons):
#     with driver.session() as session:
#         for person in persons:
#             if person.partner:
#                 session.run(
#                     "MATCH (p1:Person {personal_number: $p1_personal_number}), (p2:Person {personal_number: $p2_personal_number}) "
#                     "MERGE (p1)-[:PARTNER_OF]-(p2)",
#                     p1_personal_number=person.personal_number,
#                     p2_personal_number=person.partner.personal_number
#                 )

# def export_activities_to_neo4j(persons):
#     with driver.session() as session:
#         for person in persons:
#             if person.activity != None:  
#                 session.run(
#                     "MERGE (a:Activity {name: $activity_name})", 
#                     activity_name=person.activity
#                 )
#                 session.run(
#                     "MATCH (p:Person {personal_number: $personal_number}), (a:Activity {name: $activity_name}) "
#                     "CREATE (p)-[:ENGAGES_IN]->(a)",
#                     personal_number=person.personal_number,
#                     activity_name=person.activity
#                 )

# def export_companies_to_neo4j(companies:pd.DataFrame)->None:
#     with driver.session() as session:
#         for _, company in companies.iterrows():
#             session.run(
#                 "MERGE (c:Company {organisasjonsnummer: $organisasjonsnummer, navn: $navn, organisasjonsform: $organisasjonsform, "
#                 "registreringsdatoEnhetsregisteret: $registreringsdatoEnhetsregisteret, antallAnsatte: $antallAnsatte, "
#                 "forretningsadresse: $forretningsadresse, stiftelsesdato: $stiftelsesdato, vedtektsdato: $vedtektsdato, "
#                 "vedtektsfestetFormaal: $vedtektsfestetFormaal, aktivitet: $aktivitet, links: $links, "
#                 "sisteInnsendteAarsregnskap: $sisteInnsendteAarsregnskap, kommune: $kommune, overordnetEnhet: $overordnetEnhet})",
#                 organisasjonsnummer=company['orgnr'],
#                 navn=company['navn'],
#                 organisasjonsform=company['organisasjonsform'],
#                 registreringsdatoEnhetsregisteret=company['registreringsdatoEnhetsregisteret'],
#                 antallAnsatte=company['antallAnsatte'],
#                 forretningsadresse=company['forretningsadresse'],
#                 stiftelsesdato=company['stiftelsesdato'],
#                 vedtektsdato=company['vedtektsdato'],
#                 vedtektsfestetFormaal=company['vedtektsfestetFormaal'],
#                 aktivitet=company['aktivitet'],
#                 links=company['links'],
#                 sisteInnsendteAarsregnskap=company['sisteInnsendteAarsregnskap'],
#                 kommune=company['kommune'],
#                 overordnetEnhet=company['overordnetEnhet']
#             )

# def export_person_company_relationships_to_neo4j(persons):

#     with driver.session() as session:
#         for person in persons:
#             if person.occupation:  # Only create relationship if the person works
#                 session.run(
#                     "MATCH (p:Person {personal_number: $personal_number}), (c:Company {navn: $company_name}) "
#                     "CREATE (p)-[:WORKS_AT]->(c)",
#                     personal_number=person.personal_number,
#                     company_name=person.occupation
#                 )

# def export_idustrial_codes_to_neo4j(code_description:pd.DataFrame)->None:
#     with driver.session() as session:
#         for _, code in code_description.iterrows():
#             session.run(
#                 "CREATE (i:IndustrialCode {Code: $code, Description: $description})",
#                 code=code['industrial_code'],
#                 description=code['description']

#             )

# def company_industrialCode_relationship(company:pd.DataFrame)->None:

#     with driver.session() as session:
#         for _, c in company.iterrows():
            
#             session.run(
#             "MATCH(c:Company {organisasjonsnummer:$orgnr}), (i:IndustrialCode {Code: $industrial_code})"
#             "CREATE(c)-[:BELONGSTO]->(i)",
#             orgnr=c['orgnr'],
#             industrial_code=c['industrial_code']
#             )

# Function to export and save Cypher export to a file
def export_to_cypher_file():
    with driver.session() as session:
        # Run the export command with stream:true
        result = session.run("CALL apoc.export.cypher.all(null, {stream: true, useOptimizations: { type: 'UNWIND_BATCH', unwindBatchSize: 20 }}) YIELD cypherStatements RETURN cypherStatements")
        
        # Open a local file to write the export data with UTF-8 encoding
        with open("export.cypher", "w", encoding="utf-8") as f:
            for record in result:
                # Write each piece of streamed data to the file
                f.write(record["cypherStatements"] + "\n")

    print("Export completed and saved to export.cypher")

def import_from_cypher_file():
    with open("export.cypher", "r", encoding="utf-8") as f:
        cypher_statements = f.read()
    
    # Split the statements by semicolon if that's the delimiter used in your file
    statements = [stmt.strip() for stmt in cypher_statements.split(";") if stmt.strip()]
    total_statements = len(statements)
    print(f"Total statements to execute: {total_statements}")
    
    with driver.session() as session:
        try:
            # Execute statements in batches to manage memory and transaction size
            batch_size = 1000  # Adjust batch size as needed
            for i in range(0, total_statements, batch_size):
                batch = statements[i:i+batch_size]
                with session.begin_transaction() as tx:
                    for statement in batch:
                        tx.run(statement)
                    tx.commit()
                print(f"Executed statements {i+1} to {i+len(batch)}")
            print("Import completed successfully.")
        except Exception as e:
            print(f"An error occurred during import: {e}")


# def export_to_cypher_file():
#     with driver.session() as session:
#         result = session.run("""
#             CALL apoc.export.cypher.all(null, {
#                 stream: true,
#                 format: "cypher-shell",
#                 useOptimizations: { type: 'UNWIND_BATCH', unwindBatchSize: 20000 },
#                 includeSchema: true
#             }) YIELD cypherStatements
#             RETURN cypherStatements
#         """)
        
#         with open("export.cypher", "w", encoding="utf-8") as f:
#             for record in result:
#                 f.write(record["cypherStatements"] + "\n")

#     print("Export completed and saved to export.cypher")


if __name__ =="__main__":
    # Execute the function
    # export_to_cypher_file()
    import_from_cypher_file()
    # Close the driver connection
    driver.close()
