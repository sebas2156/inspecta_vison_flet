import flet as ft
from sidemenu import create_sidemenu


def create_camaras_view(page: ft.Page):
    # Crear el menú lateral
    sidebar, menu_button = create_sidemenu(page)

    # Controles para configuración
    cantidad_containers = ft.TextField(label="Número de cámaras", value="10", width=200)
    spacing_slider = ft.Slider(min=0, max=50, value=10, label="Espaciado horizontal")
    run_spacing_slider = ft.Slider(min=0, max=50, value=10, label="Espaciado vertical")
    alignment_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("start"),
            ft.dropdown.Option("center"),
            ft.dropdown.Option("end"),
            ft.dropdown.Option("spaceBetween"),
            ft.dropdown.Option("spaceAround"),
            ft.dropdown.Option("spaceEvenly"),
        ],
        value="start",
        label="Alineación",
        width=200
    )

    def generar_containers(e):
        try:
            num = int(cantidad_containers.value)
        except:
            num = 0
            ft.Container(
                width=100,
                height=100,
                bgcolor=ft.colors.BLUE_300,
                border_radius=5,
                content=ft.Text(str(1),
                                size=20,
                                color=ft.colors.WHITE,
                                weight="bold"),
                alignment=ft.alignment.center
            )




    # Configurar eventos
    generar_btn = ft.ElevatedButton("Generar cámaras", on_click=generar_containers)

    # Contenido principal
    content = ft.Column(
        controls=[
            ft.Row([
                cantidad_containers,
                generar_btn
            ], alignment="center"),

            ft.Row([
                ft.Column([
                    spacing_slider,
                    run_spacing_slider
                ], width=300),
                alignment_dropdown
            ], alignment="center"),

            ft.Container(
                padding=20,
                border=ft.border.all(2, ft.colors.GREY_400),
                border_radius=10,
                expand=True
            )
        ],
        spacing=20,
        expand=True
    )

    # Layout principal
    view_content = ft.Stack(
        [
            ft.Row(
                [
                    sidebar,
                    ft.VerticalDivider(width=1, color=ft.colors.GREY_300),
                    ft.Container(content, expand=True)
                ],
                expand=True
            ),
            menu_button
        ],
        expand=True
    )

    # Generar contenedores iniciales
    generar_containers(None)

    return ft.View(
        route="/camaras",
        controls=[view_content],
        padding=0,
        bgcolor=ft.colors.GREY_100
    )
