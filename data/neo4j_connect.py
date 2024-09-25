from neo4j import GraphDatabase
import pandas as pd

NEO4J_URI="bolt://localhost:7687"#"neo4j+s://1fb1cc99.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="123456789"#"XFlYW2mLk4lErhhF0En15j4_ZME5fTbn4_uyaw-Tr-E"
AURA_INSTANCEID="1fb1cc99"
AURA_INSTANCENAME="Instance01"

# Connect to Neo4j database
uri = NEO4J_URI
driver = GraphDatabase.driver(uri, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def export_persons_to_neo4j(persons):
    with driver.session() as session:
        for person in persons:
            session.run(
                "CREATE (p:Person {personal_number: $personal_number, first_name: $first_name, family_name: $family_name, "
                "age: $age, sex: $sex, occupation: $occupation})",
                personal_number=person.personal_number,
                first_name=person.first_name,
                family_name=person.family_name,
                age=person.age,
                sex=person.sex,
                occupation=person.occupation
            )

def export_families_to_neo4j(families):
    with driver.session() as session:
        for family in families:
            session.run(
                "CREATE (f:Family {family_id: $family_id})",
                family_id=family.id
            )
            for member in family.family_members:
                session.run(
                    "MATCH (p:Person {personal_number: $personal_number}), (f:Family {family_id: $family_id}) "
                    "CREATE (p)-[:MEMBER_OF_FAMILY]->(f)",
                    personal_number=member.personal_number,
                    family_id=family.id
                )

def export_households_to_neo4j(households):
    with driver.session() as session:
        for household in households:
            session.run(
                "CREATE (h:Household {household_id: $household_id, address: $address})",
                household_id=household.id,
                address=household.address
            )
            for member in household.members:
                session.run(
                    "MATCH (p:Person {personal_number: $personal_number}), (h:Household {household_id: $household_id}) "
                    "CREATE (p)-[:MEMBER_OF_HOUSEHOLD]->(h)",
                    personal_number=member.personal_number,
                    household_id=household.id
                )

def export_parent_child_to_neo4j(persons):
    with driver.session() as session:
        for person in persons:
            for child in person.children:
                session.run(
                    "MATCH (p:Person {personal_number: $parent_personal_number}), (c:Person {personal_number: $child_personal_number}) "
                    "CREATE (p)-[:PARENT_OF]->(c)",
                    parent_personal_number=person.personal_number,
                    child_personal_number=child.personal_number
                )

def export_partners_to_neo4j(persons):
    with driver.session() as session:
        for person in persons:
            if person.partner:
                session.run(
                    "MATCH (p1:Person {personal_number: $p1_personal_number}), (p2:Person {personal_number: $p2_personal_number}) "
                    "MERGE (p1)-[:PARTNER_OF]->(p2)",
                    p1_personal_number=person.personal_number,
                    p2_personal_number=person.partner.personal_number
                )
                session.run(
                    "MATCH (p1:Person {personal_number: $p1_personal_number}), (p2:Person {personal_number: $p2_personal_number}) "
                    "MERGE (p2)-[:PARTNER_OF]->(p1)",
                    p1_personal_number=person.personal_number,
                    p2_personal_number=person.partner.personal_number
                )

def export_activities_to_neo4j(persons):
    with driver.session() as session:
        for person in persons:
            if person.activity != None:  
                session.run(
                    "MERGE (a:Activity {name: $activity_name})", 
                    activity_name=person.activity
                )
                session.run(
                    "MATCH (p:Person {personal_number: $personal_number}), (a:Activity {name: $activity_name}) "
                    "CREATE (p)-[:ENGAGES_IN]->(a)",
                    personal_number=person.personal_number,
                    activity_name=person.activity
                )

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

def export_person_company_relationships_to_neo4j(persons):

    with driver.session() as session:
        for person in persons:
            if person.occupation:  # Only create relationship if the person works
                session.run(
                    "MATCH (p:Person {personal_number: $personal_number}), (c:Company {navn: $company_name}) "
                    "CREATE (p)-[:WORKS_AT]->(c)",
                    personal_number=person.personal_number,
                    company_name=person.occupation
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