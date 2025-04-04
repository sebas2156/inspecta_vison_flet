import flet as ft
from api.registros_api import RegistroClient  # Asumiendo que tienes este cliente API


def create_registros_content(page: ft.Page):
    # Estado de la aplicación
    state = {
        'current_page': 1,
        'items_per_page': 10,
        'total_pages': 1,
        'search_term': '',
        'all_registros': [],
        'filtered_registros': []
    }

    # Inicializar cliente API
    registro_client = RegistroClient()

    # Estilos comunes
    header_style = ft.TextStyle(
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        size=14
    )

    row_style = ft.TextStyle(
        size=14,
        color=ft.colors.GREY_800
    )

    # Contenedor principal
    content_column = ft.Column()
    main_container = ft.Container(
        content=content_column,
        padding=ft.padding.all(20)
    )

    def show_loading():
        loading = ft.Column(
            controls=[
                ft.ProgressRing(),
                ft.Text("Cargando registros...")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        content_column.controls.clear()
        content_column.controls.append(loading)
        page.update()

    async def load_data():
        try:
            show_loading()
            response = await registro_client.obtener_registros(
                skip=0,
                limit=100  # Aumentamos el límite para obtener todos los registros
            )

            if response and 'data' in response:
                state['all_registros'] = response['data']
                state['total_pages'] = response.get('total_paginas', 1)
                filter_registros()
                update_ui()
            else:
                page.error("Error al obtener los registros")

        except Exception as e:
            page.error(f"Error de conexión: {str(e)}")
        finally:
            page.update()

    def filter_registros():
        search_lower = state['search_term'].lower()
        state['filtered_registros'] = [
            r for r in state['all_registros']
            if search_lower in r.get('producto', '').lower()
               or search_lower in str(r.get('accion', '')).lower()
               or search_lower in str(r.get('sector', '')).lower()
        ]
        state['total_pages'] = max(
            1,
            (len(state['filtered_registros']) + state['items_per_page'] - 1) // state['items_per_page']
        )

    def update_ui():
        content_column.controls.clear()

        if not state['filtered_registros']:
            content_column.controls.append(
                ft.Text("No se encontraron registros", color=ft.colors.RED)
            )
            page.update()
            return

        start = (state['current_page'] - 1) * state['items_per_page']
        end = start + state['items_per_page']
        current_registros = state['filtered_registros'][start:end]

        rows = []
        for idx, registro in enumerate(current_registros):
            is_even_row = idx % 2 == 0

            rows.append(ft.DataRow(
                color=ft.colors.GREY_50 if is_even_row else ft.colors.WHITE,
                cells=[
                    ft.DataCell(ft.Text(str(registro.get('id', '')), style=row_style)),
                    ft.DataCell(ft.Text(registro.get('producto', ''), style=row_style)),
                    ft.DataCell(ft.Text(registro.get('accion', ''), style=row_style)),
                    ft.DataCell(ft.Text(registro.get('fecha', ''), style=row_style)),
                    ft.DataCell(ft.Text(str(registro.get('sector', '')), style=row_style)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_600,
                                    tooltip="Editar registro",
                                    on_click=lambda e, r=registro: open_edit_modal(page, r)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_600,
                                    tooltip="Eliminar registro",
                                    on_click=lambda e, r=registro: page.run_task(eliminar_registro, r)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        )
                    )
                ]
            ))

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", style=header_style)),
                ft.DataColumn(ft.Text("PRODUCTO", style=header_style)),
                ft.DataColumn(ft.Text("ACCIÓN", style=header_style)),
                ft.DataColumn(ft.Text("FECHA", style=header_style)),
                ft.DataColumn(ft.Text("SECTOR", style=header_style)),
                ft.DataColumn(ft.Text("ACCIONES", style=header_style)),
            ],
            rows=rows,
            vertical_lines=ft.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(1, ft.colors.GREY_200),
            heading_row_color=ft.colors.BLUE_700,
            heading_row_height=45,
            column_spacing=30,
            divider_thickness=1,
        )

        pagination_controls = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CHEVRON_LEFT,
                            on_click=lambda e: go_to_page(state['current_page'] - 1),
                        ),
                        ft.Text(f"Página {state['current_page']} de {state['total_pages']}"),
                        ft.IconButton(
                            icon=ft.icons.CHEVRON_RIGHT,
                            on_click=lambda e: go_to_page(state['current_page'] + 1),
                        )
                    ]
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option("5"),
                                ft.dropdown.Option("10"),
                                ft.dropdown.Option("20"),
                                ft.dropdown.Option("50"),
                            ],
                            value=str(state['items_per_page']),
                            on_change=handle_items_per_page_change,
                            width=100,
                        ),
                        ft.Text("Items por página"),
                    ]
                ),
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        content_column.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Gestión de Registros",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE_700),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                label="Buscar por producto, acción o sector",
                                icon=ft.icons.SEARCH,
                                value=state['search_term'],
                                on_change=handle_search_change,
                                on_submit=trigger_search,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.icons.SEARCH,
                                on_click=trigger_search,
                            ),
                        ]
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        content=data_table,
                        padding=20,
                        expand=True
                    ),
                    pagination_controls
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        )
        page.update()

    def go_to_page(page_number):
        if 1 <= page_number <= state['total_pages']:
            state['current_page'] = page_number
            update_ui()

    def handle_items_per_page_change(e):
        new_value = int(e.control.value)
        state['items_per_page'] = new_value
        state['current_page'] = 1
        filter_registros()
        update_ui()

    def handle_search_change(e):
        state['search_term'] = e.control.value

    def trigger_search(e=None):
        state['current_page'] = 1
        filter_registros()
        update_ui()

    def open_edit_modal(page, registro):
        # Campos del formulario
        producto_field = ft.TextField(label="Producto", value=registro.get('producto', ''))
        accion_field = ft.TextField(label="Acción", value=registro.get('accion', ''))
        fecha_field = ft.TextField(label="Fecha", value=registro.get('fecha', ''))
        sector_field = ft.TextField(label="Sector", value=registro.get('sector', ''))

        # Diálogo modal
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Registro"),
            content=ft.Column(
                controls=[producto_field, accion_field, fecha_field, sector_field],
                tight=True,
                spacing=10
            ),
            actions=[
                ft.TextButton("Guardar", on_click=lambda e: handle_save(e)),
                ft.TextButton("Cancelar", on_click=lambda e: dialog.open == False)
            ]
        )

        def handle_save(e):
            updated_data = {
                'id': registro['id'],
                'producto': producto_field.value,
                'accion': accion_field.value,
                'fecha': fecha_field.value,
                'sector': sector_field.value
            }
            page.run_task(save_edicion, registro['id'], updated_data)
            dialog.open = False
            page.update()

        # Agregar diálogo al overlay y mostrarlo
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def save_edicion(registro_id, updated_data):
        try:
            response = await registro_client.actualizar_registro(registro_id, updated_data)
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al actualizar registro: {str(e)}")
    async def editar_registro(registro):
        try:
            # Ejemplo de actualización
            updated_data = {**registro, "accion": "Modificado"}
            response = await registro_client.actualizar_registro(
                registro["id"],
                updated_data
            )

            if response:
                await load_data()

        except Exception as e:
            page.error(f"Error al actualizar registro: {str(e)}")

    async def eliminar_registro(registro):
        try:
            response = await registro_client.eliminar_registro(registro["id"])

            if response:
                await load_data()

        except Exception as e:
            page.error(f"Error al eliminar registro: {str(e)}")

    # Iniciar carga de datos
    page.run_task(load_data)

    return main_container