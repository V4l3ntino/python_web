import reflex as rx
from .model.user_model import User
from .service.user_service import select_all_user_service, select_user_by_email_service, create_user_service


class UserState(rx.State):
    
    users: list[User]
    user_buscar: str
    
    @rx.background
    async def get_all_user(self):
        async with self:
            self.users = select_all_user_service()
        
    @rx.background
    async def get_user_by_email(self):
        async with self:
            self.users = select_user_by_email_service(self.user_buscar) 
            
    @rx.background
    async def create_user(self, data: dict):
        async with self:
            try:
                self.users = create_user_service(username=data['username'], password=data['password'], phone=data['phone'], name=data['name'])
            except BaseException as be:
                print(be.args) 
            
    def buscar_on_change(self, value: str):
        self.user_buscar = value
    

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
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )
    

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
            rx.button('Eliminar')  
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
            #reset_on_submit=True,
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
    
