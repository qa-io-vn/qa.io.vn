---
layout: post
title:  "Jenkins - Allure Report Setup"
author: dani
categories: [ Jenkins, CICD, Allure report, Java, Maven]
image: assets/images/jenkins/jenkins-banner.png
---

As an automation tester, I want to use Jenkins tools to setup my CICD job that is integrated with Allure report. To do that, I need to install the Allure report tool on jenkins.

## Install Jenkins Allure Report

Install Allure Report:

- Access `Dashboard > Manage Jenkins > Plugin > Available Plugin` and install `Allure` plugin
- Access `Dashboard > Manage Jenkins > Tools` and move to `Allure Commandline` section
  - Click on `Add Allure Commandline`
  - Input maven name (recommend name: `allure`) that will be use in the Jenkinsfile (Example `maven 'allure'` for the name is `allure`)
  - Select the allure report version (any version that adapt with our project)
  - Click `Save`

## How to use Allure Report on Jenkins Pipeline project

To use Allure Report on our project, we can add new stage `reports` in `Jenkinsfile` and add following steps to get the report on Jenkins results.

Jenkinsfile sample:

 ```js
 pipeline {
    //...
     stages {
         stage('Tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    sh 'mvn clean install'
                }
            }
         }

         stage('reports') {
             steps {
                 script {
                         allure([
                                 includeProperties: false,
                                 jdk: '',
                                 properties: [],
                                 reportBuildPolicy: 'ALWAYS',
                                 results: [[path: 'target/allure-results']]
                         ])
                 }
             }
         }
     }
 }```
