---
layout: post
title:  "Generate Single Page HTML Report For Maven Project"
author: toronto22
categories: [ basic technique, tutorial, java, maven, report ]
image: assets/images/2022-03-23/test-summary-report.png
---

As an automation tester, I want to generate single page HTML report. So, I can send the report to other members easily. To do that, I will use Serenity Report to generate the single page report.

## Prerequisite

Asssumtion that we will using Junit 5 in our project. So we will setup to project that can execute the test cases with command line.

In the pom.xml we need some dependencies:

```js
//pom.xml file
    <properties>
        ...
        <serenity.version>3.2.1</serenity.version>
    </properties>

    ...
    </dependencies>
        ...
        <dependency>
            <groupId>net.serenity-bdd</groupId>
            <artifactId>serenity-core</artifactId>
            <version>${serenity.version}</version>
        </dependency>
        <dependency>
            <groupId>io.github.fabianlinz</groupId>
            <artifactId>serenity-junit5</artifactId>
            <version>1.2.1</version>
        </dependency>
    </dependencies>
    ...
```

After adding dependencies into `pom` file, we can use it to run the test cases

```java
//WhenCompareTwoObject.java file
@SerenityTest
public class WhenCompareTwoObject {
    User actualUser;
    User expectedUser;
    @Test
    public void should_be_able_to_compare_two_equal_project(){
        actualUser = new User("Toronto22",22,true,12.22);
        expectedUser = new User("Toronto22",22,true,12.22);

        Assertions.assertThat(actualUser).usingRecursiveComparison()
                .isEqualTo(expectedUser);
    }

}
```

There are two things we have to use correctly are:

- Using annotation @SerenityTest for the test class
- Using annotation @Test of `Junit5` fo the test scenario instead of `Junit4`

The main purpuse of these precondition steps is that we can run test cases with maven commonline, So we can using following commonline to verify that the project can be executed with maven's commonline.

```java
mvn clean install
//or
mvn clean verify

```

## Generate HTML

After precondition steps is done, We need to add some plugins into `pom.xml` to make the single page HTML report is generated automatically.

```js
 <build>
        <plugins>
            ...
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0-M5</version>
                <configuration>
                    <skip>true</skip>
                </configuration>
            </plugin>
            <plugin>
                <artifactId>maven-failsafe-plugin</artifactId>
                <version>3.0.0-M5</version>
                <configuration>
                    <includes>
                        <include>**/*.java</include>
                    </includes>
                    <excludes>
                        <exclude>**/*WithFailures.java</exclude>
                    </excludes>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>integration-test</goal>
                            <goal>verify</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>net.serenity-bdd.maven.plugins</groupId>
                <artifactId>serenity-maven-plugin</artifactId>
                <version>${serenity.version}</version>
                <dependencies>
                    <dependency>
                        <groupId>net.serenity-bdd</groupId>
                        <artifactId>serenity-single-page-report</artifactId>
                        <version>${serenity.version}</version>
                    </dependency>
                    <dependency>
                        <groupId>net.serenity-bdd</groupId>
                        <artifactId>serenity-navigator-report</artifactId>
                        <version>${serenity.version}</version>
                    </dependency>
                </dependencies>
                <configuration>
                    <tags>${tags}</tags>
                    <reports>single-page-html,navigator</reports>
                </configuration>
                <executions>
                    <execution>
                        <id>serenity-reports</id>
                        <phase>post-integration-test</phase>
                        <goals>
                            <goal>aggregate</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

```

Fillaly, we can generate the single page HML report after execute tests with commonline

```js
mvn clean install
\\or
mvn clean verify
```

## Example on github

[Github source](https://github.com/toronto22/BasicTecnique)
