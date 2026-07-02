from flask import Flask, redirect, url_for, jsonify, render_template
import db as database
from modules.tareas.routes       import bp as tareas_bp
from modules.eventos.routes      import bp as eventos_bp
from modules.recetas.routes      import bp as recetas_bp
from modules.limpieza.routes     import bp as limpieza_bp
from modules.comida.routes       import bp as comida_bp
from modules.hoteles.routes      import bp as hoteles_bp
from modules.restaurantes.routes import bp as restaurantes_bp
from modules.frances.routes      import bp as frances_bp

app = Flask(__name__)
database.init_db()

for bp in (tareas_bp, eventos_bp, recetas_bp, limpieza_bp, comida_bp, hoteles_bp, restaurantes_bp, frances_bp):
    app.register_blueprint(bp)


@app.context_processor
def inject_sidebar():
    return {
        'sidebar_tareas':       database.todas_las_tareas(),
        'sidebar_eventos':      database.todos_los_eventos(),
        'sidebar_recetas':      database.todas_las_recetas(),
        'sidebar_limpiezas':    database.todas_las_limpiezas(),
        'sidebar_comidas':      database.todas_las_comidas(),
        'sidebar_hoteles':      database.todos_los_hoteles(),
        'sidebar_restaurantes': database.todos_los_restaurantes(),
        'sidebar_frances':      database.todas_las_frances(),
    }


@app.route('/')
def index():
    return redirect(url_for('tareas.index'))


@app.route('/api/sidebar')
def api_sidebar():
    return jsonify({'html': render_template('_sidebar.html')})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
