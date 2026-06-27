---
layout: default
title: Mi Hogar
---

<div class="page-icon">🏠</div>
<h1 class="page-title">Mi Apartamento</h1>

<p class="block-h2">Tareas pendientes</p>

{% assign tareas_hoy = site.tareas | where_exp: "t", "t.completada != 1" | sort: "prioridad" %}
{% for t in tareas_hoy limit: 8 %}
<a href="{{ t.url | prepend: site.baseurl }}" class="n-row">
  <span style="width:16px; height:16px; border:1.5px solid rgba(55,53,47,0.25); border-radius:50%; flex-shrink:0;"></span>
  <span style="flex:1;">{{ t.titulo | default: t.title }}{% if t.recurrente == 1 %} <span style="font-size:11px; color:#2383e2;">↻</span>{% endif %}</span>
  {% if t.categoria %}<span class="n-tag tag-{{ t.categoria }}">{{ t.categoria }}</span>{% endif %}
  <span class="n-tag tag-{{ t.prioridad | default: 'normal' }}">{{ t.prioridad | default: "normal" }}</span>
</a>
{% else %}
<p class="n-empty">Sin tareas pendientes 🎉</p>
{% endfor %}

<div class="n-divider" style="margin: 24px 0;"></div>

<p class="block-h2">Próximos eventos</p>

{% assign eventos = site.eventos | sort: "fecha" %}
{% for e in eventos limit: 5 %}
<a href="{{ e.url | prepend: site.baseurl }}" class="n-row">
  <span style="font-size:12px; color:rgba(55,53,47,0.4); min-width:60px;">{{ e.fecha | slice: 5, 5 }}</span>
  <span style="flex:1;">{{ e.titulo | default: e.title }}</span>
  {% if e.tipo %}<span class="n-tag tag-{{ e.tipo }}">{{ e.tipo }}</span>{% endif %}
</a>
{% else %}
<p class="n-empty">Sin eventos próximos.</p>
{% endfor %}
