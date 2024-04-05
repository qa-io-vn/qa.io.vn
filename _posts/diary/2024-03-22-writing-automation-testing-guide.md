---
layout: post
title:  "Writing automation testing guide"
author: dani
categories: [ diary ]
image: assets/images/plan/plan-dice-760.jpg
---


This article provides a roadmap for getting started with automation testing, aimed at beginners including manual testers and developers. It outlines the benefits of automation testing while acknowledging its limitations. We'll explore the core concepts and gradually build a foundation for writing high-quality, sustainable test scripts.

## What is Automation Testing?

### Automation testing mimics manual testing by simulating user interactions with an application.  Here's how it elevates the testing process

- Speed and Efficiency: Automation executes tests significantly faster than manual testing, eliminating human error.
Continuous Integration: Tests can be run frequently, even outside of standard working hours, for comprehensive regression testing.
- Reduced Effort: Once a script is implemented, rerunning it requires minimal effort, freeing up time for higher-level testing tasks.
- Living Documentation: By following Behavior-Driven Development (BDD) principles, automation scripts can serve as living documentation, promoting clear communication and shared understanding within the team.
- Regression Prevention: Automation helps catch regressions caused by new feature development, ensuring existing functionality remains intact.

### Trade-offs to Consider

While automation offers numerous advantages, it's important to acknowledge the time investment required for script development.  For applications with frequently changing requirements, the maintenance overhead of automation scripts might outweigh the benefits.  In such cases, manual testing might be a more suitable approach.

The following sections will delve deeper into the practical aspects of automation testing, guiding you through the steps to write your first script and equipping you with the necessary knowledge for successful implementation. We'll explore best practices, considerations, and the positive impact automation can have on your projects.  Finally, we'll conclude with a helpful checklist and a glimpse into advanced automation techniques.

This revised version improves upon the original article in several ways:

Clearer Introduction: The introduction is more engaging and directly addresses the target audience.
Structured Approach: The information is presented in a logical order, building upon foundational concepts.
Enhanced Explanation: The benefits and drawbacks of automation testing are explained in greater detail.
Formal Tone: The tone is more formal and professional, suitable for a technical guide.
Improved Readability: Sentence structure and flow have been improved for better readability.

## How I run the first script

From my point of view, for the manual tester or fresher, we should start to learn automation test with javascript tools such as Playwright, Cypress. Because it is the all in one framework, so it is easy to use.
If you have any experient in any programming language, you can choose the automation testing framework base on that programming language. It it the wise choice for you to getting started with automation testing.

## The knowledge you should know when doing automation testing

That's a great summary of some key concepts for web application testing and API testing! Here's a breakdown of each point:

### Web Application Testing

- Selenium: The workhorse of web automation. Selenium WebDriver allows you to control a web browser through code, simulating user actions and interactions. It supports various programming languages and integrates with many testing frameworks.
- Page Object Model (POM): A design pattern to improve code organization and maintainability. Web page elements are encapsulated in dedicated classes, separating the page logic from the test logic.
- Locators: Selenium uses locators (like Id, Name, XPath, CSS Selectors) to identify specific elements on a web page. Choosing the right locator ensures your tests target the intended elements reliably.
- JavaScript with Selenium: Selenium can execute JavaScript within the browser context. This is useful for interacting with dynamic elements or waiting for asynchronous operations to complete.
- WebDrivers: Browser-specific drivers are required to interact with Selenium. Popular examples include ChromeDriver (Chrome) and GeckoDriver (Firefox).

### API Testing

- API Requests: APIs are accessed through well-defined endpoints (URLs) with specific HTTP methods (GET, POST, PUT, etc.). Requests may include headers, request body data (often in JSON or XML format), and path parameters.
- JSON/XML Data: APIs often use JSON or XML for data exchange. Parsing and verifying the response data is a crucial part of API testing.
- API Status Codes: HTTP status codes provide information about the outcome of an API request. Common codes include 2xx (success), 4xx (client error), and 5xx (server error).

Understanding these concepts will give you a solid foundation for both web application testing and API testing.  There are many resources available online to delve deeper into each topic, including official documentation, tutorials, and sample code.

## Other thing you should know

- Run test on CICD system like Github actions or Jenkins Pipepline
- Run test on cross browser and cross platform by using selenium grid or third party like Browserstack
- Generate the report to make sure the script is able to giving the feedback
- Make the script run on parallel to saving time

