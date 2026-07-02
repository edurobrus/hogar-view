---
layout: default
title: Restaurantes
permalink: /restaurantes/
---

<div class="page-icon">🍽️</div>
<h1 class="page-title">Restaurantes</h1>

{% assign restaurantes = site.restaurantes | sort: "titulo" %}
{% for r in restaurantes %}
<a href="{{ r.url | prepend: site.baseurl }}" class="n-row">
  <span class="nav-icon" style="opacity:0.5;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="8" x2="18" y2="21"/><line x1="6" y1="8" x2="6" y2="21"/><path d="M6 3v5a6 6 0 0 0 12 0V3"/></svg>
  </span>
  <span style="flex:1;">{{ r.titulo | default: r.title }}</span>
</a>
{% else %}
<p class="n-empty">Sin restaurantes.</p>
{% endfor %}
