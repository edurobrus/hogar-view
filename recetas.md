---
layout: default
title: Recetas
permalink: /recetas/
---

# Recetas

{% for receta in site.recetas %}
<div style="background:#fff; border-radius:6px; padding:14px 16px; margin-bottom:10px; border:1px solid #e5e5e5;">
  <a href="{{ receta.url | prepend: site.baseurl }}" style="text-decoration:none; color:#37352f; font-weight:500;">{{ receta.titulo }}</a>
</div>
{% endfor %}
