import reflex as rx
from .model.user_model import User
from .service.user_service import select_all_user_service, select_user_by_email_service, create_user_service, delete_user_service
from .notify import notify_component
import asyncio

class UserState(rx.State):
    
    users: list[User]
    user_buscar: str
    error: str = ''
    
    @rx.background
    async def get_all_user(self):
        async with self:
            self.users = select_all_user_service()
        
    @rx.background
    async def get_user_by_email(self):
        async with self:
            self.users = select_user_by_email_service(self.user_buscar) 
    
    async def handleNotify(self):
        async with self:
            await asyncio.sleep(2)
            self.error = ''
         
    @rx.background
    async def create_user(self, data: dict):
        async with self:
            try:
                self.users = create_user_service(username=data['username'], password=data['password'], phone=data['phone'], name=data['name'])
            except BaseException as be:
                print(be.args) 
                self.error = be.args
        await self.handleNotify()
            
    def buscar_on_change(self, value: str):
        self.user_buscar = value
        
    @rx.background
    async def delete_user_by_email(self, email):
        async with self:
            self.users = delete_user_service(email)
    

@rx.page(route='/user', title='user', on_load=UserState.get_all_user)
def user_page() -> rx.Component:
    return rx.flex(
        rx.heading('Usuarios', align="center"),
        rx.hstack(
            buscar_user_component(),
            create_user_dialog_component(),
            justify="center",
            style={'margin_top': '30px'}
        ),
        table_user(UserState.users),
        rx.cond(
            UserState.error != '',
            notify_component(UserState.error, 'shield-alert', 'yellow')
        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

@rx.page(route='/login', title='Login')
def user_login() -> rx.Component:
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

    

def table_user(list_user: list[User]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell('Nombre'),
                rx.table.column_header_cell('Email'),
                rx.table.column_header_cell('Telefono'),
                rx.table.column_header_cell('Accion')
            )
        ),
        rx.table.body(
            rx.foreach(list_user, row_table)
        )
    )
    

def row_table(user: User) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.username),
        rx.table.cell(user.phone),
        rx.table.cell(rx.hstack(
            delete_user_dialog_component(user.username)  
        ))
    )
    
    
def buscar_user_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese Email", on_change=UserState.buscar_on_change),
        rx.button('Buscar usuario', on_click=UserState.get_user_by_email)
    )





def create_user_form() -> rx.Component:
    return rx.form(
            rx.vstack(  
                rx.input(
                    placeholder="First Name",
                    name="name",
                ),
                rx.input(
                    placeholder="Username",
                    name="username",
                ),
                rx.input(
                    placeholder="Password",
                    name="password",
                    type="password"
                ),
                rx.input(
                    placeholder="Phone",
                    name="phone",
                ),
                rx.dialog.close(
                    rx.button("Submit", type="submit"),
                )
            ),
            on_submit=UserState.create_user,
        )
    
    
def create_user_dialog_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Crear usuario')),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title('Crear Usuario'),
                create_user_form(),
                justify='center',
                align='center',
                direction='column',
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button('Cancelar', color_scheme='gray', variant='soft')
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={'width': '300px'}
        )
    )
    

def delete_user_dialog_component(username: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon('trash-2'))),
        rx.dialog.content(
            rx.dialog.title('Eliminar usuario'),
            rx.dialog.description('Estás seguro de querer eliminar al usuario '+username),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme='gray',
                        variant='soft'
                    )
                ),
                rx.dialog.close(
                    rx.button('Confirmar', on_click=UserState.delete_user_by_email(username))
                ),
                spacing="3",
                margin_top="16px",
                justify="end"
            )
        )
    )