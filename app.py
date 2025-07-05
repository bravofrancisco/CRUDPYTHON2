from flask import Flask, flash, redirect, render_template, request, url_for
import os
from database import db
from flask_migrate import Migrate
from dotenv import load_dotenv
from forms import RegistrarForm
from models import Paciente
load_dotenv()

app = Flask(__name__)


USER_DB = os.getenv('USER_DB')
USER_PASSWORD = os.getenv('USER_PASSWORD')
SERVER_DB = os.getenv('SERVER_DB')
NAME_DB = os.getenv('NAME_DB')
SECRET_KEY = os.getenv('SECRET_KEY')

FULL_URL_DB = f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SECRET_KEY'] = SECRET_KEY or 'una_clave_secreta_muy_segura_por_defecto' # Usar una clave robusta aquí

db.init_app(app)

migrate = Migrate(app,db)



@app.route("/inicio")
def index():
    pacientes = Paciente.query.order_by(Paciente.id)
    total_pacientes = Paciente.query.count()
    return render_template('index.html',Total_Pacientes=pacientes, CantidadPacientes=total_pacientes) 

@app.route("/pacientes/<int:id>")
def ver_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('curso.html', datos=paciente)

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    registrarPaciente = Paciente()
    registrarFormulario = RegistrarForm(obj=registrarPaciente)
    if request.method == 'POST' and registrarFormulario.validate_on_submit():
        registrarFormulario.populate_obj(registrarPaciente)
        db.session.add(registrarPaciente)
        db.session.commit()
        flash('Curso insertado correcto', 'sucess')
        return redirect(url_for('index'))
    return render_template('insertar-curso.html',formulario=registrarFormulario)

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    registrarPaciente = Paciente.query.get_or_404(id)
    registrarForm = RegistrarForm(obj=registrarPaciente)
    if request.method == 'POST':
        # Validate the form data submitted via POST request.
        if registrarForm.validate_on_submit():
            # Populate the patient object with data from the validated form.
            registrarForm.populate_obj(registrarPaciente)
            try:
                # Commit the changes to the database.
                db.session.commit()
                flash("Paciente editado correctamente", 'success') # Changed 'sucess' to 'success'
                return redirect(url_for('index'))
            except Exception as e:
                # Rollback in case of a database error
                db.session.rollback()
                flash(f"Error al editar el paciente: {e}", 'danger')
                # Stay on the edit page to show error or allow retry
                return render_template('editar.html', formulario=registrarForm, paciente=registrarPaciente)
        else:
            # If form validation fails, flash an error message.
            flash("Por favor, corrige los errores en el formulario.", 'danger')
            # Render the template again with validation errors
            return render_template('editar.html', formulario=registrarForm, paciente=registrarPaciente)
            
    return render_template('editar.html', formulario=registrarForm, paciente=registrarPaciente)

 
@app.route('/eliminar/<int:id>')
def eliminar(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Curso eliminado correctamente.', 'success')
    return redirect(url_for('index'))

# @app.route('/editar/<int:id>')
# def editar(id):
#     pacientes = Paciente.query.get_or_404(id)
#     pacienteForm = 


if __name__ == '__main__':
    app.run(debug=True)