---
layout: page
permalink: /teaching/
title: Teaching
nav: true
nav_order: 5
---

<div class="teaching-list">

{% assign courses = site.teaching | sort: 'date' | reverse %}
{% for course in courses %}
  {% unless course.path contains '_template' %}
  <div class="teaching-entry">
    <h4 class="teaching-title">{{ course.title }}</h4>
    <p class="teaching-meta">{{ course.type }} · {{ course.venue }} · {{ course.date | date: "%Y" }}</p>
  </div>
  {% endunless %}
{% endfor %}

</div>
