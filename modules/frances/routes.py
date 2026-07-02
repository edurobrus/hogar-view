from flask import Blueprint, render_template, request, redirect, url_for
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('frances', __name__, url_prefix='/frances')


@bp.route('/')
def index():
    fichas = database.todas_las_frances()
    return render_template('frances.html', fichas=fichas)


@bp.route('/<int:item_id>')
def ver(item_id):
    item = next((f for f in database.todas_las_frances() if f['id'] == item_id), None)
    if not item:
        return redirect('/')
    return render_template('frances_ver.html', item=item)


@bp.route('/nuevo', methods=['POST'])
def nuevo():
    item_id = database.crear_frances('Nueva ficha', '')
    url = url_for('frances.ver', item_id=item_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/<int:item_id>/editar', methods=['POST'])
def editar(item_id):
    database.editar_frances(
        item_id,
        titulo=request.form.get('titulo', '').strip(),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('frances.ver', item_id=item_id))


@bp.route('/<int:item_id>/borrar', methods=['POST'])
def borrar(item_id):
    database.borrar_frances(item_id)
    if is_fetch(): return json_ok('/')
    return redirect('/')
