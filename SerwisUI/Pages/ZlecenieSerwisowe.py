import reflex as rx
from sqlmodel import select
from SerwisUI.models import ZlecenieSerwisowe as Entry
from SerwisUI.UI import navbar

class State(rx.State):

    new_pojazd_id: str = ""
    new_pracownik_id: str = ""
    new_opis_problemu:str = ""
    new_wykonane_naprawy: str = ""
    new_koszt_calkowity: str = ""
    entries: list[Entry] = []
    edit_id: int | None = None
    error_message: str = ""



    def load_entries(self):
        with rx.session() as session:
            statement = select(Entry)
            results = session.exec(statement)
            entries = results.all()
            # Konwertujemy decimal na float żeby serializacja była git
            for e in entries:
                e.koszt_calkowity = float(e.koszt_calkowity)
            self.entries = entries

    def add_entry(self):
        if not  self.new_pojazd_id.strip() or not self.new_pracownik_id.strip() or not self.new_opis_problemu.strip() or not self.new_wykonane_naprawy.strip() or not self.new_koszt_calkowity.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""


        try:
            id_pojazdu = int(self.new_pojazd_id)
            id_pracownika = int(self.new_pracownik_id)
            koszt = float(self.new_koszt_calkowity)

        except ValueError:
            self.error_message = "ID pojazdu, ID pracownika lub koszt całkowity muszą być liczbami!"
            return


        entry = Entry(

            pojazd_id = id_pojazdu,
            pracownik_id = id_pracownika,
            opis_problemu=self.new_opis_problemu,
            wykonane_naprawy=self.new_wykonane_naprawy,
            koszt_calkowity=koszt,
        )




        with rx.session() as session:
            session.add(entry)
            session.commit()
        # od razu odśwież dane
        self.load_entries()

        self.new_pojazd_id = ""
        self.new_pracownik_id = ""
        self.new_opis_problemu = ""
        self.new_wykonane_naprawy = ""
        self.new_koszt_calkowity = ""



    def delete_entry(self, entry_id: int):
        with rx.session() as session:
            entry = session.get(Entry, entry_id)
            if entry:
                session.delete(entry)
                session.commit()
        self.load_entries()


def main_zlecenie() -> rx.Component:
    return rx.container(
            rx.vstack(
            rx.heading("Dodaj zlecenie serwisowe:", font_size="1.5em"),

            rx.input(
                placeholder="ID pojazdu...",
                value=State.new_pojazd_id,
                on_change=State.set_new_pojazd_id,
                max_length=50,
            ),
            rx.input(
                placeholder="ID pracownika...",
                value=State.new_pracownik_id,
                on_change=State.set_new_pracownik_id,
                max_length=50,
            ),
            rx.input(
                placeholder="Opis problemu...",
                value=State.new_opis_problemu,
                on_change=State.set_new_opis_problemu,
            ),
            rx.input(
                placeholder="Wykonane naprawy...",
                value=State.new_wykonane_naprawy,
                on_change=State.set_new_wykonane_naprawy
            ),
            rx.input(
                placeholder="Koszt naprawy...",
                value=State.new_koszt_calkowity,
                on_change=State.set_new_koszt_calkowity,
                max_length=50,
            ),
            rx.hstack(
                rx.button("Dodaj", on_click=State.add_entry),
                rx.button("Użyte części", on_click=rx.redirect("/czesci")),
            ),
            rx.cond(
                State.error_message,
                rx.text(State.error_message, color="red", weight="bold"),
            ),
            rx.divider(),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID zlecenia"),
                        rx.table.column_header_cell("ID pojazdu"),
                        rx.table.column_header_cell("ID pracownika"),
                        rx.table.column_header_cell("Data zlecenia"),
                        rx.table.column_header_cell("Opis problemu"),
                        rx.table.column_header_cell("Wykonane naprawy"),
                        rx.table.column_header_cell("Koszt"),
                        rx.table.column_header_cell("Opcje"),

                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.entries,
                        lambda entry: rx.table.row(
                            rx.table.cell(entry.zlecenie_id),
                            rx.table.cell(entry.pojazd_id),
                            rx.table.cell(entry.pracownik_id),
                            rx.table.cell(entry.data_zlecenia),
                            rx.table.cell(entry.opis_problemu),
                            rx.table.cell(entry.wykonane_naprawy),
                            rx.table.cell(
                                rx.text(entry.koszt_calkowity.to_string() + " zł")
                                          ),
                            rx.table.cell(rx.button("Usuń", on_click=lambda: State.delete_entry(entry.zlecenie_id), color_scheme="red"))
                        ),
                    ),
                ),
                on_mount=State.load_entries,
                width="100%",
            ),
            spacing="3",
        )
    )

def zlecenia() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main_zlecenie(),
    )