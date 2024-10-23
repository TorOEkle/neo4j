# Define Neo4j credentials
$username = "neo4j"
$password = "123456789"

# Define the path to cypher-shell
$cypherShellPath = "C:\Users\dgronner\.Neo4jDesktop\relate-data\dbmss\dbms-e075c79d-64e5-426e-b671-91f70ffdcd76\bin"

# Define the list of scripts
$scripts = @(
  "../cypher/bakaccounts.cypher",
  "../cypher/salary.cypher",
  "../cypher/payments.cypher",
  "../cypher/fraud.cypher"
)

foreach ($script in $scripts) {
  Write-Host "Running $script..."
  & $cypherShellPath -u $username -p $password -f $script
}
