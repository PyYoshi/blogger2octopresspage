---
layout: page
title: "{{ page_name }}"
date: {{ date }}
comments: false
sharing: false
footer: false
---

Old Blog Entries:
{% for entry in entries %}
* [{{ entry.title }}](/{{ page_name }}{{ entry.permalink}})
{% endfor %}
