import flet as ft

def create_sidemenu(page: ft.Page):
    # Estado persistente en la página
    if not hasattr(page, "menu_abierto"):
        page.menu_abierto = True

    ancho_menu = 240
    ancho_cerrado = 0

    # Elementos del menú con sus rutas correspondientes
    items_menu = [
        {"icon": ft.icons.HOME, "text": "Inicio", "ruta": "/home"},
        {"icon": ft.icons.SHOPPING_BAG, "text": "Productos", "ruta": "/productos"},
        {"icon": ft.icons.SHOPPING_BAG, "text": "Sectores", "ruta": "/sectores"},
        {"icon": ft.icons.ASSIGNMENT, "text": "Registros", "ruta": "/registros"},
        {"icon": ft.icons.PIE_CHART, "text": "Camaras", "ruta": "/camaras"},
        {"icon": ft.icons.SETTINGS, "text": "Cuentas", "ruta": "/cuentas"},
    ]

    def toggle_menu(e):
        page.menu_abierto = not page.menu_abierto
        update_menu_visibility()
        page.update()

    def update_menu_visibility():
        sidebar.width = ancho_menu if page.menu_abierto else ancho_cerrado
        texto_perfil.visible = page.menu_abierto
        avatar.visible = page.menu_abierto
        for container in columna_menu.controls[2:]:
            if hasattr(container, "content"):
                row = container.content
                if len(row.controls) > 1:
                    row.controls[1].visible = page.menu_abierto

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
                                visible=page.menu_abierto),
                    ],
                    spacing=12,
                ),
                on_click=lambda e, ruta=item["ruta"]: page.go(ruta),
                border_radius=12,
                padding=ft.padding.only(left=14),
            )
        )

    sidebar = ft.Container(
        width=ancho_menu if page.menu_abierto else ancho_cerrado,
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

    # Llamar a la actualización inicial
    update_menu_visibility()

    return sidebar, menu_button