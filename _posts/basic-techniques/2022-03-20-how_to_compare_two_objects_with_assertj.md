---
layout: post
title:  "How to compare two object with AssertJ"
author: toronto22
categories: [ basic technique, tutorial, java, maven ]
image: assets/images/6.jpg
---

As an automation tester, I want to compare two objects to prove those are equal or not.
To do that, I can use function of AssertJ library (`assertj-core`) to compare tow objects field by field.

## Assertion example:

We have the Class `User` and then we create 2 objects of that class with name `expectedUser` and `actualUser`. To compare those objects, we can use following steps:

- Add `assertj-core` dependency to `pom.xml` file

```java
<!-- https://mvnrepository.com/artifact/org.assertj/assertj-core -->
        <dependency>
            <groupId>org.assertj</groupId>
            <artifactId>assertj-core</artifactId>
            <version>3.22.0</version>
            <scope>test</scope>
        </dependency>
```

- The compare functions is described in following test

```java
package info.toronto22.feature;

import info.toronto22.model.User;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

public class WhenCompareTwoObject {
    User actualUser;
    User expectedUser;
    @Test
    public void should_be_able_to_compare_two_equal_project(){
		//Init two objects to compare
        actualUser = new User("Toronto22",22,true,12.22);
        expectedUser = new User("Toronto22",22,true,12.22);
		//Compare two object with AssertJ library
        Assertions.assertThat(actualUser).usingRecursiveComparison()
                .isEqualTo(expectedUser);
		//Test passed due to same value of the two objects
    }
}

```

That’s It!
Pretty simple right!

## Proven GitHub source code:

The source code: [here](https://github.com/toronto22/BasicTecnique/tree/master/src/test/java/info/toronto22/how_to_assert_two_objects_with_assertj)

## More details about assertion example

- `User` class:

```java
package info.toronto22.model;

public class User {
    String name;
    int age;
    Boolean isMarriage;
    double salary;

    public User(String name, int age, Boolean isMarriage, double salary) {
        this.name = name;
        this.age = age;
        this.isMarriage = isMarriage;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public Boolean getMarriage() {
        return isMarriage;
    }

    public void setMarriage(Boolean marriage) {
        isMarriage = marriage;
    }

    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        this.salary = salary;
    }
}
```

- To add `assertj-core` dependency to `pom.xml` file, I am currently using version `3.22.0` to create the example, but we can use other version following our needed. With old version, we can use this function to compare two objects also:

```java
import org.assertj.core.api.Assertions;
...
Assertions.assertThat(actualUser).isEqualToComparingFieldByField(expectedUser);
//Note: this function is deprecated in new versions of assertj-core library
```

- When compare two different object we can get error message that is similar to understand:

```java
//compare
//actualUser = new User("Toronto22",22,true,12.22);
//expectedUser = new User("Toronto23",23,false,12.22);
//Assertions.assertThat(actualUser).usingRecursiveComparison()
//                .isEqualTo(expectedUser);
//With error log:

C:\Users\admin\.jdks\corretto-11.0.14.1\bin\java.exe -ea -Didea.test.cyclic.buffer.size=1048576 "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2021.1\lib\idea_rt.jar=61506:C:\Program Files\JetBrains\IntelliJ IDEA 2021.1\bin" -Dfile.encoding=UTF-8 -classpath "C:\Program Files\JetBrains\IntelliJ IDEA 2021.1\lib\idea_rt.jar;C:\Users\admin\.m2\repository\org\junit\platform\junit-platform-launcher\1.8.2\junit-platform-launcher-1.8.2.jar;C:\Program Files\JetBrains\IntelliJ IDEA 2021.1\plugins\junit\lib\junit5-rt.jar;C:\Program Files\JetBrains\IntelliJ IDEA 2021.1\plugins\junit\lib\junit-rt.jar;D:\OneMountWorkspace\SourceCode\BasicTecnique\target\test-classes;C:\Users\admin\.m2\repository\org\junit\jupiter\junit-jupiter\5.8.2\junit-jupiter-5.8.2.jar;C:\Users\admin\.m2\repository\org\junit\jupiter\junit-jupiter-api\5.8.2\junit-jupiter-api-5.8.2.jar;C:\Users\admin\.m2\repository\org\opentest4j\opentest4j\1.2.0\opentest4j-1.2.0.jar;C:\Users\admin\.m2\repository\org\junit\platform\junit-platform-commons\1.8.2\junit-platform-commons-1.8.2.jar;C:\Users\admin\.m2\repository\org\apiguardian\apiguardian-api\1.1.2\apiguardian-api-1.1.2.jar;C:\Users\admin\.m2\repository\org\junit\jupiter\junit-jupiter-params\5.8.2\junit-jupiter-params-5.8.2.jar;C:\Users\admin\.m2\repository\org\junit\jupiter\junit-jupiter-engine\5.8.2\junit-jupiter-engine-5.8.2.jar;C:\Users\admin\.m2\repository\org\junit\platform\junit-platform-engine\1.8.2\junit-platform-engine-1.8.2.jar;C:\Users\admin\.m2\repository\org\assertj\assertj-core\3.22.0\assertj-core-3.22.0.jar" com.intellij.rt.junit.JUnitStarter -ideVersion5 -junit5 info.toronto22.feature.WhenCompareTwoObject,should_be_able_to_compare_two_equal_project

java.lang.AssertionError: 
Expecting actual:
  info.toronto22.model.User@366647c2
to be equal to:
  info.toronto22.model.User@6a6afff2
when recursively comparing field by field, but found the following 3 differences:

field/property 'age' differ:
- actual value  : 22
- expected value: 23

field/property 'isMarriage' differ:
- actual value  : true
- expected value: false

field/property 'name' differ:
- actual value  : "Toronto22"
- expected value: "Toronto23"

The recursive comparison was performed with this configuration:
- no overridden equals methods were used in the comparison (except for java types)
- these types were compared with the following comparators:
  - java.lang.Double -> DoubleComparator[precision=1.0E-15]
  - java.lang.Float -> FloatComparator[precision=1.0E-6]
  - java.nio.file.Path -> lexicographic comparator (Path natural order)
- actual and expected objects and their fields were compared field by field recursively even if they were not of the same type, this allows for example to compare a Person to a PersonDto (call strictTypeChecking(true) to change that behavior).

	at info.toronto22.feature.WhenCompareTwoObject.should_be_able_to_compare_two_equal_project(WhenCompareTwoObject.java:17)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
... Bla Bla about some thing not so important. 
```