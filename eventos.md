---
layout: default
title: Eventos
permalink: /eventos/
---

# Eventos

{% assign eventos = site.eventos | sort: "fecha" %}
{% for evento in eventos %}
<div style="background:#fff; border-radius:6px; padding:14px 16px; margin-bottom:10px; border:1px solid #e5e5e5;">
  <a href="{{ evento.url | prepend: site.baseurl }}" style="text-decoration:none; color:#37352f; font-weight:500;">{{ evento.titulo }}</a>
  <div style="font-size:12px; color:#888; margin-top:4px;">📅 {{ evento.fecha }}{% if evento.hora %} · {{ evento.hora }}{% endif %}</div>
</div>
{% endfor %}
