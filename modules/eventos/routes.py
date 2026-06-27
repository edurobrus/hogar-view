import calendar as cal_mod
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('eventos', __name__)

TIPOS_EVENTO = ['cita', 'recordatorio', 'tarea']

MESES_ES = [
    '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]


@bp.route('/calendario')
def calendario():
    hoy = date.today()
    year = int(request.args.get('year', hoy.year))
    month = int(request.args.get('month', hoy.month))

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year  = year if month < 12 else year + 1

    return render_template(
        'calendario.html',
        cal=cal_mod.monthcalendar(year, month),
        year=year,
        month=month,
        mes_nombre=MESES_ES[month],
        hoy=hoy,
        eventos=database.eventos_del_mes(year, month),
        dias_eventos=database.dias_con_eventos(year, month),
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        tipos=TIPOS_EVENTO,
        fecha_sel=request.args.get('fecha', ''),
        tareas_recurrentes=database.tareas_recurrentes(),
    )


@bp.route('/calendario/nuevo-evento', methods=['POST'])
def nuevo_desde_calendario():
    titulo = request.form.get('titulo', '').strip()
    if not titulo:
        if is_fetch(): return json_ok(url_for('eventos.calendario'))
        return redirect(url_for('eventos.calendario'))
    evento_id = database.crear_evento(
        titulo,
        request.form.get('descripcion', ''),
        request.form.get('fecha', ''),
        request.form.get('hora', '') or None,
        request.form.get('tipo', 'recordatorio'),
    )
    url = url_for('eventos.ver', evento_id=evento_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/eventos/nuevo', methods=['POST'])
def nuevo_sidebar():
    evento_id = database.crear_evento('Nuevo evento', '', date.today().isoformat(), None, 'recordatorio')
    url = url_for('eventos.ver', evento_id=evento_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/eventos/<int:evento_id>')
def ver(evento_id):
    evento = next((e for e in database.todos_los_eventos() if e['id'] == evento_id), None)
    if not evento:
        return redirect(url_for('eventos.calendario'))
    return render_template('evento_ver.html', evento=evento, tipos=TIPOS_EVENTO)


@bp.route('/eventos/<int:evento_id>/editar', methods=['POST'])
def editar(evento_id):
    database.editar_evento(
        evento_id,
        titulo=request.form.get('titulo', '').strip(),
        descripcion=request.form.get('descripcion', ''),
        fecha=request.form.get('fecha', date.today().isoformat()),
        hora=request.form.get('hora', '') or None,
        tipo=request.form.get('tipo', 'recordatorio'),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('eventos.ver', evento_id=evento_id))


@bp.route('/api/evento/<int:evento_id>/borrar', methods=['POST'])
def borrar(evento_id):
    database.borrar_evento(evento_id)
    ref = request.referrer or url_for('eventos.calendario')
    if is_fetch(): return json_ok(ref)
    return redirect(ref)


@bp.route('/api/exportar/<int:year>/<int:month>')
def exportar_mes(year, month):
    eventos = database.eventos_del_mes(year, month)
    tareas_rec = database.tareas_recurrentes()
    mes = MESES_ES[month]

    lineas = [f"Eventos de {mes} {year}:\n"]
    for e in eventos:
        dia = int(e['fecha'].split('-')[2])
        hora_str = f" {e['hora']}" if e['hora'] else ''
        lineas.append(f"- {dia} {mes.lower()}{hora_str} — {e['titulo']} ({e['tipo']})")
        if e['descripcion']:
            lineas.append(f"  Nota: {e['descripcion']}")

    if tareas_rec:
        lineas.append("\nTareas recurrentes del hogar:")
        for t in tareas_rec:
            lineas.append(f"- Cada {t['dias_recurrencia']} días — {t['titulo']} ({t['categoria']})")

    return jsonify({'texto': '\n'.join(lineas), 'mes': mes, 'year': year})
