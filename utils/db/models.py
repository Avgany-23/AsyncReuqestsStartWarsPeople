from sqlalchemy.orm import Mapped, mapped_column
from utils.db.basic import Base


class StartWarsPeople(Base):
    __tablename__ = 'startwarspeople'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_character: Mapped[int]
    birth_year: Mapped[str | None]
    eye_color: Mapped[str | None]
    films: Mapped[str | None]
    gender: Mapped[str | None]
    hair_color: Mapped[str | None]
    height: Mapped[str | None]
    homeworld: Mapped[str | None]
    mass: Mapped[str | None]
    name: Mapped[str | None]
    skin_color: Mapped[str | None]
    species: Mapped[str | None]
    starships: Mapped[str | None]
    vehicles: Mapped[str | None]
