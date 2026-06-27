---
layout: default
title: Limpieza
permalink: /limpieza/
---

# Limpieza

{% for item in site.limpieza %}
<div style="background:#fff; border-radius:6px; padding:14px 16px; margin-bottom:10px; border:1px solid #e5e5e5;">
  <a href="{{ item.url | prepend: site.baseurl }}" style="text-decoration:none; color:#37352f; font-weight:500;">{{ item.titulo }}</a>
</div>
{% endfor %}
