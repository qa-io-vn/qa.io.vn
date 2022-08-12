---
layout: post
title:  "Docker - Getting started"
author: toronto22
categories: [ UI, Automation testing tools]
image: assets/images/6.jpg
---

As an automation tester, I want to istall tools easily and it will be not diffirent between machines. To do that, I have to you Docker to install that tools.

## Why Docker?

- Docker For Everyone
- Environment Isolation
- OS Independent Apps
- Rapid Development & Deployment
- Scalability & Flexibility Made Easier
- No More Security Issues
- Ship Anytime, Anywhere
- Dependency Management Made Easier

## What is Docker?

Docker is a tool designed to make it easier for developers to develop, ship, and run applications by using containers. Containers allow devs to package an application with all of its requirements and configurations, such as libraries and other dependencies and deploy it as a single package.

## How to install Docker Desktop

Docker Desktop is developer productivity tools and a local Kubernetes environment. To install it, we following these steps:

- Access <https://www.docker.com/get-started/>
- Download Docker Desktop for our operating system.
- Install that Docker with downloaded file
- Start Docker application and finish the setup

## Install the first Docker container

As an automation tester, I want to install Jenkins server to setup my CICD jobs. To do that, I need to install the server with Docker Destop by using the command:

```js
docker run -p 8080:8080 -p 50000:50000 --restart=on-failure jenkins/jenkins:lts-jdk11
```

After the command line is executed completely, we can verify that by access <http://localhost:8080/>. If the jenkins site is shown, the Docker contaner is installed successfully.

## Video guide (Click on Image to view video)

<iframe
    width="640"
    height="480"
    src="https://www.youtube.com/embed/CGGGqbBWKRI"
    frameborder="10"
    allow="autoplay; encrypted-media"
    allowfullscreen
>
</iframe>
