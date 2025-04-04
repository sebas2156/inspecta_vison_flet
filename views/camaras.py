import flet as ft

def create_camaras_content(page: ft.Page):
    # Crear 5 contenedores estilo cámara
    containers = []
    for i in range(1, 6):
        containers.append(
            ft.Container(
                content=ft.Text(f"Cámara {i}", color=ft.colors.WHITE, size=20),
                height=150,
                bgcolor=ft.colors.BLUE_800,
                border_radius=10,
                alignment=ft.alignment.center,
                border=ft.border.all(2, ft.colors.BLUE_900),
                ink=True,
                on_click=lambda e, idx=i: page.go(f"/camara/{idx}")
            )
        )

    # Contenido principal
    return ft.Column(
        controls=containers,
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )