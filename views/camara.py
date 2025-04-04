import flet as ft

# Lista de direcciones IP de ejemplo
CAMERAS_IPS = [
    "192.168.0.3:8080",
    "192.168.1.101",
    "192.168.1.102",
    "192.168.1.103",
    "192.168.1.104"
]

def create_camara_content(page: ft.Page):
    # Obtener el índice de la cámara actual desde la ruta
    route_parts = page.route.split("/")
    current_camera_index = int(route_parts[-1]) if len(route_parts) > 2 else 0

    def cambiar_camara(e, offset):
        nonlocal current_camera_index
        new_index = (current_camera_index + offset) % len(CAMERAS_IPS)
        page.go(f"/camara/{new_index}")

    # Contenedor principal del video (simulación)
    video_container = ft.Image(
        src=f"http://{CAMERAS_IPS[current_camera_index]}/video_feed",
        fit=ft.ImageFit.CONTAIN,
        height=400,
        border_radius=15
    )

    # Controles de navegación
    controls = ft.Row(
        controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_size=30,
                    on_click=lambda e: cambiar_camara(e, -1)),
                ft.IconButton(
                    icon=ft.icons.ARROW_FORWARD,
                    icon_size=30,
                    on_click=lambda e: cambiar_camara(e, 1))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Panel de información
    info_panel = ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(controls=[
                    ft.Text("Información de la Cámara",
                            size=18,
                            weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Row(controls=[
                        ft.Text("IP:", weight=ft.FontWeight.BOLD),
                        ft.Text(CAMERAS_IPS[current_camera_index])
                    ], spacing=20)]
            )
        )
    )

    return ft.Column(
        controls=[
            video_container,
            ft.Divider(height=20),
            controls,
            ft.Divider(height=20),
            info_panel
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )