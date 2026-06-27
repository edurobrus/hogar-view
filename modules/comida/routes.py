from flask import Blueprint, render_template, request, redirect, url_for
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('comida', __name__, url_prefix='/comida')


@bp.route('/<int:item_id>')
def ver(item_id):
    item = next((r for r in database.todas_las_comidas() if r['id'] == item_id), None)
    if not item:
        return redirect('/')
    return render_template('comida_ver.html', item=item)


@bp.route('/nueva', methods=['POST'])
def nueva():
    item_id = database.crear_comida('Nueva comida', '')
    url = url_for('comida.ver', item_id=item_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/<int:item_id>/editar', methods=['POST'])
def editar(item_id):
    database.editar_comida(
        item_id,
        titulo=request.form.get('titulo', '').strip(),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('comida.ver', item_id=item_id))


@bp.route('/<int:item_id>/borrar', methods=['POST'])
def borrar(item_id):
    database.borrar_comida(item_id)
    if is_fetch(): return json_ok('/')
    return redirect('/')
