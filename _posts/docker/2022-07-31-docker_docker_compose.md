---
layout: post
title:  "Docker - Docker Compose"
author: dani
categories: [ Docker, Docker Compose]
image: assets/images/docker/docker-compose.png
---

As an automation tester, I want run multi-container Docker application easily. To do that, I need to use the `Docker Compose` to run the multi-container with the `YAML` file.

<blockquote
>Note: Basically, the Docker Compose is existed in Docker Desktop.
</blockquote>

## Prerequisite

- [Docker is installed](/docker_installation/)

## Install Compose plugin

- (Mac, Win, Linux) Docker Desktop: If you have Desktop installed then you already have the Compose plugin installed.
- Linux systems: To install the Docker CLI’s Compose plugins use one of these methods of installation:
  - Using the convenience scripts offered per Linux distro from the Engine install section.
  - Setting up Docker’s repository and using it to install the compose plugin package.
  - Other scenarios, check the Linux install.
- Windows Server: If you want to run the Docker daemon and client directly on Microsoft Windows Server, follow the Windows Server install instructions.
  
## Run the first Docker Compose

To run the first Docker Compose, we can following these steps.

- Create new file `docker-compose.yml` with below content
  
```js
version: "3"
services:
  chrome:
    image: selenium/node-chrome:4.0.0-rc-1-prerelease-20210618
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
    image: selenium/node-firefox:4.0.0-rc-1-prerelease-20210618
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
    image: selenium/hub:4.0.0-rc-1-prerelease-20210618
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"
```

- Access the folder contain the new file and run the command

```js
  docker compose up
```

- After the setting up is done, we access the url <http://localhost:4444/ui/index.html> to verify it is run correctly.

## Video guide

<iframe
    width="640"
    height="480"
    src="https://www.youtube.com/embed/5-ku4oWZMIc"
    frameborder="10"
    allow="autoplay; encrypted-media"
    allowfullscreen
>
</iframe>
