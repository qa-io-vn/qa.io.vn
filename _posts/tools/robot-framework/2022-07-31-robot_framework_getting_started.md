---
layout: post
title:  "Robot Framework - Getting started"
author: toronto22
categories: [ UI, Automation testing tools]
image: assets/images/tools/robot-framework.png
---

As an automation tester, I want to do automation test for UI application. To do that, I can use Robot Framework tools to implement the test script.

## Why Robot Framework

## Prerequisite

- [Python is installed.](https://www.python.org/downloads/) (On Windows machines, make sure to add Python to PATH during installation.)
- [Pycharm IDE is installed.](https://www.jetbrains.com/pycharm/download/#section=windows)
  
## Installation

- Execute the command `pip install robotframework`
- Check the installation is successful by run the command `robot --version`

## Robot Framework Selenium Installation

- Execute the command
  
```js
  pip install --upgrade robotframework-seleniumlibrary
  pip install webdrivermanager
  webdrivermanager firefox chrome --linkpath /usr/local/bin
```

## Reference

<https://github.com/alapanme/Robot-Framework>
