from wtforms import StringField, SubmitField, DateField, SelectField, EmailField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm


# Campo personalizado que capitaliza la entrada
class Capitalized(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0].strip()
            self.data = value.capitalize()


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
        DataRequired(message="La fecha de nacimiento es obligatoria")
    ])
    genero = SelectField('Género', choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro')
    ], validators=[DataRequired(message="El género es obligatorio")])
    direccion = StringField('Dirección', validators=[
        Length(min=3, max=255, message="La dirección debe tener entre 3 y 255 caracteres")
    ])
    telefono = StringField('Teléfono', validators=[
        Length(min=3, max=20, message="El teléfono debe tener entre 3 y 20 caracteres")
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
