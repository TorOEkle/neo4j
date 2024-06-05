from neo4j import GraphDatabase

# Connect to Neo4j database
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123456789"))

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
                    "MERGE (a:Activity {name: $activity_name})",  # Use MERGE to avoid duplicate Activity nodes
                    activity_name=person.activity
                )
                session.run(
                    "MATCH (p:Person {personal_number: $personal_number}), (a:Activity {name: $activity_name}) "
                    "CREATE (p)-[:ENGAGES_IN]->(a)",
                    personal_number=person.personal_number,
                    activity_name=person.activity
                )
