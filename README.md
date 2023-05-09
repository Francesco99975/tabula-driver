# [Docker Image Here](https://hub.docker.com/r/kalairen/tabula-driver)

# How does it work

- This image is meant to be used in tandem with kalairen/tabula on the same docker network.
- At this stage custom ports are not available, there fore know that the driver image runs on port 9888 and tabula on port 9889. Be sure to name the tabula container: _tabula_; so that the python serve can be able to properly communicate with tabula.
- This server has only a **POST** route: _/pdf_, that takes in a PDF file and responds with a zip file of CSVs of all the detected tables by the tabula server.

# Docker Compose

- _docker-compose.yml_

```
version: "3"

networks:
  tabunet:
    driver: bridge

services:
  tabula-driver:
    container_name: tabula-driver
    image: kalairen/tabula-driver
    ports:
      - "9888:9888"
    networks:
      - tabunet
    depends_on:
      - tabula
  tabula:
    container_name: tabula
    image: kalairen/tabula
    networks:
      - tabunet
```
