import flet as ft
from views.home import create_home_content  # Importamos la función del contenido
from views.camaras import create_camaras_content
from sidemenu import create_sidemenu  # Importamos el menú lateral
from views.camara import create_camara_content
from views.productos import create_productos_content
from views.registros import create_registros_content
from views.cuentas import create_cuentas_content
from views.inventario import create_sectores_content
def create_login_view(page):
    # Estilos reutilizables
    title_style = ft.TextStyle(
        size=28,
        weight=ft.FontWeight.BOLD,
        font_family="Poppins",
        color=ft.Colors.WHITE
    )

    input_style = {
        "border_color": ft.Colors.WHITE54,
        "cursor_color": ft.Colors.WHITE,
        "color": ft.Colors.WHITE,
        "border_radius": 12,
        "bgcolor": ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        "border_width": 1.5,
        "height": 50,
        "text_size": 14,
        "label_style": ft.TextStyle(color=ft.Colors.WHITE54, font_family="Poppins"),
        "prefix_style": ft.TextStyle(color=ft.Colors.WHITE54)
    }

    def login_clicked(e):
        if username.value == "" and password.value == "":
            error_text.visible = False
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ ¡Bienvenido de nuevo!", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
                behavior=ft.SnackBarBehavior.FLOATING
            )
            page.snack_bar.open = True
            page.go("/app")  # Navegación a la vista principal
        else:
            error_text.visible = True
            error_text.value = "⚠️ Usuario o contraseña incorrectos"
            error_text.color = ft.Colors.RED_ACCENT
        page.update()

    # Componentes UI
    title = ft.Text("Iniciar Sesión", style=title_style)
    subtitle = ft.Text("Accede a tu cuenta para continuar", color=ft.Colors.WHITE54, font_family="Poppins")

    username = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        **input_style,
        width=320
    )

    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        **input_style,
        width=320
    )

    login_button = ft.ElevatedButton(
        "Iniciar Sesión",
        width=320,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_ACCENT_700,
            shape={"": ft.RoundedRectangleBorder(radius=12)},
            overlay_color=ft.Colors.BLUE_ACCENT_100,
            padding={"": 15},
            elevation={"": 8}
        ),
        on_click=login_clicked
    )

    error_text = ft.Text(
        "⚠️ Usuario o contraseña incorrectos",
        color=ft.Colors.RED_ACCENT,
        visible=False,
        weight=ft.FontWeight.W_500,
        font_family="Poppins"
    )

    signup_row = ft.Row(
        [
            ft.Text("¿No tienes cuenta?", color=ft.Colors.WHITE54, font_family="Poppins"),
            ft.TextButton(
                "Regístrate aquí",
                style=ft.ButtonStyle(color=ft.Colors.BLUE_ACCENT),
                on_click=lambda e: print("Redirigir a registro")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    )

    # Contenedor principal del formulario
    login_container = ft.Container(
        ft.Column(
            [
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.BLUE_ACCENT),
                title,
                subtitle,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                username,
                password,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                login_button,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                error_text,
                signup_row
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=40,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_radius=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.with_opacity(0.2, ft.Colors.BLUE_900), ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900)]
        ),
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
        shadow=ft.BoxShadow(blur_radius=50, color=ft.Colors.BLUE_900),
        width=400,
        height=500
    )

    # Devolver la vista de login
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                gradient=ft.LinearGradient(
                    colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_800],
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center
                ),
                expand=True,  # Ocupar toda la pantalla
                content=ft.Stack(
                    [
                        ft.Container(
                            content=login_container,
                            alignment=ft.alignment.center,
                            expand=True  # Expandir para centrar correctamente
                        )
                    ],
                    expand=True
                )
            )
        ],
        padding=0,  # Eliminar padding de la vista
        spacing=0
    )

def main(page: ft.Page):
    page.title = "Login Moderno"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap"
    }

    # Crear el layout principal UNA VEZ
    sidebar, menu_button = create_sidemenu(page)
    content_container = ft.Container(expand=True)  # Contenedor dinámico

    # Layout principal (fuera de las vistas)
    main_layout = ft.Stack(
        [
            ft.Row(
                [
                    sidebar,
                    content_container
                ],
                expand=True
            ),
            menu_button
        ],
        expand=True
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_login_view(page))
        else:
            # Solo actualizamos el contenido dinámico
            if page.route == "/home":
                content_container.content = create_home_content(page)
            elif page.route == "/productos":
                content_container.content = create_productos_content(page)
            elif page.route == "/registros":
                content_container.content = create_registros_content(page)
            elif page.route == "/camaras":
                content_container.content = create_camaras_content(page)
            elif page.route == "/cuentas":
                content_container.content = create_cuentas_content(page)
            elif page.route == "/sectores":
                content_container.content = create_sectores_content(page)
            elif page.route.startswith("/camara"):
                content_container.content = create_camara_content(page)
            page.views.append(
                ft.View(
                    route="/app",
                    controls=[main_layout],
                    padding=0,
                    bgcolor=ft.Colors.GREY_100
                )
            )
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = lambda _: page.go("/")
    page.go(page.route)

ft.app(target=main)