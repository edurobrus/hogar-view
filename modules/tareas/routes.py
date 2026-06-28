from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('tareas', __name__)

CATEGORIAS = ['cocina', 'baño', 'compras', 'limpieza', 'general']
PRIORIDADES = ['urgente', 'normal', 'opcional']


@bp.route('/tareas')
def index():
    categoria = request.args.get('categoria', '')
    prioridad = request.args.get('prioridad', '')
    mostrar_completadas = request.args.get('completadas', '') == '1'
    lista = database.todas_las_tareas(
        categoria=categoria or None,
        prioridad=prioridad or None,
        incluir_completadas=mostrar_completadas,
    )
    return render_template(
        'tareas.html',
        tareas=lista,
        categorias=CATEGORIAS,
        prioridades=PRIORIDADES,
        filtro_cat=categoria,
        filtro_pri=prioridad,
        mostrar_completadas=mostrar_completadas,
    )


@bp.route('/tareas/<int:tarea_id>')
def ver(tarea_id):
    tarea = next((t for t in database.todas_las_tareas() if t['id'] == tarea_id), None)
    if not tarea:
        return redirect(url_for('tareas.index'))
    return render_template('tarea_ver.html', tarea=tarea,
                           categorias=CATEGORIAS, prioridades=PRIORIDADES)


@bp.route('/tareas/nueva', methods=['POST'])
def nueva():
    titulo = request.form.get('titulo', '').strip()
    if not titulo:
        if is_fetch(): return json_ok(url_for('tareas.index'))
        return redirect(url_for('tareas.index'))
    categoria = request.form.get('categoria', 'general')
    prioridad = request.form.get('prioridad', 'normal')
    recurrente = 'recurrente' in request.form
    dias_rec = request.form.get('dias_recurrencia', '')
    fecha_limite = request.form.get('fecha_limite', '')
    tarea_id = database.crear_tarea(
        titulo, categoria, prioridad, recurrente,
        int(dias_rec) if dias_rec.isdigit() else None,
        fecha_limite or None,
    )
    url = url_for('tareas.ver', tarea_id=tarea_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/tareas/<int:tarea_id>/editar', methods=['POST'])
def editar(tarea_id):
    database.editar_tarea(
        tarea_id,
        titulo=request.form.get('titulo', '').strip(),
        categoria=request.form.get('categoria', 'general'),
        prioridad=request.form.get('prioridad', 'normal'),
        fecha_limite=request.form.get('fecha_limite', '') or None,
        recurrente='recurrente' in request.form,
        dias_recurrencia=request.form.get('dias_recurrencia', ''),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('tareas.ver', tarea_id=tarea_id))


@bp.route('/api/tarea/<int:tarea_id>/completar', methods=['POST'])
def completar(tarea_id):
    database.completar_tarea(tarea_id)
    ref = request.referrer or url_for('tareas.index')
    if is_fetch(): return json_ok(ref)
    return redirect(ref)


@bp.route('/api/tarea/<int:tarea_id>/borrar', methods=['POST'])
def borrar(tarea_id):
    database.borrar_tarea(tarea_id)
    ref = request.referrer or url_for('tareas.index')
    if is_fetch(): return json_ok(ref)
    return redirect(ref)


@bp.route('/api/tarea/<int:tarea_id>/mover', methods=['POST'])
def mover(tarea_id):
    estado = request.form.get('estado', 'pendiente')
    if estado not in ('pendiente', 'en_progreso', 'hecho'):
        return jsonify({'error': 'estado inválido'}), 400
    database.mover_tarea_kanban(tarea_id, estado)
    return jsonify({'ok': True})


@bp.route('/kanban')
def kanban():
    pendiente, en_progreso, hecho = database.tareas_kanban()
    return render_template('kanban.html',
                           pendiente=pendiente,
                           en_progreso=en_progreso,
                           hecho=hecho)
