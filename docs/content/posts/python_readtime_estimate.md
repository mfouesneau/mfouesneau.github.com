---
type: section
active: true

date: 2022-05-17

# Display name
title: Estimating an article's reading time in python

brief: Offering reading time estimation can contribute greatly to the end users' experience. I use it on my website and here is how I implemented it.

keywords:
    - python
    - code
    - Website

preview-image: ""

---

As part of my website, I wanted to provide reading time estimation. I find this gesture very useful from other websites. It allows a reader to guest the post length and to prepare the time they need to read an article in full.

**The principle is very basic**: I count the number of words in the article and divide it by the average word per minute (WPM). This is the average reading time for an article.

**Estimating words per **minute**
WPM measures words _processed__ in a minute. It has many meanings and complications. First and foremost, the average reading time is subjective. Secondly, the length or duration of words is variable, as some words are quick to read (e.g. 'dog') while others take much longer (like 'Incomprehensibility'). Other parameters affect the reading time, such as font type and size, your age, reading on a monitor or paper, paragraphs, images, etc.

Based on research done in this field (e.g., [irisreading.com](https://irisreading.com/average-reading-speed-by-age-are-you-fast-enough/)), adults read English at around 200 WPM on paper and 180 WPM on a monitor (the record is 290 WPM).

**Code**: The following code counts the number of words in the text and averages it to the 200 WPM speed.

```python
import re

def estimate_reading_time(text: str, WPM: int = 200) -> int:
    total_words = len(re.findall(r'\w+', text))
    time_minute = total_words // WPM + 1
    if time_minute == 0:
        time_minute = 1
    elif time_minute > 60:
        return str(time_minute // 60) + 'h'
    return str(time_minute) + 'min'
```