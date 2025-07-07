from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from database import db
from flask_migrate import Migrate
from dotenv import load_dotenv
from forms import RegistrarForm
from models import Cita, Doctor, Paciente
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('debes iniciar sesion para acceder a esta pagina' ,'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def inicio():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    # Validación simple para el usuario 'admin'.
        # En un sistema real, aquí buscarías el usuario en la base de datos
        # y verificarías la contraseña de forma segura (e.g., con hashes).
        if username == 'admin':
            if password == 'secret':
                session['logged_in'] = True
                # Puedes usar flash para un mensaje de éxito también
                flash('Has iniciado sesión exitosamente como administrador.', 'success')
                return redirect(url_for('inicio')) # Redirige a la página principal de cursos
            else:
                # Mensaje si la contraseña es incorrecta para 'admin'
                flash('Contraseña incorrecta para el usuario admin.', 'danger')
        else:
            # Mensaje si el usuario no es 'admin' o no coincide con 'admin'
            flash('Usuario o contraseña inválidos. Asegúrate de usar "admin" y "secret".', 'danger')

        # Vuelve a renderizar el login con el mensaje de error flasheado
        return render_template('login.html') 

    return render_template('login.html')   


@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('Has cerrado session exitosamente','success')
    return redirect(url_for('login'))

@app.route("/inicio")
@login_required
def index():
    pacientes = Paciente.query.order_by(Paciente.id).all()
    total_pacientes = Paciente.query.count()
    return render_template('index.html',Total_Pacientes=pacientes, CantidadPacientes=total_pacientes) 



@app.route("/pacientes/<int:id>")
def ver_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('curso.html', datos=paciente)

@app.route('/registrar', methods=['GET','POST'])
@login_required
def registrar():
    registrarPaciente = Paciente()
    registrarFormulario = RegistrarForm(obj=registrarPaciente)
    if request.method == 'POST' and registrarFormulario.validate_on_submit():
        registrarFormulario.populate_obj(registrarPaciente)
        db.session.add(registrarPaciente)
        db.session.commit()
        flash('Paciente insertado correcto', 'success')
        return redirect(url_for('index'))
    return render_template('insertar-curso.html',formulario=registrarFormulario)

@app.route('/editar/<int:id>', methods=['GET','POST'])
@login_required
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
@login_required
def eliminar(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Curso eliminado correctamente.', 'success')
    return redirect(url_for('index'))


@app.route("/ver_citas")
@login_required # Protege esta ruta también
def ver_citas():
    citas_completas = [] # Inicializa como lista vacía
    total_citas = 0

    try:
        # Consulta para obtener las citas con la información de paciente y doctor
        citas_completas = db.session.query(
            Cita.id,
            Cita.fecha_hora,
            Cita.motivo,
            Paciente.nombre.label('paciente_nombre'),
            Paciente.apellido.label('paciente_apellido'),
            Doctor.nombre.label('doctor_nombre'),
            Doctor.especialidad
        ).join(Paciente, Cita.paciente_id == Paciente.id)\
         .join(Doctor, Cita.doctor_id == Doctor.id)\
         .order_by(Cita.fecha_hora)\
         .all()
        
        total_citas = len(citas_completas)
        # print(f"DEBUG: Citas obtenidas para /ver_citas: {total_citas} registros.")
        # print("DEBUG: Primeros 5 registros de citas (/ver_citas):", citas_completas[:5]) # Muestra los primeros 5

    except Exception as e:
        flash(f"Error al cargar las citas: {e}", 'danger')
        print(f"ERROR: Fallo al cargar citas en /ver_citas: {e}")
        # En caso de error, citas_completas ya está inicializada como []

    # Renderiza una plantilla específica para las citas detalladas
    return render_template('ver_citas.html', VerCitas=citas_completas, TotalCitas=total_citas)


if __name__ == '__main__':
    app.run(debug=True)