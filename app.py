# importando flask
from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

# creamos la instancia de Flask
app = Flask(__name__)

# configurar nuestra aplicacion para crear nuestro modelo de bd
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///tareas.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    # columna identificador unico
    id = db.Column(db.Integer, primary_key=True)
    # columna titulo
    titulo = db.Column(db.String(100), nullable=False)
    # columnas descripcion
    descripcion =db.Column(db.Text, nullable=True)
    # columna prioridad
    prioridad = db.Column(db.String(20), nullable=True)
    # columnas para las fechas
    fecha_inicio = db.Column(db.String(20), nullable=True)
    fecha_fin = db.Column(db.String(20), nullable=True)
    # estado de la tarea
    estado = db.Column(db.String(20), nullable=True)
    
    
with app.app_context():
    db.create_all() # crea todas las tablas definidas



@app.route('/', methods=['GET'])
def home():
    # consulta a la base de datos
    tareas = Tarea.query.all()
    return render_template('index.html', tarea=tareas)


@app.route('/tarea', methods=['POST'])
def manejar_tarea():
    accion = request.form.get('accion')
    tarea_id = request.form.get('id')
    print('action', accion)
    if accion == 'agregar':
        nueva = Tarea(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            prioridad=request.form.get('prioridad'),
            fecha_inicio=request.form.get('fecha_inicio'),
            fecha_fin=request.form.get('fecha_fin'),
            estado=request.form.get('estado')
        )
        print(accion)
        db.session.add(nueva)
        db.session.commit()
        
        # si la operacion es editar
    elif accion == 'editar' and tarea_id:
        #buscar la tarea por su id en la base de datos
        tarea =Tarea.query.get(tarea_id)
        
        tareas = Tarea.query.all()
        
        return render_template('index.html', tarea=tareas, tarea_editando=tarea)
    
    elif accion == 'actualizar' and tarea_id:
        tarea = Tarea.query.get(tarea_id)
        
        # si la tarea existe, actualizamos con los nuevos datos
        if tarea:
            tarea.titulo = request.form.get('titulo')
            tarea.descripcion = request.form.get('descripcion')
            tarea.prioridad = request.form.get('prioridad')
            tarea.fecha_inicio = request.form.get('fecha_inicio')
            tarea.fecha_limite = request.form.get('fecha_limite')
            tarea.estado = request.form.get('estado')
            
            db.session.commit()
            
            # si la opcion es eliminar
    elif accion == 'eliminar' and tarea_id:
            # buscar la tarea que queremos borrar
            tarea = Tarea.query.get(tarea_id)
            
            # si la tarea existe, marcar para borrar
            if tarea:
                db.session.delete(tarea)
                # confirmar la eliminacion de la base de datos
                db.session.commit()
                
        # finalmnete redirigimos a la pagina principal
    return redirect('/')




if __name__ == "__main__":
    app.run()