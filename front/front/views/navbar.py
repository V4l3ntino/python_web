import reflex as rx
from front.styles.styles import Size, Color

def navbar() -> rx.Component:
    return rx.vstack(
            rx.hstack(
            rx.image(
                src="assets\\\\avatar.jpg",
                alt = "",
                width = Size.BIG.value,
                height = Size.VERY_BIG.value
            ),
            rx.text("addViento 2023"),
            rx.spacer(),
            width="100%"
        ),
        bg = Color.PRIMARY.value,
        position = "sticky",
        border_bottom = "1px dashed var(--gray-a7)",
        padding_x = Size.BIG.value,
        padding_y = Size.DEFAULT.value,
        z_index = "999",
        top = "0",
        width="100%",
    )

