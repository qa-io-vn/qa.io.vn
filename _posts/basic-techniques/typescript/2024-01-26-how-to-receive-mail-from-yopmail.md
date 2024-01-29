---
layout: post
title:  "How to receive mail from yopmail in typescript"
author: dani
categories: [ basic technique, mail, typescript]
image: assets/images/6.jpg
---

As an automation tester, I want to receive mail from yopmail system. So I can do some feature needed to get information from mail inbox details such as register account or forgot password in an application.

## Installation

To receive mail in typescript, I will use the yopmail-helper package. To install that package, I use this command:

```cmd
npm i yopmail-helper
```

## Example link

[Yop Mail Helper Sample](https://github.com/qa-io-vn/yopmail-helper-sample)

## How to use

``` js
//Declare module
import { inbox, linkOfFirstMail, mailDetails, mailDetailsHtml } from 'yopmail-helper';
```

### ✉️ *get inbox of a mail address*

``` js
    const mails = await inbox('admin01');
```

### 🗃️ *Read details of an email*

``` js
    const mails = await inbox('admin01');
    const mailDetailsInfo = await mailDetails(mails[0].mailId,'admin01');
```

### 🗃️ *Read details of an email in HTML*

``` js
    const mails = await inbox('admin01');
    const mailDetailsHtmlInfo = await mailDetailsHtml(mails[0].mailId,'admin01');
```

### 📑 *Read link of an email*

``` js
    const link = await linkOfFirstMail('admin01');
```
