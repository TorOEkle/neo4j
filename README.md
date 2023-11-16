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
