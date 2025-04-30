import reflex as rx

def button(text: str, click_action):
    return rx.button(
        text,
        on_click=click_action,
        background_image="linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%)",
        border_radius="8px",
        box_sizing="border-box",
        color="#ffffff",
        cursor="pointer",
        flex_shrink="0",
        font_size="16px",
        font_weight="bold",
        height="4rem",
        padding="0 1.6rem",
        text_align="center",
        text_shadow="rgba(0,0,0,0.25) 0 3px 8px",
        transition="all 0.5s",
        user_select="none",
        touch_action="manipulation",
        style={
            "_hover": {
                "box-shadow": "rgba(80, 63, 205, 0.5) 0 1px 30px",
                "transition-duration": ".1s",
            },
        },
    )