import enum
from sqlalchemy import  String, Enum
from datetime import date
from database import db
from sqlalchemy.orm import Mapped, mapped_column

class GeneroEnum(enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"

class Paciente(db.Model):
    
    __tablename__ = 'pacientes'

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    nombre:Mapped[str] = mapped_column(type_=String(255),nullable=False)
    apellido:Mapped[str] = mapped_column(type_=String(255), nullable=False)
    fecha_nacimiento:Mapped[date] = mapped_column(nullable=False)
    genero:Mapped[GeneroEnum] = mapped_column(Enum(GeneroEnum),nullable=False)
    direccion:Mapped[str] = mapped_column(String(255),nullable=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    numero_documento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


    @property
    def genero_str(self) -> str:
        return self.genero.value if self.genero else "No definido"
    
    
    def __str__(self) -> str:
     return (
        f'id: {self.id}, '
        f'nombre: {self.nombre}, '
        f'apellido: {self.apellido}, '
        f'fecha_nacimiento: {self.fecha_nacimiento}, '
        f'genero: {self.genero.value}, '
        f'direccion: {self.direccion}, '
        f'telefono: {self.telefono}, '
        f'email: {self.email}, '
        f'numero_documento: {self.numero_documento}'
    )


