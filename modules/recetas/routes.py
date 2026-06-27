from flask import Blueprint, render_template, request, redirect, url_for
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('recetas', __name__, url_prefix='/recetas')


@bp.route('/<int:receta_id>')
def ver(receta_id):
    receta = next((r for r in database.todas_las_recetas() if r['id'] == receta_id), None)
    if not receta:
        return redirect('/')
    return render_template('receta_ver.html', receta=receta)


@bp.route('/nueva', methods=['POST'])
def nueva():
    receta_id = database.crear_receta('Nueva receta', '')
    url = url_for('recetas.ver', receta_id=receta_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/<int:receta_id>/editar', methods=['POST'])
def editar(receta_id):
    database.editar_receta(
        receta_id,
        titulo=request.form.get('titulo', '').strip(),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('recetas.ver', receta_id=receta_id))


@bp.route('/<int:receta_id>/borrar', methods=['POST'])
def borrar(receta_id):
    database.borrar_receta(receta_id)
    if is_fetch(): return json_ok('/')
    return redirect('/')
