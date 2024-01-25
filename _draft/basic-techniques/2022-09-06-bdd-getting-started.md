---
layout: post
title:  "How API works"
author: dani
categories: [ automation test, api testing]
image: assets/images/basic-technique/api-testing.png
---

As an automation tester, I want to be able to test APIs. To do that, I have to understand about what is an API and how does it work.

## What is an API

API stands for application programming interface. It is the way for two or more computer program communicate with each other. It is also a type of software interface, offering a service to other pieces of software.

In the real project, we can see the API is the part of the system that help server connect to client application (web application, mobile application) or connect between 2 or more services (microservices system, 3nd party services).

## Types of API

There are many types of API in real life, but we mostly test only those two:

- [Rest APIs](https://restfulapi.net/)
- Soap

The article will not solve the question `what is the difference between SOAP and REST APIs, and which one is right for my project?`. It just list out the existing types of API. (We can find it solution [here](https://www.soapui.org/learn/api/soap-vs-rest-api/))

## How it works (Interm of testing)

### Rest APIs (Restful API)

There are two part of an Rest APIs that is consist of `resquest` and `response`. The data we send called `request`, the data sent back to our is `response`.

#### `Request`

A request is made up by four things:

- The endpoint
- The method
- The headers
- the body

Interm of testing, we have to understand about those things to be able to use APIs in the right way. The expectation is about we can call the APIs throw PostMan (API testing tools) with the request information.

`The endpoint` The endpoint is the URL that contains some information of request like `Base URL`, `Path`. Beside, we have `Query string parameters` that is query string of `the endpoint` after the `?` and it is the set of key-value pairs.

Example:

```js
    Endpoint: www.our-domain.com/surfreport?days=3&units=metric&time=1400
    Baseurl: www.our-domain.com
    Path: /surfreport
    Query string parameters: days=3&units=metric&time=1400 (Set of 3 key-value pairs)
```

`The method`: Is mandatory information for APIs, and it consists of:

- POST: usually for create
- GET: usually for read
- PUT: usually for update/replace
- PATCH: usually for partial update/modify
- DELETE: usually for delete

> **_NOTE:_**  feature of method is just theory, so we still can see an get API that be able to delete or create data.

`The header`: Contains the data for the request in list of key-value pair. I usually contain some kinds of data like authentication, content-type.

`The body`: Contains the data for the request like the header but the data will be `XML` or `Json` type.

#### `Response`

In term of testing, we focus on the `status code` and `respone body` to verify the logic of APIs.

`status code`: It is the information of the `response`. Base on that, we can know the request is call successfully or fail.

list status code(from wiki):

- 1xx informational response – the request was received, continuing process
- 2xx successful – the request was successfully received, understood, and accepted
- 3xx redirection – further action needs to be taken in order to complete the request
- 4xx client error – the request contains bad syntax or cannot be fulfilled
- 5xx server error – the server failed to fulfil an apparently valid request

`response body`: Is the data that we getting back after call the APIs.The data will be in `XML` or `Json` type. In testing, we focus on verify this data to make sure the APIs going well.

### SOAP

//TODO