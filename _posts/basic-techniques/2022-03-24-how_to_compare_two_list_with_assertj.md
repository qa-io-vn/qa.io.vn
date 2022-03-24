---
layout: post
title:  "How to compare two lists with AssertJ"
author: toronto22
categories: [ basic technique, tutorial, java, maven, assertj ]
image: assets/images/2022-03-23/assertj.png
---
As an automation tester, I want to compare two lists to prove those are equal or not.
To do that, I can use function of AssertJ library (`assertj-core`) to compare two list

## Prerequisite
To using AssertJ we have to add dependency into `pom.xml` file

```java
<!-- https://mvnrepository.com/artifact/org.assertj/assertj-core -->
        <dependency>
            <groupId>org.assertj</groupId>
            <artifactId>assertj-core</artifactId>
            <version>3.22.0</version>
            <scope>test</scope>
        </dependency>
```

## Compare two lists objects
### Example
I have some lists of `user` class
```java
    static List<User> firstList = new ArrayList<>();
    static List<User> secondList = new ArrayList<>();
    static List<User> thirdList = new ArrayList<>();
    static List<User> fourthList = new ArrayList<>();

    //Original list
    firstList.add(new User("A",12,true,123.12));
    firstList.add(new User("B",14,true,888));
    firstList.add(new User("C",13,false,999));

    //Same original list but different order
    secondList.add(new User("A",12,true,123.12));
    secondList.add(new User("C",13,false,999));
    secondList.add(new User("B",14,true,888));

    //Same original list
    thirdList.add(new User("A",12,true,123.12));
    thirdList.add(new User("B",14,true,888));
    thirdList.add(new User("C",13,false,999));
```

I want to compare 2 lists with order and ignore order.
### Compare 2 lists with order
Using following function we can compare two list that compare with order.
```java
    @Test
    public void compare_with_order_with_2_equal_lists_have_same_order(){
        assertThat(firstList).usingRecursiveComparison()
                .isEqualTo(thirdList);
    }
```
### Compare 2 lists ignore order
Using following function we can compare two list and ignore about the order of items.
```java
    @Test
    public void compare_ignore_order_with_2_equal_objects_have_different_order(){
        assertThat(firstList).usingRecursiveComparison().ignoringCollectionOrder()
                .isEqualTo(secondList);
    }
```

## Compare two lists String

### Example
I have some lists of String class.

```java
    static List<String> firstList = new ArrayList<>();
    static List<String> secondList = new ArrayList<>();
    static List<String> thirdList = new ArrayList<>();
    static List<String> fourthList = new ArrayList<>();

   //Original list
    firstList.add("A");
    firstList.add("B");
    firstList.add("C");

    //Same original list but different order
    secondList.add("A");
    secondList.add("C");
    secondList.add("B");

    //Same original list
    thirdList.add("A");
    thirdList.add("B");
    thirdList.add("C");
```

I want to compare those lists with order and ignore order.


### Compare 2 lists with order
Using following function we can compare two list that compare with order.
```java
    @Test
    public void compare_with_order_with_2_equal_lists_have_same_order(){
        assertThat(firstList).usingRecursiveComparison()
                .isEqualTo(thirdList);
    }
```

### Compare 2 lists ignore order
Using following function we can compare two list that compare ignore order.
```java
    @Test
    public void compare_with_order_with_2_equal_lists_have_different_order(){
        assertThat(firstList).usingRecursiveComparison()
                .isEqualTo(thirdList);
    }
```

## Compare two lists Interger, Float and Double
We use the function to compare like the function that is used for two list String