import flet as ft

def create_sidemenu(page: ft.Page):
    # Estado del menú
    menu_abierto = True
    ancho_menu = 240
    ancho_cerrado = 0

    # Elementos del menú con sus rutas correspondientes
    items_menu = [
        {"icon": ft.icons.HOME, "text": "Inicio", "ruta": "/home"},
        {"icon": ft.icons.SHOPPING_BAG, "text": "Productos", "ruta": "/productos"},
        {"icon": ft.icons.ASSIGNMENT, "text": "Registros", "ruta": "/registros"},
        {"icon": ft.icons.PIE_CHART, "text": "Camaras", "ruta": "/camaras"},
        {"icon": ft.icons.SETTINGS, "text": "Configuración", "ruta": "/configuracion"},
    ]

    def toggle_menu(e):
        nonlocal menu_abierto, ancho_menu
        menu_abierto = not menu_abierto
        sidebar.width = ancho_menu if menu_abierto else ancho_cerrado
        texto_perfil.visible = menu_abierto
        avatar.visible = menu_abierto

        # Ocultar/mostrar texto en los ítems
        for container in columna_menu.controls[2:2 + len(items_menu)]:
            if hasattr(container, "content") and isinstance(container.content, ft.Row):
                row = container.content
                if len(row.controls) > 1:
                    row.controls[1].visible = menu_abierto

        page.update()

    # Barra lateral
    columna_menu = ft.Column(
        spacing=0,
        controls=[
            ft.Container(  # Header
                padding=50,
                height=180,
                content=ft.Column(
                    [
                        avatar := ft.CircleAvatar(
                            content=ft.Image(
                                src="https://picsum.photos/100",
                                fit=ft.ImageFit.COVER,
                            ),
                            radius=32,
                        ),
                        texto_perfil := ft.Text("John Doe", color=ft.colors.WHITE, size=14),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center,
            ),
            ft.Divider(height=1, color=ft.colors.WHITE24),
        ]
    )

    # Añadir items del menú con navegación
    for item in items_menu:
        columna_menu.controls.append(
            ft.Container(
                height=56,
                content=ft.Row(
                    [
                        ft.IconButton(
                            icon=item["icon"],
                            icon_size=24,
                            style=ft.ButtonStyle(color=ft.colors.WHITE),
                        ),
                        ft.Text(item["text"],
                                color=ft.colors.WHITE,
                                size=14,
                                visible=menu_abierto),
                    ],
                    spacing=12,
                ),
                on_click=lambda e, ruta=item["ruta"]: page.go(ruta),
                border_radius=12,
                padding=ft.padding.only(left=14),
            )
        )

    sidebar = ft.Container(
        width=ancho_menu,
        content=columna_menu,
        bgcolor=ft.colors.BLUE_900,
        animate=ft.animation.Animation(300, "easeOut"),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Botón de menú flotante (siempre visible)
    menu_button = ft.IconButton(
        icon=ft.icons.MENU,
        icon_size=24,
        on_click=toggle_menu,
        style=ft.ButtonStyle(color=ft.colors.WHITE),
        top=10,
        left=10,
    )

    return sidebar, menu_button