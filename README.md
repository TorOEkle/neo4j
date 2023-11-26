# Docker + Neo4j
Very easy to get started. Install podman or docker on your computer
```bash
podman pull neo4j:latest
```

``` bash
podman run \   
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -d \
  -e NEO4J_AUTH=neo4j/CapgeminiSVG \
  neo4j:latest
```

``` bash
docker run \
    --name neo4j_tor \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4JLABS_PLUGINS='["apoc", "n10s"]' \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
```
Then Neo4j is available on <http://localhost:7474/>
