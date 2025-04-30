import reflex as rx
from sqlmodel import select
from SerwisUI.models import Klient
from SerwisUI.UI import navbar

class State(rx.State):
    new_imie: str = ""
    new_nazwisko: str = ""
    new_nr_telefonu: str = ""
    new_email: str = ""
    new_adres: str = ""
    klienci: list[Klient] = []
    edit_id: int | None = None
    error_message: str = ""


    def load_klienci(self):
        with rx.session() as session:
            statement = select(Klient)
            results = session.exec(statement)
            self.klienci = results.all()

    def add_klient(self):
        if not self.new_imie.strip() or not self.new_nazwisko.strip() or not self.new_nr_telefonu.strip() or not self.new_email.strip() or not self.new_adres.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""

        klient = Klient(imie=self.new_imie, nazwisko=self.new_nazwisko, nr_telefonu=self.new_nr_telefonu, email=self.new_email, adres=self.new_adres)
        with rx.session() as session:
            session.add(klient)
            session.commit()
        # od razu odśwież dane
        self.load_klienci()
        self.new_imie = ""
        self.new_nazwisko = ""
        self.new_nr_telefonu = ""
        self.new_email = ""
        self.new_adres = ""

    def delete_klient(self, klient_id: int):
        with rx.session() as session:
            klient = session.get(Klient, klient_id)
            if klient:
                session.delete(klient)
                session.commit()
        self.load_klienci()

# Front-End

def main_klienci() -> rx.Component:
    return rx.container(
            rx.vstack(
            rx.heading("Dodaj klienta:", font_size="1.5em"),
            rx.input(
                placeholder="Imie klienta...",
                value=State.new_imie,
                on_change=State.set_new_imie,
                max_length=50,
            ),
            rx.input(
                placeholder="Nazwisko klienta...",
                value=State.new_nazwisko,
                on_change=State.set_new_nazwisko,
                max_length=50,
            ),
            rx.input(
                placeholder="Numer telefonu...",
                value=State.new_nr_telefonu,
                on_change=State.set_new_nr_telefonu,
                max_length=15,
            ),
            rx.input(
                placeholder="Adres e-mail...",
                value=State.new_email,
                on_change=State.set_new_email,
                max_length=100,
            ),
            rx.input(
                placeholder="Wpisz adres...",
                value=State.new_adres,
                on_change=State.set_new_adres,
                max_length=255,
            ),
            rx.button("Dodaj", on_click=State.add_klient),
            rx.cond(
                State.error_message,
                rx.text(State.error_message, color="red", weight="bold"),
            ),
            rx.divider(),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID Klienta"),
                        rx.table.column_header_cell("Imie"),
                        rx.table.column_header_cell("Nazwisko"),
                        rx.table.column_header_cell("Telefon"),
                        rx.table.column_header_cell("E-mail"),
                        rx.table.column_header_cell("Adres"),
                        rx.table.column_header_cell("Opcje"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.klienci,
                        lambda klient: rx.table.row(
                            rx.table.cell(klient.klient_id),
                            rx.table.cell(klient.imie),
                            rx.table.cell(klient.nazwisko),
                            rx.table.cell(klient.nr_telefonu),
                            rx.table.cell(klient.email),
                            rx.table.cell(klient.adres),
                            rx.table.cell(rx.button("Usuń", on_click=lambda: State.delete_klient(klient.klient_id), color_scheme="red"))
                        ),
                    ),
                ),
                on_mount=State.load_klienci,
                width="100%",
            ),
            spacing="3",
        )
    )

def klienci() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main_klienci(),
    )
