import reflex as rx
from sqlmodel import select
from SerwisUI.models import Pracownik as Entry
from SerwisUI.UI import navbar

class State(rx.State):

    new_imie: str = ""
    new_nazwisko: str = ""
    new_stanowisko: str = ""
    entries: list[Entry] = []
    edit_id: int | None = None
    error_message: str = ""


    def load_entries(self):
        with rx.session() as session:
            statement = select(Entry)
            results = session.exec(statement)
            self.entries = results.all()

    def add_entry(self):
        if not  self.new_imie.strip() or not self.new_nazwisko.strip() or not self.new_stanowisko.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""


        entry = Entry(

            imie=self.new_imie,
            nazwisko=self.new_nazwisko,
            stanowisko=self.new_stanowisko,

        )




        with rx.session() as session:
            session.add(entry)
            session.commit()
        # od razu odśwież dane
        self.load_entries()

        self.new_imie = ""
        self.new_nazwisko = ""
        self.new_stanowisko = ""


    def delete_entry(self, entry_id: int):
        with rx.session() as session:
            entry = session.get(Entry, entry_id)
            if entry:
                session.delete(entry)
                session.commit()
        self.load_entries()


def main_pracownik() -> rx.Component:
    return rx.container(
            rx.vstack(
            rx.heading("Dodaj pracownika:", font_size="1.5em"),

            rx.input(
                placeholder="Imie pracownika...",
                value=State.new_imie,
                on_change=State.set_new_imie,
                max_length=50,
            ),
            rx.input(
                placeholder="Nazwisko pracownika...",
                value=State.new_nazwisko,
                on_change=State.set_new_nazwisko,
                max_length=50,
            ),
            rx.input(
                placeholder="Stanowisko...",
                value=State.new_stanowisko,
                on_change=State.set_new_stanowisko,
                max_length=50,
            ),



            rx.button("Dodaj", on_click=State.add_entry),
            rx.cond(
                State.error_message,
                rx.text(State.error_message, color="red", weight="bold"),
            ),
            rx.divider(),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID pracownika"),
                        rx.table.column_header_cell("Imie pracownika"),
                        rx.table.column_header_cell("Nazwisko pracownika"),
                        rx.table.column_header_cell("Stanowisko"),
                        rx.table.column_header_cell("Opcje"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.entries,
                        lambda entry: rx.table.row(
                            rx.table.cell(entry.pracownik_id),
                            rx.table.cell(entry.imie),
                            rx.table.cell(entry.nazwisko),
                            rx.table.cell(entry.stanowisko),
                            rx.table.cell(rx.button("Usuń", on_click=lambda: State.delete_entry(entry.pracownik_id), color_scheme="red"))
                        ),
                    ),
                ),
                on_mount=State.load_entries,
                width="100%",
            ),
            spacing="3",
        )
    )

def pracownicy() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main_pracownik(),
    )