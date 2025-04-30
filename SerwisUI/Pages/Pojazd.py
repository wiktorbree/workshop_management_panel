import reflex as rx
from sqlmodel import select
from SerwisUI.models import Pojazd as Entry
from SerwisUI.UI import navbar

class State(rx.State):
    new_klient_id: str = ""
    new_marka: str = ""
    new_model: str = ""
    new_rok_produkcji: str = ""
    new_numer_rejestracyjny: str = ""
    new_vin: str = ""
    entries: list[Entry] = []
    edit_id: int | None = None
    error_message: str = ""


    def load_entries(self):
        with rx.session() as session:
            statement = select(Entry)
            results = session.exec(statement)
            self.entries = results.all()

    def add_entry(self):
        if not self.new_klient_id.strip() or not self.new_marka.strip() or not self.new_model.strip() or not self.new_numer_rejestracyjny.strip() or not self.new_vin.strip() or not self.new_rok_produkcji.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""



        try:
            id_klienta = int(self.new_klient_id)
            rok = int(self.new_rok_produkcji)
        except ValueError:
            self.error_message = "Rok produkcji musi być liczbą!"
            return

        entry = Entry(
            klient_id=id_klienta,
            marka=self.new_marka,
            model=self.new_model,
            rok_produkcji=rok,
            numer_rejestracyjny=self.new_numer_rejestracyjny,
            vin=self.new_vin
        )



        with rx.session() as session:
            session.add(entry)
            session.commit()
        # od razu odśwież dane
        self.load_entries()
        self.new_klient_id = ""
        self.new_marka = ""
        self.new_model = ""
        self.new_rok_produkcji = ""
        self.new_numer_rejestracyjny = ""
        self.new_vin = ""

    def delete_entry(self, entry_id: int):
        with rx.session() as session:
            entry = session.get(Entry, entry_id)
            if entry:
                session.delete(entry)
                session.commit()
        self.load_entries()


def main() -> rx.Component:
    return rx.container(
            rx.vstack(
            rx.heading("Dodaj pojazd:", font_size="1.5em"),
            rx.input(
                placeholder="ID klienta...",
                value=State.new_klient_id,
                on_change=State.set_new_klient_id,
                max_length=50,
            ),
            rx.input(
                placeholder="Marka pojazdu...",
                value=State.new_marka,
                on_change=State.set_new_marka,
                max_length=50,
            ),
            rx.input(
                placeholder="Model pojazdu...",
                value=State.new_model,
                on_change=State.set_new_model,
                max_length=50,
            ),
            rx.input(
                placeholder="Rok produkcji pojazdu...",
                value=State.new_rok_produkcji,
                on_change=State.set_new_rok_produkcji,
                input_type="number",
            ),
            rx.input(
                placeholder="Numer rejestracyjny pojazdu...",
                value=State.new_numer_rejestracyjny,
                on_change=State.set_new_numer_rejestracyjny,
                max_length=8,
            ),
            rx.input(
                placeholder="VIN pojazdu...",
                value=State.new_vin,
                on_change=State.set_new_vin,
                max_length=17,
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
                        rx.table.column_header_cell("ID Pojazdu"),
                        rx.table.column_header_cell("ID Klienta"),
                        rx.table.column_header_cell("Marka"),
                        rx.table.column_header_cell("Model"),
                        rx.table.column_header_cell("Rok produkcji"),
                        rx.table.column_header_cell("Numer rejestracyjny"),
                        rx.table.column_header_cell("VIN"),
                        rx.table.column_header_cell("Opcje"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.entries,
                        lambda entry: rx.table.row(
                            rx.table.cell(entry.pojazd_id),
                            rx.table.cell(entry.klient_id),
                            rx.table.cell(entry.marka),
                            rx.table.cell(entry.model),
                            rx.table.cell(entry.rok_produkcji),
                            rx.table.cell(entry.numer_rejestracyjny),
                            rx.table.cell(entry.vin),
                            rx.table.cell(rx.button("Usuń", on_click=lambda: State.delete_entry(entry.pojazd_id), color_scheme="red"))
                        ),
                    ),
                ),
                on_mount=State.load_entries,
                width="100%",
            ),
            spacing="3",
        )
    )

def pojazdy() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main(),
    )