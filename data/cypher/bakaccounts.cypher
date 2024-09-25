
// Create COMPANY bank accounts 
MATCH (c:Company)
WITH c, apoc.coll.randomItem(range(50000, 200000, 1000)) AS randomBalance
CREATE (b:BankAccount {account_number: randomUUID(), balance: randomBalance, type: 'Company Account'})
CREATE (c)-[:HAS_BANK_ACCOUNT]->(b);

// Create PERSONAL bank accounts 
MATCH (p:Person)
WITH p, apoc.coll.randomItem(range(1000, 10000, 100)) AS randomBalance
CREATE (b:BankAccount {account_number: randomUUID(), balance: randomBalance, type: 'Personal Account'})
CREATE (p)-[:HAS_BANK_ACCOUNT]->(b);

// Create JOINT bank accounts 
MATCH (p1:Person)-[:PARTNER_OF]-(p2:Person)
WHERE p1.personal_number < p2.personal_number
WITH p1, p2, apoc.coll.randomItem(range(5000, 50000, 500)) AS randomBalance
MERGE (b:BankAccount {account_key: p1.personal_number + '-' + p2.personal_number, type: 'Household Account'})
ON CREATE SET b.balance = randomBalance, b.account_number = randomUUID()
WITH p1, p2, b
MERGE (p1)-[:HAS_BANK_ACCOUNT]->(b)
MERGE (p2)-[:HAS_BANK_ACCOUNT]->(b);

