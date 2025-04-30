import reflex as rx
from SerwisUI.UI import navbar
from SerwisUI.UI import gradientbutton as gbtn
from SerwisUI.Pages import Pojazd, Magazyn, Pracownik, Klienci, ZlecenieSerwisowe, Czesci


def main() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("🛠️ Serwis Samochodowy — Panel Zarządzania", font_size="2.5em", justify="center", padding="10rem 1rem 1rem 1rem"),
            rx.text(
                "Zarządzaj swoim serwisem w jednym miejscu. Zlecenia, klienci, pojazdy i części — wszystko pod ręką w przejrzystym panelu.",
                font_size="1.3em",
                padding="1rem 1rem 3rem 1rem",
                font_weight="medium"
            ),
            rx.vstack(
                rx.hstack(
                    gbtn.button("Przejdź do zleceń", rx.redirect("/zlecenie")),
                    gbtn.button("Przejdź do klientów", rx.redirect("/klienci")),
                    gbtn.button("Przejdź do pojazdów", rx.redirect("/pojazdy")),
                    justify="center",
                    align_items="center",
                    width="100%",
                ),
                rx.hstack(
                    gbtn.button("Przejdź do magazynu", rx.redirect("/magazyn")),
                    gbtn.button("Przejdź do pracowników", rx.redirect("/pracownicy")),
                    justify="center",
                    align_items="center",
                    width="100%",
                ),
                align_items = "center",
                width = "100%",
                spacing = "4"
            ),


        )



    )

def index() -> rx.Component:
    return rx.box(
        navbar.navbar(),
        rx.divider(),
        main(),
    )

app = rx.App()
app.add_page(index, route="/")
app.add_page(Klienci.klienci, route="/klienci")
app.add_page(Pojazd.pojazdy, route="/pojazdy")
app.add_page(Magazyn.magazyn, route="/magazyn")
app.add_page(Pracownik.pracownicy(), route="/pracownicy")
app.add_page(ZlecenieSerwisowe.zlecenia(), route="/zlecenie")
app.add_page(Czesci.czesci(), route="/czesci")
