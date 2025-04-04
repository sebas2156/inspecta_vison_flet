import flet as ft
from api.sectores_api import SectorClient  # Asumiendo que tienes este cliente API

def create_sectores_content(page: ft.Page):
    # Estado de la aplicación
    state = {
        'current_page': 1,
        'items_per_page': 10,
        'total_pages': 1,
        'search_term': '',
        'all_sectores': [],
        'filtered_sectores': []
    }

    # Inicializar cliente API
    sector_client = SectorClient()

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
                ft.Text("Cargando sectores...")
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
            response = await sector_client.obtener_sectores(
                skip=0,
                limit=100  # Obtener todos los sectores
            )

            if response and 'data' in response:
                state['all_sectores'] = response['data']
                state['total_pages'] = response.get('total_paginas', 1)
                filter_sectores()
                update_ui()
            else:
                page.error("Error al obtener los sectores")

        except Exception as e:
            page.error(f"Error de conexión: {str(e)}")
        finally:
            page.update()

    def filter_sectores():
        search_lower = state['search_term'].lower()
        state['filtered_sectores'] = [
            s for s in state['all_sectores']
            if search_lower in s.get('producto', '').lower()
        ]
        state['total_pages'] = max(
            1,
            (len(state['filtered_sectores']) + state['items_per_page'] - 1) // state['items_per_page']
        )

    def update_ui():
        content_column.controls.clear()

        if not state['filtered_sectores']:
            content_column.controls.append(
                ft.Text("No se encontraron sectores", color=ft.colors.RED)
            )
            page.update()
            return

        start = (state['current_page'] - 1) * state['items_per_page']
        end = start + state['items_per_page']
        current_sectores = state['filtered_sectores'][start:end]

        rows = []
        for idx, sector in enumerate(current_sectores):
            is_even_row = idx % 2 == 0

            rows.append(ft.DataRow(
                color=ft.colors.GREY_50 if is_even_row else ft.colors.WHITE,
                cells=[
                    ft.DataCell(ft.Text(str(sector.get('id', '')), style=row_style)),
                    ft.DataCell(ft.Text(sector.get('producto', ''), style=row_style)),
                    ft.DataCell(ft.Text(str(sector.get('unidades', '')), style=row_style)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_600,
                                    tooltip="Editar sector",
                                    on_click=lambda e, s=sector: open_edit_modal(page, s)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_600,
                                    tooltip="Eliminar sector",
                                    on_click=lambda e, s=sector: page.run_task(eliminar_sector, s)
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
                ft.DataColumn(ft.Text("UNIDADES", style=header_style)),
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
                    ft.Text("Gestión de Sectores",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE_700),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                label="Buscar por producto",
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
        filter_sectores()
        update_ui()

    def handle_search_change(e):
        state['search_term'] = e.control.value

    def trigger_search(e=None):
        state['current_page'] = 1
        filter_sectores()
        update_ui()

    def open_edit_modal(page, sector):
        # Campos del formulario
        producto_field = ft.TextField(label="Producto", value=sector.get('producto', ''))
        unidades_field = ft.TextField(label="Unidades", value=str(sector.get('unidades', '')))

        # Diálogo modal
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Sector"),
            content=ft.Column(
                controls=[producto_field, unidades_field],
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
                'id': sector['id'],
                'producto': producto_field.value,
                'unidades': int(unidades_field.value)
            }
            page.run_task(save_edicion, sector['id'], updated_data)
            dialog.open = False
            page.update()

        # Agregar diálogo al overlay y mostrarlo
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def save_edicion(sector_id, updated_data):
        try:
            response = await sector_client.actualizar_sector(sector_id, updated_data)
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al actualizar sector: {str(e)}")

    async def eliminar_sector(sector):
        try:
            response = await sector_client.eliminar_sector(sector['id'])
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al eliminar sector: {str(e)}")

    # Iniciar carga de datos
    page.run_task(load_data)

    return main_container