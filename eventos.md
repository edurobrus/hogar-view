---
layout: default
title: Eventos
permalink: /eventos/
---

<div class="page-icon">🕐</div>
<h1 class="page-title">Eventos</h1>

{% assign eventos = site.eventos | sort: "fecha" %}
{% for e in eventos %}
<a href="{{ e.url | prepend: site.baseurl }}" class="n-row">
  <span style="font-size:12px; color:rgba(55,53,47,0.4); min-width:70px; flex-shrink:0;">{{ e.fecha }}</span>
  {% if e.hora %}<span style="font-size:12px; color:rgba(55,53,47,0.35); flex-shrink:0;">{{ e.hora }}</span>{% endif %}
  <span style="flex:1;">{{ e.titulo | default: e.title }}</span>
  {% if e.tipo %}<span class="n-tag tag-{{ e.tipo }}">{{ e.tipo }}</span>{% endif %}
</a>
{% else %}
<p class="n-empty">Sin eventos.</p>
{% endfor %}
