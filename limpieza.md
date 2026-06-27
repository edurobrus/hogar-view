---
layout: default
title: Limpieza
permalink: /limpieza/
---

<div class="page-icon">🧹</div>
<h1 class="page-title">Limpieza</h1>

{% assign items = site.limpieza | sort: "titulo" %}
{% for item in items %}
<a href="{{ item.url | prepend: site.baseurl }}" class="n-row">
  <span class="nav-icon" style="opacity:0.5;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 22l4-4"/><path d="M10.5 13.5L3 21"/><path d="M14 3l7 7-9.5 9.5-7-7z"/></svg>
  </span>
  <span style="flex:1;">{{ item.titulo | default: item.title }}</span>
</a>
{% else %}
<p class="n-empty">Sin rutinas de limpieza.</p>
{% endfor %}
