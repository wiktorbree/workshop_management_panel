import reflex as rx

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="3", weight="medium"), href=url,
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        rx.link("Serwis", href="/"),
                        size="6",
                        weight="bold",
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Zlecenie", "/zlecenie"),
                    navbar_link("Klienci", "/klienci"),
                    navbar_link("Pojazdy", "/pojazdy"),
                    navbar_link("Magazyn", "/magazyn"),
                    navbar_link("Pracownicy", "/pracownicy"),
                    rx.color_mode.button(),
                    justify="end",
                    spacing="5",
                    align_items="center",
                ),
                justify="between",
                align_items="center",
            ),
            padding="1rem 15rem 1rem 15rem",
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        rx.link("Serwis", href="/"),
                        size="6",
                        weight="bold",
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        rx.menu.item("Zlecenie", on_click=rx.redirect("/zlecenie")),
                        rx.menu.item("Klienci", on_click=rx.redirect("/klienci")),
                        rx.menu.item("Pojazdy", on_click=rx.redirect("/pojazdy")),
                        rx.menu.item("Magazyn", on_click=rx.redirect("/magazyn")),
                        rx.menu.item("Pracownicy", on_click=rx.redirect("/pracownicy")),
                        rx.menu.item(rx.color_mode.button()),
                    ),
                    justify="end",
                    align_items="center",
                ),
                justify="between",
                align_items="center",
            ),
            padding="1rem 2rem 1rem 2rem",
        ),
        width="100%",
    )