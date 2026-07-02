from flask import Blueprint, render_template, request, redirect, url_for
import db as database
from modules.utils import is_fetch, json_ok

bp = Blueprint('hoteles', __name__, url_prefix='/hoteles')


@bp.route('/')
def index():
    hoteles = database.todos_los_hoteles()
    return render_template('hoteles.html', hoteles=hoteles)


@bp.route('/<int:hotel_id>')
def ver(hotel_id):
    hotel = next((h for h in database.todos_los_hoteles() if h['id'] == hotel_id), None)
    if not hotel:
        return redirect('/')
    return render_template('hotel_ver.html', hotel=hotel)


@bp.route('/nuevo', methods=['POST'])
def nuevo():
    hotel_id = database.crear_hotel('Nuevo hotel', '')
    url = url_for('hoteles.ver', hotel_id=hotel_id)
    if is_fetch(): return json_ok(url)
    return redirect(url)


@bp.route('/<int:hotel_id>/editar', methods=['POST'])
def editar(hotel_id):
    database.editar_hotel(
        hotel_id,
        titulo=request.form.get('titulo', '').strip(),
        contenido=request.form.get('contenido', ''),
    )
    if is_fetch(): return json_ok()
    return redirect(url_for('hoteles.ver', hotel_id=hotel_id))


@bp.route('/<int:hotel_id>/borrar', methods=['POST'])
def borrar(hotel_id):
    database.borrar_hotel(hotel_id)
    if is_fetch(): return json_ok('/')
    return redirect('/')
