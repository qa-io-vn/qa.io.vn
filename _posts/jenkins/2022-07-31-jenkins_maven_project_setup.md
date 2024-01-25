---
layout: post
title:  "Jenkins - Maven project setup"
author: dani
categories: [ Jenkins, CICD]
image: assets/images/jenkins/jenkins-banner.png
---

As an automation tester, I want to use Jenkins tools to setup my CICD job for my Maven Project. But the Jenkins is not support Maven project indefault. Therefore, I need to setup Jenkins to able to work with me Jenkins project

## Jenkins - Setup Maven

To setup Maven:

- Access `Dashboard > Manage Jenkins > Plugin > Available Plugin` and install `Maven Integration` plugin
- Access `Dashboard > Manage Jenkins > Tools` and move to `Maven` section
  - Click on `Add maven`
  - Input maven name (any name) that will be use in the Jenkinsfile (Example `maven 'maven'` for the name is `maven`)
  - Select the maven version (any version that adapt with our project)
  - Click `Save`

## Jenkins - Use Maven on Jenkins Pipeline Project

In Jenkinsfile, if the maven name is `maven`, we will use the tool is `maven 'maven'` to use the Maven on our project. Then, in the `stage`, we can run the project with the command `mvn clean install` as in the example.

`Jenkinsfile` sample:

```js
pipeline {
     agent any

     tools{
         maven 'maven'
     }

     stages {
         stage('Tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    sh 'mvn clean install'
                }
            }
         }

        //....
     }
 }
```
