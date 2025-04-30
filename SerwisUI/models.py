import reflex as rx
from sqlmodel import Field
from datetime import date
from sqlalchemy import Column
from sqlalchemy.types import Numeric


class Klient(rx.Model, table=True):
    klient_id: int | None = Field(default=None, primary_key=True)
    imie: str = Field(nullable=False, max_length=50)
    nazwisko: str = Field(nullable=False, max_length=50)
    nr_telefonu: str = Field(nullable=False, max_length=15)
    email: str = Field(nullable=False, max_length=100)
    adres: str = Field(nullable=False, max_length=255)

class Pojazd(rx.Model, table=True):
    pojazd_id: int | None = Field(default=None, primary_key=True)
    klient_id: int = Field(foreign_key="klient.klient_id")
    marka: str = Field(nullable=False, max_length=50)
    model: str = Field(nullable=False, max_length=50)
    rok_produkcji: int = Field(nullable=False)
    numer_rejestracyjny: str = Field(nullable=False, max_length=8)
    vin: str = Field(nullable=False, max_length=17)

class CzescZamienna(rx.Model, table=True):
    czesc_id: int | None = Field(default=None, primary_key=True)
    nazwa: str = Field(nullable=False, max_length=100)
    numer_seryjny: str = Field(nullable=False, max_length=50)
    cena: float = Field(
        default=0.0,
        sa_column=Column(Numeric(10, 2), nullable=False),
    )
    dostepnosc: int = Field(nullable=False)

class Pracownik(rx.Model, table=True):
    pracownik_id: int | None = Field(default=None, primary_key=True)
    imie: str = Field(nullable=False, max_length=50)
    nazwisko: str = Field(nullable=False, max_length=50)
    stanowisko: str = Field(nullable=False, max_length=50)

class ZlecenieSerwisowe(rx.Model, table=True):
    zlecenie_id: int | None = Field(default=None, primary_key=True)
    pojazd_id: int = Field(foreign_key="pojazd.pojazd_id")
    pracownik_id: int = Field(foreign_key="pracownik.pracownik_id")
    data_zlecenia: date = Field(default_factory=date.today, nullable=False)
    opis_problemu: str = Field(nullable=False)
    wykonane_naprawy: str = Field(nullable=False)
    koszt_calkowity: float = Field(
        default=0.0,
        sa_column=Column(Numeric(10, 2), nullable=False),)

class UzycieCzesci(rx.Model, table=True):
    uzycie_id: int | None = Field(default=None, primary_key=True)
    zlecenie_id: int = Field(foreign_key="zlecenieserwisowe.zlecenie_id")
    czesc_id: int = Field(foreign_key="czesczamienna.czesc_id")
    ilosc: int = Field(nullable=False)