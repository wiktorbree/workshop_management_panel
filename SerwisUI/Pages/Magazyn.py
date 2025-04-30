import reflex as rx
from sqlmodel import select
from SerwisUI.models import CzescZamienna as Entry
from SerwisUI.UI import navbar
class State(rx.State):
    new_nazwa: str = ""
    new_numer_seryjny: str = ""
    new_cena: str = ""
    new_dostepnosc: str = ""
    entries: list[Entry] = []
    error_message: str = ""

    def load_entries(self):
        with rx.session() as session:
            statement = select(Entry)
            results = session.exec(statement)
            entries = results.all()
            # Konwertujemy decimal na float żeby serializacja była git
            for e in entries:
                e.cena = float(e.cena)
            self.entries = entries

    def add_entry(self):
        if not self.new_nazwa.strip() or not self.new_numer_seryjny.strip() or not self.new_cena.strip() or not self.new_dostepnosc.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""

        try:
            cena_float = float(self.new_cena)
        except ValueError:
            self.error_message = "Cena musi być wartością liczbową!"
            return

        entry = Entry(
            nazwa=self.new_nazwa,
            numer_seryjny=self.new_numer_seryjny,
            cena = cena_float,
            dostepnosc=self.new_dostepnosc,
        )

        with rx.session() as session:
            session.add(entry)
            session.commit()

        self.load_entries()
        self.new_nazwa = ""
        self.new_numer_seryjny = ""
        self.new_cena = ""
        self.new_dostepnosc = ""

    def delete_entry(self, entry_id: int):
        with rx.session() as session:
            entry = session.get(Entry, entry_id)
            if entry:
                session.delete(entry)
                session.commit()
        self.load_entries()


def main_magazyn() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Dodaj część:", font_size="1.5em"),
            rx.input(
                placeholder="Nazwa części...",
                value=State.new_nazwa,
                on_change=State.set_new_nazwa,
                max_length=100,
            ),
            rx.input(
                placeholder="Numer seryjny części...",
                value=State.new_numer_seryjny,
                on_change=State.set_new_numer_seryjny,
                max_length=50,
            ),
            rx.input(
                placeholder="Cena części...",
                value=State.new_cena,
                on_change=State.set_new_cena,
                input_type="number",
            ),
            rx.input(
                placeholder="Dostępność...",
                value=State.new_dostepnosc,
                on_change=State.set_new_dostepnosc,
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
                        rx.table.column_header_cell("ID Części"),
                        rx.table.column_header_cell("Nazwa"),
                        rx.table.column_header_cell("Numer seryjny"),
                        rx.table.column_header_cell("Cena"),
                        rx.table.column_header_cell("Dostępność"),
                        rx.table.column_header_cell("Opcje"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.entries,
                        lambda entry: rx.table.row(
                            rx.table.cell(entry.czesc_id),
                            rx.table.cell(entry.nazwa),
                            rx.table.cell(entry.numer_seryjny),
                            rx.table.cell(
                                rx.text(entry.cena.to_string() + " zł")
                            ),
                            rx.table.cell(entry.dostepnosc),
                            rx.table.cell(
                                rx.button(
                                    "Usuń",
                                    on_click=lambda entry_id=entry.czesc_id: State.delete_entry(entry_id),
                                    color_scheme="red"
                                )
                            )
                        ),
                    ),
                ),
                on_mount=State.load_entries,
                width="100%",
            ),
            spacing="3",
        )
    )

def magazyn() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main_magazyn(),
    )