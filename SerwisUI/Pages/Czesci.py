import reflex as rx
from sqlmodel import select
from SerwisUI.models import UzycieCzesci as Entry
from SerwisUI.UI import navbar
from SerwisUI.models import CzescZamienna


class State(rx.State):
    new_zlecenie_id: str = ""
    new_czesc_id: str = ""
    new_ilosc: str= ""
    entries: list[Entry] = []
    edit_id: int | None = None
    error_message: str = ""




    def load_entries(self):
        with rx.session() as session:
            statement = select(Entry)
            results = session.exec(statement)
            self.entries = results.all()

    def add_entry(self):
        if not self.new_zlecenie_id.strip() or not self.new_czesc_id.strip() or not self.new_ilosc.strip():
            self.error_message = "Wypełnij wszystkie pola!"
            return
        self.error_message = ""


        try:
            id_zlecenia = int(self.new_zlecenie_id)
            id_czesci = int(self.new_czesc_id)
            ilosci = float(self.new_ilosc)

        except ValueError:
            self.error_message = "Musza być liczby"
            return


        entry = Entry(
           zlecenie_id = id_zlecenia,
           czesc_id = id_czesci,
           ilosc = ilosci,
        )




        with rx.session() as session:
            czesc = session.get(CzescZamienna, id_czesci)
            if czesc:
                if czesc.dostepnosc >= ilosci:
                    czesc.dostepnosc -= int(ilosci)
                    session.add(entry)
                    session.commit()
                else:
                    self.error_message = "Niewystarczająca ilość części w magazynie."
                    return
            else:
                self.error_message = "Część o podanym ID nie istnieje."
                return
        # od razu odśwież dane
        self.load_entries()
        self.new_zlecenie_id = ""
        self.new_czesc_id = ""
        self.new_ilosc = ""



    def delete_entry(self, entry_id: int):
        with rx.session() as session:
            entry = session.get(Entry, entry_id)
            if entry:
                czesc = session.get(CzescZamienna, entry.czesc_id)
                if czesc:
                    czesc.dostepnosc += int(entry.ilosc)
                session.delete(entry)
                session.commit()
        self.load_entries()


def main_czesci() -> rx.Component:
    return rx.container(
            rx.vstack(
            rx.heading("Dodaj zużycie części:", font_size="1.5em"),
            rx.input(
                placeholder="ID zlecenia...",
                value=State.new_zlecenie_id,
                on_change=State.set_new_zlecenie_id,
                max_length=50,
            ),
            rx.input(
                placeholder="ID części...",
                value=State.new_czesc_id,
                on_change=State.set_new_czesc_id,
                max_length=50,
            ),
            rx.input(
                placeholder="ilość...",
                value=State.new_ilosc,
                on_change=State.set_new_ilosc,
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
                        rx.table.column_header_cell("ID użycia czesci"),
                        rx.table.column_header_cell("ID zlecenia"),
                        rx.table.column_header_cell("ID czesci"),
                        rx.table.column_header_cell("Ilosc"),
                        rx.table.column_header_cell("Opcje"),

                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.entries,
                        lambda entry: rx.table.row(
                            rx.table.cell(entry.uzycie_id),
                            rx.table.cell(entry.zlecenie_id),
                            rx.table.cell(entry.czesc_id),
                            rx.table.cell(entry.ilosc),
                            rx.table.cell(rx.button("Usuń", on_click=lambda: State.delete_entry(entry.uzycie_id), color_scheme="red"))
                        ),
                    ),
                ),
                on_mount=State.load_entries,
                width="100%",
            ),
            spacing="3",

        )
    )

def czesci() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main_czesci(),
    )