---
layout: default
title: Hoteles
permalink: /hoteles/
---

<div class="page-icon">🏨</div>
<h1 class="page-title">Hoteles</h1>

{% assign hoteles = site.hoteles | sort: "titulo" %}
{% for h in hoteles %}
<a href="{{ h.url | prepend: site.baseurl }}" class="n-row">
  <span class="nav-icon" style="opacity:0.5;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
  </span>
  <span style="flex:1;">{{ h.titulo | default: h.title }}</span>
</a>
{% else %}
<p class="n-empty">Sin hoteles.</p>
{% endfor %}
