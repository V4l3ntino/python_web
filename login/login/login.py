import reflex as rx

class State(rx.State):
    """The app state."""


#RETURN CUSTOM TEXT INPUT FIELD
# def get_input_field(icon:str, placeholder: str, _type: str):
#     return rx.container(
#         rx.hstack(
#             tag=icon,
#             color="white",
#             fontSize="11px",
#         ),
#         rx.input(
#             placeholder=placeholder,
#             border="0px",
#             focus_border_color=""
#         )
#     )


def index() -> rx.Component:
    login_container = rx.container(
        rx.vstack(
            rx.container(
                rx.text(
                    "Iniciar Sesión",
                    fontSize="28px",
                    color='white',
                    fontWeight="bold",
                    letterSpacing="2",
                    text_align="center",
                ),
                #text settings
                width='250px',
                margin="auto",
            ),
            rx.container(
                rx.text(
                    "Debes tener una cuenta previamente",
                    fontSize="12px",
                    color='white',
                    fontWeight="#eeeeee",
                    letterSpacing="0.25px",
                    text_align="center"
                ),
                #text settings
                width='250px',
                margin="auto",
            ),
            rx.form(
                rx.vstack(  
                    rx.input(
                        placeholder="Email",
                        name="name",
                    ),
                    rx.input(
                        placeholder="Password",
                        name="password",
                        type="password"
                    ),
                    rx.button(
                        "Submit", 
                        type="submit",
                        bg="black",
                        width="100%",
                         _hover={
                             "color": "black",
                                 "background":"white"
                                 },   
                    ),
                ),
                #on_submit=UserState.create_user,
                #reset_on_submit=True,
                margin="auto"
            ),
            padding_top="2em",

        ),
        width="400px",
        height="300px",
        bg="#1D2330",
        boxShadow="41px -41px 82px #0d0f15, -41px 41px 82px #2d374b",
        margin="auto",
        borderRadius="15px",

    )
    
    _main = rx.container(
        login_container,
        maxWidth="auto",
        height="100vh",
        bg="#1D2330",
        #padding="10em",
        justify_content="center",
    )

    return _main
    


app = rx.App()
app.add_page(index)
