---
layout: post
title:  "Selenium Grid - Installation"
author: toronto22
categories: [ Jenkins, CICD]
image: assets/images/selenium-grid/selenium-grid-basic.jpg
---

As an automation tester, I want to execute my UI test script on remote browser. To do that, I need to install Selenium Grid which help me to execute my test script easily throw remote browsers.
## Install Selenium Grid on Docker
To install Selnium Grid on Docker, we have to install Docker first. After that, we can easily install Selenium Grid by `Docker Compose`:

- Create `docker-compose.yml` file with content (Or download [here](../resources/docker-compose/selenium-grid/docker-compose.yml)):
```js
version: "3"
services:
  chrome:
    image: selenium/node-chrome:latest
    volumes:
      - /dev/shm:/dev/shm
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_OVERRIDE_MAX_SESSIONS=true
      - SE_NODE_MAX_SESSIONS=10

  firefox:
    image: selenium/node-firefox:latest
    volumes:
      - /dev/shm:/dev/shm
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_OVERRIDE_MAX_SESSIONS=true
      - SE_NODE_MAX_SESSIONS=10     
  edge:
    image: selenium/node-firefox:latest
    volumes:
      - /dev/shm:/dev/shm
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_OVERRIDE_MAX_SESSIONS=true
      - SE_NODE_MAX_SESSIONS=10   
 
  selenium-hub:
    image: selenium/hub:latest
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"
```
- Open commandline and access to folder contain the `docker-compose.yml` file and execute the command 

```js
docker-compose up
```

- After the command is finished, Open browser (Chrome browser) and access URL: `localhost:4444`. The Selenium Hub Site is expected to display.



