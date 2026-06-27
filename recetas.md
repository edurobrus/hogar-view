---
layout: default
title: Recetas
permalink: /recetas/
---

<div class="page-icon">🍳</div>
<h1 class="page-title">Recetas</h1>

{% assign recetas = site.recetas | sort: "titulo" %}
{% for r in recetas %}
<a href="{{ r.url | prepend: site.baseurl }}" class="n-row">
  <span class="nav-icon" style="opacity:0.5;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>
  </span>
  <span style="flex:1;">{{ r.titulo | default: r.title }}</span>
</a>
{% else %}
<p class="n-empty">Sin recetas.</p>
{% endfor %}
