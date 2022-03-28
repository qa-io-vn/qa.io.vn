---
layout: post
title:  "Execute test in paralell with junit5"
author: toronto22
categories: [ basic technique ]
image: assets/images/2022-03-23/assertj.png
tags: [junit5, serenity]
---
As an automation tester I want to execute our automation test script in parallel. So I can finish the execution faster.

## Prerequisite

Our automation test script need to config to execute with Junit 5

## Configuration

There are atleast two ways to configure the test cases can run in parallel is using configuration file and using annotation.

### Configure with configuration file
To run our script in parallel we can create `junit-platform.properties` file in `src/java/resources` folder and create the content with

```java
junit.jupiter.execution.parallel.enabled = true
junit.jupiter.execution.parallel.mode.default = concurrent
junit.jupiter.execution.parallel.mode.classes.default = concurrent
```

The above content will enable the parallel executing feature and make script can run functions and classes in parallel. For more details, we can run with fix number of thread is 2 (We can change to any number).

```java
//To execute test with fix number of thread
junit.jupiter.execution.parallel.config.strategy=fixed
junit.jupiter.execution.parallel.config.fixed.parallelism=2
```
### Configure directly by annotation
We can define the class or function is run with concurrent or same thread with annotation

```java
//To execute class/function in concurrent mode
@Execution(ExecutionMode.CONCURRENT)

//To execute class/function in same thread mode
@Execution(ExecutionMode.SAME_THREAD)
```
## For more information
[Referrence link](https://junit.org/junit5/docs/snapshot/user-guide/#writing-tests-parallel-execution)

## Example

Source code is [here](https://github.com/toronto22/BasicTecnique) with`how_to_assert_two_list_with_assertj` feature folder that contains test cases are configured by annotation.