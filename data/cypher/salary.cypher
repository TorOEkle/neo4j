// // Iterate over each company and its employees
// MATCH (c:Company)<-[:WORKS_AT]-(e:Person)
// MATCH (c)-[:HAS_BANK_ACCOUNT]->(cb:BankAccount),
//       (e)-[:HAS_BANK_ACCOUNT]->(eb:BankAccount)
// WITH c, e, cb, eb, rand() * (60000 - 45000) + 10000 AS salary
// CREATE (t:Transaction {amount: round(salary), date: date(), description: 'Monthly Salary'})
// CREATE (cb)-[:SENDS_SALARY]->(t)-[:TO_EMPLOYEE]->(eb)
// WITH cb, eb, t
// SET cb.balance = cb.balance - t.amount,
//     eb.balance = eb.balance + t.amount;
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Define Time Span
WITH date('2020-01-01') AS startDate, date('2023-12-31') AS endDate
WITH apoc.date.parse(startDate.toString(), 'ms', 'yyyy-MM-dd') AS startMs,
     apoc.date.parse(endDate.toString(), 'ms', 'yyyy-MM-dd') AS endMs,
     duration.inMonths(startDate, endDate).months AS totalMonths

// Generate Salary Payments for Each Month
UNWIND range(0, totalMonths) AS monthOffset
WITH startDate.plusMonths(monthOffset) AS payDate
WHERE payDate <= endDate
WITH payDate, apoc.date.endOfMonth(payDate.toString(), 'ms') AS salaryDate
MATCH (c:Company)<-[:WORKS_AT]-(e:Person)
MATCH (c)-[:HAS_BANK_ACCOUNT]->(companyAccount:BankAccount),
      (e)-[:HAS_BANK_ACCOUNT]->(employeeAccount:BankAccount)
WITH c, e, companyAccount, employeeAccount, payDate,
     CASE e.role
       WHEN 'Manager' THEN apoc.coll.randomItem(range(70000, 90000, 5000))
       WHEN 'Engineer' THEN apoc.coll.randomItem(range(50000, 70000, 5000))
       ELSE apoc.coll.randomItem(range(30000, 50000, 5000))
     END AS salary
CREATE (t:Transaction {
  amount: salary,
  date: date(payDate),
  description: 'Monthly Salary'
})
CREATE (companyAccount)-[:SENDS_SALARY]->(t)-[:RECEIVES_SALARY]->(employeeAccount)
SET companyAccount.balance = companyAccount.balance - salary,
    employeeAccount.balance = employeeAccount.balance + salary
