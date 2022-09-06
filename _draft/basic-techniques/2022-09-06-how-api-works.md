---
layout: post
title:  "How API works"
author: toronto22
categories: [ automation test, api testing]
image: assets/images/basic-technique/api-testing.png
---

As an automation tester, I want to be able to test APIs. To do that, I have to understand about what is an API and how does it work. 

## What is an API
API stands for application programming interface. It is the way for two or more computer program communicate with each other. It is also a type of software interface, offering a service to other pieces of software. 
In the real project, we can see the API is the part that help server connect to client application (web application, mobile application) or connect between 2 or more services (microservices system).

## Types of API

There are many types of API in real life, but we mostly test only those two:
- [Rest APIs](https://restfulapi.net/)
- [Soap]()  

The article will not solve the question `what is the difference between SOAP and REST APIs, and which one is right for my project?`. It just list out the existing types of API. (We can find it solution [here](https://www.soapui.org/learn/api/soap-vs-rest-api/))

## How it works (Interm of testing)

### Rest APIs (Restful API)
There are two part of an Rest APIs that is consist of `resquest` and `response`. The data we send called `request`, the data sent back to our is `response`. 

A request is made up by four things:
- The endpoint
- The method
- The headers
- the body

The endpoint is the URL of our request. It have 2 part is `base URL` and `path`. 

Base url is the consistent part of the root of the endpoint. The Base url will be the same in the APIs of one service.

Path is the remaining part given after base URL.

//TODO
