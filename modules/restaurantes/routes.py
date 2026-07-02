from flask import Blueprint, render_template, request, redirect, url_for
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('restaurantes', __name__, url_prefix='/restaurantes')


@bp.route('/<int:restaurante_id>')
def ver(restaurante_id):
    restaurante = next((r for r in database.todos_los_restaurantes() if r['id'] == restaurante_id), None)
    if not restaurante:
        return redirect('/')
    return render_template('restaurante_ver.html', restaurante=restaurante)


@bp.route('/nuevo', methods=['POST'])
def nuevo():
    restaurante_id = database.crear_restaurante('Nuevo restaurante', '')
    url = url_for('restaurantes.ver', restaurante_id=restaurante_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/<int:restaurante_id>/editar', methods=['POST'])
def editar(restaurante_id):
    database.editar_restaurante(
        restaurante_id,
        titulo=request.form.get('titulo', '').strip(),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('restaurantes.ver', restaurante_id=restaurante_id))


@bp.route('/<int:restaurante_id>/borrar', methods=['POST'])
def borrar(restaurante_id):
    database.borrar_restaurante(restaurante_id)
    if is_fetch(): return json_ok('/')
    return redirect('/')
