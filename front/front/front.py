import reflex as rx
import front.styles.styles as styles
from front.views.navbar import navbar

def index() -> rx.Component:
    return rx.box(
        navbar()
    )

app = rx.App(
   stylesheets=styles.STYLESHEETS,
   style=styles.BASE_STYLE
)

app.add_page(
    index,
    title="Calendario de adViento 2023 | 24 días. 24 regalos",
    description="Por tercer año, ¡aquí está el calendario de adviento sorpresa de nuestra comunidad"
)

app.compile()