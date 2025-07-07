from wtforms import StringField, SubmitField, DateField, SelectField, EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError
from flask_wtf import FlaskForm
from datetime import date

class Capitalized(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0].strip()
            self.data = value.title()  # Capitaliza cada palabra

def validar_fecha_pasada(form, field):
    if field.data > date.today():
        raise ValidationError("La fecha de nacimiento no puede ser futura.")

class RegistrarForm(FlaskForm):
    nombre = Capitalized('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(min=3, max=40, message="El nombre debe tener entre 3 y 40 caracteres")
    ])
    apellido = Capitalized('Apellido', validators=[
        DataRequired(message="El apellido es obligatorio"),
        Length(min=3, max=40, message="El apellido debe tener entre 3 y 40 caracteres")
    ])
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[
        DataRequired(message="La fecha de nacimiento es obligatoria"),
        validar_fecha_pasada
    ])
    genero = SelectField('Género', choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], validators=[DataRequired(message="El género es obligatorio")])
    direccion = StringField('Dirección', validators=[
        DataRequired(message="La dirección es obligatoria"),
        Length(min=3, max=255)
    ])
    telefono = StringField('Teléfono', validators=[
        Length(min=3, max=20, message="El teléfono debe tener entre 3 y 20 caracteres"),
        Regexp(r'^\+?\d{7,15}$', message="Formato de teléfono no válido")
    ])
    email = EmailField('Correo electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio"),
        Email(message="Ingrese un correo electrónico válido"),
        Length(max=255)
    ])
    numero_documento = StringField('Número de documento', validators=[
        DataRequired(message="El número de documento es obligatorio"),
        Length(min=3, max=50, message="Debe tener entre 3 y 50 caracteres")
    ])
    
    enviar = SubmitField('Enviar')
