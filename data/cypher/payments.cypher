

// Define Time Span
WITH date('2020-01-01') AS startDate, date('2023-12-31') AS endDate

// Define Expense Categories and Merchants
WITH startDate, endDate,
     [
       {category: 'Groceries', merchants: ['Whole Foods', 'Trader Joe\'s', 'Walmart'], avgAmount: 150},
       {category: 'Utilities', merchants: ['Comcast', 'Verizon', 'AT&T'], avgAmount: 100},
       {category: 'Entertainment', merchants: ['Netflix', 'Spotify', 'Hulu'], avgAmount: 15},
       {category: 'Dining', merchants: ['McDonald\'s', 'Starbucks', 'Chipotle'], avgAmount: 30},
       {category: 'Clothing', merchants: ['Gap', 'Uniqlo', 'H&M'], avgAmount: 80}
     ] AS expenseCategories

// Generate Expenses for Each Person
MATCH (p:Person)-[:HAS_BANK_ACCOUNT]->(account:BankAccount)
UNWIND expenseCategories AS expense
UNWIND range(0, duration.inDays(startDate, endDate).days) AS dayOffset
WITH p, account, expense, startDate.plusDays(dayOffset) AS expenseDate
WHERE rand() < 0.05  // 5% chance of making an expense each day per category
WITH p, account, expense, expenseDate,
     apoc.coll.randomItem(expense.merchants) AS merchant,
     round(expense.avgAmount * (0.5 + rand())) AS amount  // Amount varies ±50%
CREATE (t:Transaction {
  amount: amount,
  date: date(expenseDate),
  description: expense.category + ' at ' + merchant
})
CREATE (account)-[:SENDS_MONEY]->(t)
SET account.balance = account.balance - amount
