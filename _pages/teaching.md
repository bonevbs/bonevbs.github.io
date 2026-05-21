---
layout: page
permalink: /teaching/
title: teaching
description: Courses and teaching activities.
nav: true
nav_order: 5
---

<div class="teaching-list">

{% assign courses = site.teaching | sort: 'date' | reverse %}
{% for course in courses %}
  {% unless course.path contains '_template' %}
  <div class="mb-4">
    <h3><a href="{{ course.url | relative_url }}">{{ course.title }}</a></h3>
    <p class="text-muted mb-1">
      {{ course.type }} · {{ course.venue }} · {{ course.date | date: "%Y" }}
      {% if course.location %} · {{ course.location }}{% endif %}
    </p>
    {% if course.content != "" %}
    <div>{{ course.content | markdownify }}</div>
    {% endif %}
  </div>
  <hr>
  {% endunless %}
{% endfor %}

</div>
