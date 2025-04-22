from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,Column,ForeignKey,Table
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

relacion_user_planeta=Table(
    "relacion_user_planeta",
    db.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("planeta_id", ForeignKey("planetas.id"), primary_key=True)
)

relacion_user_nave=Table(
    "relacion_user_nave",
    db.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("nave_id", ForeignKey("naves.id"), primary_key=True)
)
relacion_user_people=Table(
    "relacion_user_people",
    db.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("people_id", ForeignKey("people.id"), primary_key=True)
)

class User(db.Model):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)


    people_favoritos:Mapped[list["People"]]=relationship(secondary=relacion_user_people,back_populates="favotiro_por")
    planetas_favoritos:Mapped[list["Planet"]]=relationship(secondary=relacion_user_planeta,back_populates="favotiro_por")
    naves_favoritos:Mapped[list["Nave"]]=relationship(secondary=relacion_user_nave,back_populates="favotiro_por")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

            }
    

class People(db.Model):
    __tablename__="people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=False)

    favotiro_por:Mapped[list["User"]]=relationship(secondary=relacion_user_people,back_populates="people_favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color,
            }
    
class Planet(db.Model):
    __tablename__="planetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)
    gravity: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[str] = mapped_column(String(50), nullable=False)

    favotiro_por:Mapped[list["User"]]=relationship(secondary=relacion_user_planeta,back_populates="planetas_favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "population": self.population,
            }

class Nave(db.Model):
    __tablename__="naves"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(String(50), nullable=False)
    crew: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)

    favotiro_por:Mapped[list["User"]]=relationship(secondary=relacion_user_nave,back_populates="naves_favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo_capacity": self.cargo_capacity,
            "crew": self.crew,
            "model": self.model,
            }
