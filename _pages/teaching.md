---
layout: page
permalink: /teaching/
title: Teaching
description: Courses and teaching activities.
nav: true
nav_order: 5
---

<div class="teaching-list">

{% assign courses = site.teaching | sort: 'date' | reverse %}
{% for course in courses %}
  {% unless course.path contains '_template' %}
  <div class="mb-4">
    <h3 class="mb-1">{{ course.title }}</h3>
    <p class="text-muted mb-2">
      {{ course.type }} · {{ course.venue }} · {{ course.date | date: "%Y" }}
      {% if course.location %} · {{ course.location }}{% endif %}
    </p>
    {% if course.content != "" %}
    <div>{{ course.content | markdownify }}</div>
    {% endif %}
  </div>
  {% endunless %}
{% endfor %}

</div>
