---
layout: default
title: Eventos
permalink: /eventos/
---

<div class="page-icon">🕐</div>
<h1 class="page-title">Eventos</h1>

{% assign eventos_pendientes = site.eventos | where_exp: "e", "e.completado != 1" | sort: "fecha" %}
{% assign eventos_hechos = site.eventos | where_exp: "e", "e.completado == 1" | sort: "fecha" %}
{% for e in eventos_pendientes %}
<a href="{{ e.url | prepend: site.baseurl }}" class="n-row">
  <span style="font-size:12px; color:rgba(55,53,47,0.4); min-width:70px; flex-shrink:0;">{{ e.fecha }}</span>
  {% if e.hora %}<span style="font-size:12px; color:rgba(55,53,47,0.35); flex-shrink:0;">{{ e.hora }}</span>{% endif %}
  <span style="flex:1;">{{ e.titulo | default: e.title }}</span>
  {% if e.tipo %}<span class="n-tag tag-{{ e.tipo }}">{{ e.tipo }}</span>{% endif %}
</a>
{% else %}
<p class="n-empty">Sin eventos pendientes.</p>
{% endfor %}

{% if eventos_hechos.size > 0 %}
<div class="n-divider" style="margin: 24px 0;"></div>
<p class="block-h2" style="font-size:14px; color:rgba(55,53,47,0.5); font-weight:500;">Completados ({{ eventos_hechos.size }})</p>
{% for e in eventos_hechos %}
<a href="{{ e.url | prepend: site.baseurl }}" class="n-row" style="opacity:0.4;">
  <span style="font-size:12px; color:rgba(55,53,47,0.4); min-width:70px; flex-shrink:0;">{{ e.fecha }}</span>
  <span style="flex:1; text-decoration:line-through;">{{ e.titulo | default: e.title }}</span>
</a>
{% endfor %}
{% endif %}
