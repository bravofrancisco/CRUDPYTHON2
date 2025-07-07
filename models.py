import enum
from sqlalchemy import  String, Enum
from datetime import date, datetime
from database import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, DateTime

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
    citas: Mapped[list["Cita"]]= relationship("Cita", back_populates="paciente")

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


class Doctor(db.Model):
    __tablename__ = 'doctores'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    especialidad: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)

    # Relación inversa con citas
    citas: Mapped[list["Cita"]] = relationship("Cita", back_populates="doctor")


class Cita(db.Model):
    __tablename__ = 'citas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_hora: Mapped[datetime] = mapped_column(nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=True)

    # Foreign keys
    paciente_id: Mapped[int] = mapped_column(ForeignKey('pacientes.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey('doctores.id'), nullable=False)

    # Relaciones
    paciente: Mapped["Paciente"] = relationship("Paciente", back_populates="citas")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="citas")    