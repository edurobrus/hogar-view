---
layout: default
title: Tareas
permalink: /tareas/
---

# Tareas

{% assign tareas = site.tareas | sort: "prioridad" %}
{% for tarea in tareas %}
<div style="background:#fff; border-radius:6px; padding:14px 16px; margin-bottom:10px; border:1px solid #e5e5e5; display:flex; align-items:center; gap:12px;">
  <span>{% if tarea.completada == 1 %}✅{% else %}⬜{% endif %}</span>
  <div style="flex:1;">
    <a href="{{ tarea.url | prepend: site.baseurl }}" style="text-decoration:none; color:#37352f; font-weight:500;">{{ tarea.titulo }}</a>
    {% if tarea.fecha_limite %}<div style="font-size:12px; color:#888; margin-top:2px;">{{ tarea.fecha_limite }}</div>{% endif %}
  </div>
  {% if tarea.prioridad == "urgente" %}<span style="background:#ffe2dd; color:#c0392b; font-size:11px; padding:2px 8px; border-radius:4px;">urgente</span>{% endif %}
</div>
{% endfor %}
