---
layout: post
title:  "Jenkins - Installation"
author: dani
categories: [ Jenkins, CICD]
image: assets/images/jenkins/jenkins-banner.png
---

As an automation tester, I want to use Jenkins tools to setup my CICD job. To do that, I need to install the jenkins tools.

## Install Jenkins on local machine - Windows

- Access [link](https://www.jenkins.io/download/) and download the jenkins.war file.
- Open up a terminal/command prompt window to the download directory.
- Run the command `java -jar jenkins.war` and get `key` in the command log (Example: eb09c7a30b814164a0be806dd126f39a)
- Browse to `http://localhost:8080` and enter the `key` into `Administrator password` field and click Continue.
- Click on `Install suggested plugins` and wait for the setup is done.
- Finish the installation and start using Jenkins

## Install Jenkins on docker

- Docker is installed
- Run the command `docker run -p 8080:8080 -p 50000:50000 --restart=on-failure jenkins/jenkins:lts-jdk11` and get `key` in the command log
- Browse to `http://localhost:8080` and enter the `key` into `Administrator password` field and click Continue.
- Click on `Install suggested plugins` and wait for the setup is done.
- Finish the installation and start using Jenkins
