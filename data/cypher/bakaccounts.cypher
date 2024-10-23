
// // Create COMPANY bank accounts 
// MATCH (c:Company)
// WITH c, apoc.coll.randomItem(range(50000, 200000, 1000)) AS randomBalance
// CREATE (b:BankAccount {account_number: randomUUID(), balance: randomBalance, type: 'Company Account'})
// CREATE (c)-[:HAS_BANK_ACCOUNT]->(b);

// // Create PERSONAL bank accounts 
// MATCH (p:Person)
// WITH p, apoc.coll.randomItem(range(1000, 10000, 100)) AS randomBalance
// CREATE (b:BankAccount {account_number: randomUUID(), balance: randomBalance, type: 'Personal Account'})
// CREATE (p)-[:HAS_BANK_ACCOUNT]->(b);

// // Create JOINT bank accounts 
// MATCH (p1:Person)-[:PARTNER_OF]-(p2:Person)
// WHERE p1.personal_number < p2.personal_number
// WITH p1, p2, apoc.coll.randomItem(range(5000, 50000, 500)) AS randomBalance
// MERGE (b:BankAccount {account_key: p1.personal_number + '-' + p2.personal_number, type: 'Household Account'})
// ON CREATE SET b.balance = randomBalance, b.account_number = randomUUID()
// WITH p1, p2, b
// MERGE (p1)-[:HAS_BANK_ACCOUNT]->(b)
// MERGE (p2)-[:HAS_BANK_ACCOUNT]->(b);

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Script 1: Bank Accounts Creation

// Create Bank Nodes
MERGE (bankA:Bank {name: 'Bank A'})
MERGE (bankB:Bank {name: 'Bank B'})
MERGE (bankC:Bank {name: 'Bank C'})

// Assign Bank Accounts to Companies
MATCH (c:Company)
WITH c, apoc.coll.randomItem([bankA, bankB, bankC]) AS bank,
     apoc.coll.randomItem(range(50000, 200000, 5000)) AS randomBalance
CREATE (account:BankAccount {
  account_number: apoc.create.uuid(),
  balance: randomBalance,
  type: 'Company Account'
})
CREATE (c)-[:HAS_BANK_ACCOUNT]->(account)
CREATE (account)-[:ACCOUNT_OF]->(bank)

// Assign Personal Bank Accounts to Individuals
MATCH (p:Person)
WITH p, apoc.coll.randomItem([bankA, bankB, bankC]) AS bank,
     apoc.coll.randomItem(range(1000, 10000, 500)) AS randomBalance
CREATE (account:BankAccount {
  account_number: apoc.create.uuid(),
  balance: randomBalance,
  type: 'Personal Account'
})
CREATE (p)-[:HAS_BANK_ACCOUNT]->(account)
CREATE (account)-[:ACCOUNT_OF]->(bank)

// Assign Joint Bank Accounts to Partners
MATCH (p1:Person)-[:PARTNER_OF]-(p2:Person)
WHERE id(p1) < id(p2)  // Avoid duplicates
WITH p1, p2, apoc.coll.randomItem([bankA, bankB, bankC]) AS bank,
     apoc.coll.randomItem(range(5000, 50000, 1000)) AS randomBalance
MERGE (account:BankAccount {
  account_key: id(p1) + '-' + id(p2),
  type: 'Joint Account'
})
ON CREATE SET account.balance = randomBalance,
              account.account_number = apoc.create.uuid()
MERGE (p1)-[:HAS_BANK_ACCOUNT]->(account)
MERGE (p2)-[:HAS_BANK_ACCOUNT]->(account)
CREATE (account)-[:ACCOUNT_OF]->(bank)
