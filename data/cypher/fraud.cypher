// Assign a temporary label to 100 randomly selected persons
MATCH (p:Person)
WHERE p.age > 20
WITH p
ORDER BY rand()
LIMIT 100
SET p:SelectedForFraudAnalysis  
RETURN count(p) as SelectedCount




// Random large transfers between persons
WITH 10 as amount, 2017 as startYear, 2021 as endYear
WITH range(1, amount) as xx, startYear, (endYear - startYear) as yearRange
UNWIND xx as x
WITH date({
  year:toInteger(1+startYear+floor(rand()*yearRange)), 
  month:toInteger(1+floor(rand()*12)), 
  day:toInteger(1+floor(rand()*27))
}) as randomDate

MATCH (p1:Person)-[:PARTNER_OF]-(p2:Person),
      (p1)-[:HAS_BANK_ACCOUNT]->(b:BankAccount {type: 'Household Account'})
WITH p1, p2, b, rand() * 15000 + 10000 AS largePayment, randomDate
CREATE (t:Transaction {amount: largePayment, date: randomDate, description: 'Suspicious large payment to joint account'})
CREATE (b)-[:RECEIVES_MONEY]->(t);



//Many Small Transactions Between the Same Accounts
WITH 20 as amount, 2017 as startYear, 2021 as endYear
WITH range(1, amount) as xx, startYear, (endYear - startYear) as yearRange
UNWIND xx as x
WITH date({
  year: toInteger(1 + startYear + floor(rand()*yearRange)), 
  month: toInteger(1 + floor(rand()*12)), 
  day: toInteger(1 + floor(rand()*27))
}) as randomDate

MATCH (p1:Person)-[:HAS_BANK_ACCOUNT]->(b1:BankAccount {type: 'Personal Account'}),
      (p2:Person)-[:HAS_BANK_ACCOUNT]->(b2:BankAccount {type: 'Personal Account'})
WHERE p1 <> p2 AND NOT (p1)-[:PARTNER_OF]-(p2) AND NOT (p1)-[:PARENT_OF]-(p2)
WITH p1, p2, b1, b2, randomDate, 50 + rand() * 100 AS smallAmount
CREATE (t:Transaction {amount: smallAmount, date: randomDate, description: 'Repeated small transfer'})
CREATE (b1)-[:SENDS_MONEY]->(t)-[:RECEIVES_MONEY]->(b2);



// Start the unified transaction script
CALL {
  // Select 100 persons who are over 20 years old
  MATCH (p:Person)
  WHERE p.age > 20
  WITH p
  ORDER BY rand()
  LIMIT 100
  WITH collect(p) as selectedPersons
  RETURN selectedPersons
}

// Scenario 1: Proxy using a child
CALL {
  WITH selectedPersons
  UNWIND selectedPersons AS p1
  UNWIND selectedPersons AS p2
  WITH p1, p2, 
  WHERE p1 <> p2
  OPTIONAL MATCH (p2)-[:PARENT_OF]->(c:Person)-[:HAS_BANK_ACCOUNT]->(cb:BankAccount),
                (p1)-[:HAS_BANK_ACCOUNT]->(pb1:BankAccount),
                (p2)-[:HAS_BANK_ACCOUNT]->(pb2:BankAccount)
  WITH p1, pb1, pb2, c, cb,
       date({
         year: toInteger(2017 + floor(rand()*5)),
         month: toInteger(1 + floor(rand()*12)),
         day: toInteger(1 + floor(rand()*27))
       }) as randomDate
  WITH p1, pb1, pb2, c, cb, randomDate, 1000 + rand() * 5000 AS proxyAmount
  CREATE (t1:Transaction {amount: proxyAmount, date: randomDate, description: 'To child proxy'})
  CREATE (t2:Transaction {amount: proxyAmount, date: randomDate, description: 'from proxy to sender'})
  CREATE (pb1)-[:SENDS_MONEY]->(t1)-[:RECEIVES_MONEY]->(cb),
        (cb)-[:SENDS_MONEY]->(t2)-[:RECEIVES_MONEY]->(pb2)
  RETURN count(t1) as ProxyTransactions
}

// Scenario 2: Small transactions over multiple days
CALL {
  WITH selectedPersons
  UNWIND selectedPersons AS p1
  UNWIND selectedPersons AS p2
  WITH p1, p2,
       date({
         year: toInteger(2017 + floor(rand()*5)),
         month: toInteger(1 + floor(rand()*12)),
         day: toInteger(1 + floor(rand()*27))
       }) as startDate WHERE p1 <> p2,
  MATCH (p1)-[:HAS_BANK_ACCOUNT]->(b1:BankAccount),
        (p2)-[:HAS_BANK_ACCOUNT]->(b2:BankAccount)
  UNWIND range(1, 5) AS idx
  WITH p1, b1, b2, startDate, idx, 50 + rand() * 100 AS smallAmount
  CREATE (t:Transaction {
    amount: smallAmount,
    date: date(startDate + duration('P' + idx + 'D')),  // Adds days sequentially
    description: 'Structuring over days'
  })
  CREATE (b1)-[:SENDS_MONEY]->(t),
        (t)-[:RECEIVES_MONEY]->(b2)
  RETURN count(t) as SmallTransactions
}

// Scenario 3: Large Transactions
CALL {
  WITH selectedPersons
  UNWIND selectedPersons AS p1
  UNWIND selectedPersons AS p2
  WITH p1, p2, 
       date({
         year: toInteger(2017 + floor(rand()*5)),
         month: toInteger(1 + floor(rand()*12)),
         day: toInteger(1 + floor(rand()*27))
       }) as randomDate,WHERE p1 <> p2
       
  MATCH (p1)-[:HAS_BANK_ACCOUNT]->(b1:BankAccount),
        (p2)-[:HAS_BANK_ACCOUNT]->(b2:BankAccount)
  WITH p1, p2, b1, b2, randomDate, 5000 + rand() * 15000 AS largeAmount
  CREATE (t:Transaction {amount: largeAmount, date: randomDate, description: 'Large suspicious transaction'})
  CREATE (b1)-[:SENDS_MONEY]->(t),
        (t)-[:RECEIVES_MONEY]->(b2)
  RETURN count(t) as LargeTransactions
}

