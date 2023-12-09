---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

<table cellspacing="0" cellpadding="0" width="100%" style="border: none; font-size: $type-size-5;">
  {% for post in site.publications reversed %}
      {% include archive-single-table.html %}
  {% endfor %}
</table>
