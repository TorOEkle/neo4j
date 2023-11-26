# Use the official Neo4j image as a base
FROM neo4j:latest

# Set an environment variable with the version of APOC
ENV APOC_VERSION 4.3.0.0

# Download the APOC plugin
ADD https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.3.0.0/apoc-$APOC_VERSION-all.jar /plugins
