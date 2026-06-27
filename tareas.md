---
layout: default
title: Tareas
permalink: /tareas/
---

<div class="page-icon">✅</div>
<h1 class="page-title">Tareas del hogar</h1>

{% assign tareas_pendientes = site.tareas | where_exp: "t", "t.completada != 1" | sort: "prioridad" %}
{% assign tareas_hechas = site.tareas | where_exp: "t", "t.completada == 1" %}

{% for t in tareas_pendientes %}
<a href="{{ t.url | prepend: site.baseurl }}" class="n-row">
  <span style="width:16px; height:16px; border:1.5px solid rgba(55,53,47,0.25); border-radius:50%; flex-shrink:0;"></span>
  <span style="flex:1;">{{ t.titulo | default: t.title }}{% if t.recurrente == 1 %} <span style="font-size:11px; color:#2383e2; margin-left:4px;">↻ {{ t.dias_recurrencia }}d</span>{% endif %}</span>
  {% if t.fecha_limite %}<span style="font-size:12px; color:rgba(55,53,47,0.4);">{{ t.fecha_limite }}</span>{% endif %}
  {% if t.categoria %}<span class="n-tag tag-{{ t.categoria }}">{{ t.categoria }}</span>{% endif %}
  <span class="n-tag tag-{{ t.prioridad | default: 'normal' }}">{{ t.prioridad | default: "normal" }}</span>
</a>
{% endfor %}

{% if tareas_pendientes.size == 0 %}
<p class="n-empty">Sin tareas pendientes 🎉</p>
{% endif %}

{% if tareas_hechas.size > 0 %}
<div class="n-divider" style="margin: 24px 0;"></div>
<p class="block-h2" style="font-size:14px; color:rgba(55,53,47,0.5); font-weight:500;">Completadas ({{ tareas_hechas.size }})</p>
{% for t in tareas_hechas %}
<a href="{{ t.url | prepend: site.baseurl }}" class="n-row" style="opacity:0.4;">
  <span style="width:16px; height:16px; background:rgba(55,53,47,0.15); border-radius:50%; flex-shrink:0;"></span>
  <span style="flex:1; text-decoration:line-through;">{{ t.titulo | default: t.title }}</span>
</a>
{% endfor %}
{% endif %}
