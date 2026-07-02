---
layout: default
title: Francés
permalink: /frances/
---

<div class="page-icon">🇫🇷</div>
<h1 class="page-title">Francés</h1>

{% assign fichas = site.frances | sort: "titulo" %}
{% for f in fichas %}
<a href="{{ f.url | prepend: site.baseurl }}" class="n-row">
  <span class="nav-icon" style="opacity:0.5;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </span>
  <span style="flex:1;">{{ f.titulo | default: f.title }}</span>
</a>
{% else %}
<p class="n-empty">Sin fichas.</p>
{% endfor %}
