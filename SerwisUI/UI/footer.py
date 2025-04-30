import reflex as rx

def footer() -> rx.Component:
    return rx.el.footer(
        rx.text("© 2025 Serwis Samochodowy", font_size="0.8em"),
        margin_top="auto",
        padding="1em",
        text_align="center",
    )