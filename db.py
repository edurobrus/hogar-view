"""
Storage backend: archivos Markdown con frontmatter YAML.

Estructura:
  data/
    _tareas/   slug-titulo_ID.md
    _eventos/  YYYY-MM-DD_slug-titulo_ID.md
    compras/   ID_slug.md
    gastos/    YYYY-MM-DD_ID_slug.md
    _recetas/  slug_ID.md
    _limpieza/ slug_ID.md
    comida/    slug_ID.md
"""

import re
import frontmatter
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).parent / "data"

DIRS = {
    "tareas":       BASE / "_tareas",
    "eventos":      BASE / "_eventos",
    "recetas":      BASE / "_recetas",
    "limpieza":     BASE / "_limpieza",
    "comida":       BASE / "comida",
    "hoteles":      BASE / "_hoteles",
    "restaurantes": BASE / "_restaurantes",
    "frances":      BASE / "_frances",
}

# ── utilidades ────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def _slug(text: str, maxlen=30) -> str:
    text = text.lower().strip()
    text = re.sub(r'[áàä]', 'a', text)
    text = re.sub(r'[éèë]', 'e', text)
    text = re.sub(r'[íìï]', 'i', text)
    text = re.sub(r'[óòö]', 'o', text)
    text = re.sub(r'[úùü]', 'u', text)
    text = re.sub(r'ñ', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:maxlen] or 'sin-titulo'

def _new_id(directory: Path) -> int:
    ids = []
    for f in directory.glob("*.md"):
        post = _load(f)
        if post and 'id' in post.metadata:
            ids.append(int(post.metadata['id']))
    return (max(ids) + 1) if ids else 1

def _load(path: Path):
    try:
        return frontmatter.load(str(path))
    except Exception:
        return None

_INVISIBLE = re.compile('[​‌‍﻿ ]')

def _clean(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return _INVISIBLE.sub('', text)

def _save(directory: Path, filename: str, metadata: dict, content: str = ""):
    path = directory / filename
    post = frontmatter.Post(_clean(content), **metadata)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
    return path

def _serialize(v):
    if isinstance(v, datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, date):
        return v.isoformat()
    return v

def _all(directory: Path) -> list[dict]:
    items = []
    for f in sorted(directory.glob("*.md")):
        post = _load(f)
        if post is None:
            continue
        d = {k: _serialize(v) for k, v in post.metadata.items()}
        d['_content'] = post.content
        d['_file'] = f
        items.append(_DictRow(d))
    return items

def _find_file(directory: Path, item_id: int) -> Path | None:
    for f in directory.glob("*.md"):
        post = _load(f)
        if post and post.metadata.get('id') == item_id:
            return f
    return None

def _delete(directory: Path, item_id: int):
    f = _find_file(directory, item_id)
    if f:
        f.unlink()


class _DictRow(dict):
    """dict con acceso por atributo."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


# ── init ──────────────────────────────────────────────────────────────────────

def init_db():
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)


# ── TAREAS ────────────────────────────────────────────────────────────────────

def _tarea_filename(t: dict) -> str:
    return f"{_slug(str(t.get('titulo', 'tarea')))}_{t['id']}.md"

def _tarea_meta(titulo, categoria, prioridad, recurrente, dias_recurrencia, fecha_limite) -> dict:
    return {
        'id':                _new_id(DIRS['tareas']),
        'titulo':            titulo,
        'categoria':         categoria,
        'prioridad':         prioridad,
        'recurrente':        int(bool(recurrente)),
        'dias_recurrencia':  dias_recurrencia,
        'fecha_limite':      fecha_limite,
        'completada':        0,
        'ultima_completada': None,
        'fecha_creacion':    date.today().isoformat(),
        'estado':            'pendiente',
    }

def crear_tarea(titulo, categoria, prioridad, recurrente, dias_recurrencia, fecha_limite):
    meta = _tarea_meta(titulo, categoria, prioridad, recurrente, dias_recurrencia, fecha_limite)
    _save(DIRS['tareas'], _tarea_filename(meta), meta)
    return meta['id']

def _tareas_all() -> list[_DictRow]:
    return _all(DIRS['tareas'])

def tareas_de_hoy() -> list[_DictRow]:
    hoy = date.today().isoformat()
    result = []
    for t in _tareas_all():
        if t.get('completada', 0):
            continue
        if t.get('recurrente', 0):
            ult = t.get('ultima_completada')
            dias = t.get('dias_recurrencia') or 1
            if ult is None or (date.today() - date.fromisoformat(str(ult))).days >= int(dias):
                result.append(t)
        else:
            fl = t.get('fecha_limite')
            if fl is None or str(fl) == hoy:
                result.append(t)
    result.sort(key=lambda t: (
        {'urgente': 0, 'normal': 1, 'opcional': 2}.get(t.get('prioridad', 'normal'), 1),
        str(t.get('fecha_limite') or 'z'),
    ))
    return result

def todas_las_tareas(categoria=None, prioridad=None, incluir_completadas=False) -> list[_DictRow]:
    items = _tareas_all()
    if not incluir_completadas:
        items = [t for t in items if not t.get('completada', 0)]
    if categoria:
        items = [t for t in items if t.get('categoria') == categoria]
    if prioridad:
        items = [t for t in items if t.get('prioridad') == prioridad]
    items.sort(key=lambda t: (
        {'urgente': 0, 'normal': 1, 'opcional': 2}.get(t.get('prioridad', 'normal'), 1),
        str(t.get('fecha_creacion', '')),
    ))
    return items

def editar_tarea(tarea_id: int, titulo, categoria, prioridad, fecha_limite, recurrente, dias_recurrencia, contenido=None):
    f = _find_file(DIRS['tareas'], tarea_id)
    if not f:
        return
    post = _load(f)
    meta = dict(post.metadata)
    meta['titulo'] = titulo or meta['titulo']
    meta['categoria'] = categoria
    meta['prioridad'] = prioridad
    meta['fecha_limite'] = fecha_limite
    meta['recurrente'] = int(bool(recurrente))
    meta['dias_recurrencia'] = int(dias_recurrencia) if str(dias_recurrencia).isdigit() else None
    _save(DIRS['tareas'], f.name, meta, contenido if contenido is not None else post.content)

def completar_tarea(tarea_id: int):
    f = _find_file(DIRS['tareas'], tarea_id)
    if not f:
        return
    post = _load(f)
    meta = dict(post.metadata)
    if meta.get('recurrente', 0):
        meta['ultima_completada'] = date.today().isoformat()
    else:
        meta['completada'] = 1
        meta['estado'] = 'hecho'
    _save(DIRS['tareas'], f.name, meta, post.content)

def borrar_tarea(tarea_id: int):
    _delete(DIRS['tareas'], tarea_id)

def tareas_recurrentes() -> list[_DictRow]:
    return [t for t in _tareas_all() if t.get('recurrente', 0)]

def tareas_kanban():
    all_t = _tareas_all()
    pendiente   = [t for t in all_t if t.get('estado') == 'pendiente'   and not t.get('completada', 0)]
    en_progreso = [t for t in all_t if t.get('estado') == 'en_progreso' and not t.get('completada', 0)]
    hecho       = sorted(
        [t for t in all_t if t.get('estado') == 'hecho' or t.get('completada', 0)],
        key=lambda t: str(t.get('ultima_completada') or t.get('fecha_creacion') or ''),
        reverse=True
    )[:30]
    def pri_sort(lst):
        return sorted(lst, key=lambda t: {'urgente': 0, 'normal': 1, 'opcional': 2}.get(t.get('prioridad', 'normal'), 1))
    return pri_sort(pendiente), pri_sort(en_progreso), hecho

def mover_tarea_kanban(tarea_id: int, nuevo_estado: str):
    f = _find_file(DIRS['tareas'], tarea_id)
    if not f:
        return
    post = _load(f)
    meta = dict(post.metadata)
    meta['estado'] = nuevo_estado
    if nuevo_estado == 'hecho':
        meta['completada'] = 1
        meta['ultima_completada'] = date.today().isoformat()
    else:
        meta['completada'] = 0
    _save(DIRS['tareas'], f.name, meta, post.content)

def dias_con_tareas(year: int, month: int) -> set[int]:
    prefix = f"{year}-{month:02d}-"
    dias = set()
    for t in _tareas_all():
        fl = str(t.get('fecha_limite') or '')
        if fl.startswith(prefix) and not t.get('completada', 0):
            try:
                dias.add(int(fl[8:10]))
            except Exception:
                pass
    return dias


# ── EVENTOS ───────────────────────────────────────────────────────────────────

def _evento_filename(meta: dict) -> str:
    return f"{meta.get('fecha', '0000-00-00')}_{_slug(str(meta.get('titulo', 'evento')))}_{meta['id']}.md"

def crear_evento(titulo, descripcion, fecha, hora, tipo):
    meta = {
        'id':          _new_id(DIRS['eventos']),
        'titulo':      titulo,
        'descripcion': descripcion or '',
        'fecha':       fecha,
        'hora':        hora,
        'tipo':        tipo,
        'completado':  0,
    }
    _save(DIRS['eventos'], _evento_filename(meta), meta)
    return meta['id']

def todos_los_eventos(incluir_completados=False) -> list[_DictRow]:
    result = _all(DIRS['eventos'])
    for e in result:
        e['descripcion'] = e.get('_content', '') or e.get('descripcion', '')
    if not incluir_completados:
        result = [e for e in result if not e.get('completado', 0)]
    result.sort(key=lambda e: (str(e.get('fecha', '')), str(e.get('hora') or 'z')))
    return result

def editar_evento(evento_id: int, titulo, descripcion, fecha, hora, tipo):
    f = _find_file(DIRS['eventos'], evento_id)
    if not f:
        return
    post = _load(f)
    meta = dict(post.metadata)
    meta['titulo'] = titulo or meta['titulo']
    meta['fecha']  = fecha
    meta['hora']   = hora or None
    meta['tipo']   = tipo
    new_name = _evento_filename(meta)
    f.unlink()
    _save(DIRS['eventos'], new_name, meta, descripcion or '')

def eventos_del_mes(year: int, month: int, incluir_completados=False) -> list[_DictRow]:
    prefix = f"{year}-{month:02d}-"
    result = [e for e in _all(DIRS['eventos']) if str(e.get('fecha', '')).startswith(prefix)]
    if not incluir_completados:
        result = [e for e in result if not e.get('completado', 0)]
    result.sort(key=lambda e: (str(e.get('fecha', '')), str(e.get('hora') or 'z')))
    return result

def dias_con_eventos(year: int, month: int) -> set[int]:
    prefix = f"{year}-{month:02d}-"
    dias = set()
    for e in _all(DIRS['eventos']):
        if e.get('completado', 0):
            continue
        f = str(e.get('fecha', ''))
        if f.startswith(prefix):
            try:
                dias.add(int(f[8:10]))
            except Exception:
                pass
    return dias

def borrar_evento(evento_id: int):
    _delete(DIRS['eventos'], evento_id)



# ── SimpleCollection — recetas / limpieza / comida ────────────────────────────

class SimpleCollection:
    """CRUD genérico para colecciones titulo+contenido."""

    def __init__(self, dir_key: str, default_title: str):
        self._dir = DIRS[dir_key]
        self._default_title = default_title

    def _filename(self, meta: dict) -> str:
        return f"{_slug(str(meta.get('titulo') or self._default_title))}_{meta['id']}.md"

    def all(self) -> list[_DictRow]:
        items = _all(self._dir)
        for item in items:
            item['contenido'] = item.get('_content', '')
        items.sort(key=lambda r: str(r.get('titulo', '')))
        return items

    def get(self, item_id: int) -> _DictRow | None:
        return next((r for r in self.all() if r['id'] == item_id), None)

    def crear(self, titulo, contenido) -> int:
        now = _now()
        meta = {
            'id':                 _new_id(self._dir),
            'titulo':             titulo or '',
            'fecha_creacion':     now,
            'fecha_modificacion': now,
        }
        _save(self._dir, self._filename(meta), meta, contenido)
        return meta['id']

    def editar(self, item_id: int, titulo, contenido):
        f = _find_file(self._dir, item_id)
        if not f:
            return
        post = _load(f)
        meta = dict(post.metadata)
        meta['titulo'] = titulo or meta['titulo']
        meta['fecha_modificacion'] = _now()
        new_name = self._filename(meta)
        if f.name != new_name:
            f.unlink()
        _save(self._dir, new_name, meta, contenido or '')

    def borrar(self, item_id: int):
        _delete(self._dir, item_id)


_recetas      = SimpleCollection('recetas',      'nueva-receta')
_limpieza     = SimpleCollection('limpieza',     'nueva-limpieza')
_comida       = SimpleCollection('comida',       'nueva-comida')
_hoteles      = SimpleCollection('hoteles',      'nuevo-hotel')
_restaurantes = SimpleCollection('restaurantes', 'nuevo-restaurante')
_frances      = SimpleCollection('frances',      'nueva-ficha')

# ── RECETAS ───────────────────────────────────────────────────────────────────

def todas_las_recetas() -> list[_DictRow]:  return _recetas.all()
def crear_receta(titulo, contenido) -> int:  return _recetas.crear(titulo, contenido)
def editar_receta(receta_id, titulo, contenido): _recetas.editar(receta_id, titulo, contenido)
def borrar_receta(receta_id): _recetas.borrar(receta_id)

# ── LIMPIEZA ──────────────────────────────────────────────────────────────────

def todas_las_limpiezas() -> list[_DictRow]:  return _limpieza.all()
def crear_limpieza(titulo, contenido) -> int:  return _limpieza.crear(titulo, contenido)
def editar_limpieza(item_id, titulo, contenido): _limpieza.editar(item_id, titulo, contenido)
def borrar_limpieza(item_id): _limpieza.borrar(item_id)

# ── COMIDA ────────────────────────────────────────────────────────────────────

def todas_las_comidas() -> list[_DictRow]:  return _comida.all()
def crear_comida(titulo, contenido) -> int:  return _comida.crear(titulo, contenido)
def editar_comida(item_id, titulo, contenido): _comida.editar(item_id, titulo, contenido)
def borrar_comida(item_id): _comida.borrar(item_id)

# ── HOTELES ───────────────────────────────────────────────────────────────────

def todos_los_hoteles() -> list[_DictRow]:  return _hoteles.all()
def crear_hotel(titulo, contenido) -> int:  return _hoteles.crear(titulo, contenido)
def editar_hotel(item_id, titulo, contenido): _hoteles.editar(item_id, titulo, contenido)
def borrar_hotel(item_id): _hoteles.borrar(item_id)

# ── RESTAURANTES ──────────────────────────────────────────────────────────────

def todos_los_restaurantes() -> list[_DictRow]:  return _restaurantes.all()
def crear_restaurante(titulo, contenido) -> int:  return _restaurantes.crear(titulo, contenido)
def editar_restaurante(item_id, titulo, contenido): _restaurantes.editar(item_id, titulo, contenido)
def borrar_restaurante(item_id): _restaurantes.borrar(item_id)

# ── FRANCÉS ───────────────────────────────────────────────────────────────────

def todas_las_frances() -> list[_DictRow]:  return _frances.all()
def crear_frances(titulo, contenido) -> int:  return _frances.crear(titulo, contenido)
def editar_frances(item_id, titulo, contenido): _frances.editar(item_id, titulo, contenido)
def borrar_frances(item_id): _frances.borrar(item_id)
