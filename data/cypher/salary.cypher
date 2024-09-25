// Iterate over each company and its employees
MATCH (c:Company)<-[:WORKS_AT]-(e:Person)
MATCH (c)-[:HAS_BANK_ACCOUNT]->(cb:BankAccount),
      (e)-[:HAS_BANK_ACCOUNT]->(eb:BankAccount)
WITH c, e, cb, eb, rand() * (60000 - 45000) + 10000 AS salary
CREATE (t:Transaction {amount: round(salary), date: date(), description: 'Monthly Salary'})
CREATE (cb)-[:SENDS_SALARY]->(t)-[:TO_EMPLOYEE]->(eb)
WITH cb, eb, t
SET cb.balance = cb.balance - t.amount,
    eb.balance = eb.balance + t.amount;
