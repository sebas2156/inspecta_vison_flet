import flet as ft
from api.cuentas_api import CuentaClient


def create_cuentas_content(page: ft.Page):
    state = {
        'current_page': 1,
        'items_per_page': 10,
        'total_pages': 1,
        'search_term': '',
        'all_cuentas': [],
        'filtered_cuentas': []
    }

    cuenta_client = CuentaClient()

    # Estilos
    header_style = ft.TextStyle(
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        size=14
    )

    row_style = ft.TextStyle(
        size=14,
        color=ft.colors.GREY_800
    )

    content_column = ft.Column()
    main_container = ft.Container(
        content=content_column,
        padding=ft.padding.all(20)
    )
    def show_loading():
        content_column.controls.clear()
        content_column.controls.append(
            ft.Column(
                [ft.ProgressRing(), ft.Text("Cargando...")],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    async def load_data():
        try:
            show_loading()
            response = await cuenta_client.obtener_cuentas(skip=0, limit=100)

            if response and 'data' in response:
                state['all_cuentas'] = response['data']
                filter_cuentas()
                update_ui()
        except Exception as e:
            page.error(f"Error: {str(e)}")
        finally:
            page.update()

    def filter_cuentas():
        search_lower = state['search_term'].lower()
        state['filtered_cuentas'] = [
            c for c in state['all_cuentas']
            if search_lower in c.get('nombre', '').lower()
               or search_lower in c.get('correo', '').lower()
               or search_lower in c.get('empresa', '').lower()
        ]
        state['total_pages'] = max(
            1,
            (len(state['filtered_cuentas']) + state['items_per_page'] - 1) // state['items_per_page']
        )

    def update_ui():
        content_column.controls.clear()

        if not state['filtered_cuentas']:
            content_column.controls.append(ft.Text("No se encontraron cuentas"))
            page.update()
            return

        # Generar filas de la tabla
        start = (state['current_page'] - 1) * state['items_per_page']
        end = start + state['items_per_page']
        current_cuentas = state['filtered_cuentas'][start:end]

        rows = []
        for cuenta in current_cuentas:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cuenta.get('id', '')))),
                        ft.DataCell(ft.Text(cuenta.get('nombre', ''))),
                        ft.DataCell(ft.Text(cuenta.get('correo', ''))),
                        ft.DataCell(ft.Text(str(cuenta.get('telefono', '')))),
                        ft.DataCell(ft.Text(cuenta.get('nivel', ''))),
                        ft.DataCell(ft.Text(cuenta.get('empresa', ''))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_600,
                                    on_click=lambda e, c=cuenta: open_edit_modal(page, c)
                                ),
                                ft.IconButton(
                                    ft.icons.DELETE,
                                    icon_color=ft.colors.RED_600,
                                    on_click=lambda e, c=cuenta: page.run_task(eliminar_cuenta, c)
                                )
                            ])
                        )
                    ]
                )
            )

        # Construir tabla
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", style=header_style)),
                ft.DataColumn(ft.Text("Nombre", style=header_style)),
                ft.DataColumn(ft.Text("Correo", style=header_style)),
                ft.DataColumn(ft.Text("Teléfono", style=header_style)),
                ft.DataColumn(ft.Text("Nivel", style=header_style)),
                ft.DataColumn(ft.Text("Empresa", style=header_style)),
                ft.DataColumn(ft.Text("Acciones", style=header_style)),
            ],
            rows=rows,
        )

        # Controles de paginación
        pagination = ft.Row([
            ft.IconButton(ft.icons.CHEVRON_LEFT, on_click=lambda e: change_page(-1)),
            ft.Text(f"Página {state['current_page']} de {state['total_pages']}"),
            ft.IconButton(ft.icons.CHEVRON_RIGHT, on_click=lambda e: change_page(1)),
        ])

        content_column.controls.extend([
            ft.TextField(
                label="Buscar...",
                on_change=handle_search_change,
                value=state['search_term']
            ),
            ft.Divider(),
            data_table,
            pagination
        ])
        page.update()

    def open_edit_modal(page, cuenta):
        # Campos del formulario
        nombre_field = ft.TextField(label="Nombre", value=cuenta.get('nombre', ''))
        correo_field = ft.TextField(label="Correo", value=cuenta.get('correo', ''))
        telefono_field = ft.TextField(label="Teléfono", value=str(cuenta.get('telefono', '')))
        nivel_field = ft.Dropdown(
            label="Nivel",
            options=[
                ft.dropdown.Option("admin"),
                ft.dropdown.Option("usuario"),
                ft.dropdown.Option("invitado")
            ],
            value=cuenta.get('nivel', 'usuario')
        )
        empresa_field = ft.TextField(label="Empresa", value=cuenta.get('empresa', ''))
        contraseña_field = ft.TextField(label="Contraseña", value=cuenta.get('contraseña', ''), password=True)

        # Diálogo modal
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Cuenta"),
            content=ft.Column(
                controls=[
                    nombre_field,
                    correo_field,
                    telefono_field,
                    nivel_field,
                    empresa_field,
                    contraseña_field  # Campo de contraseña añadido
                ],
                tight=True,
                spacing=10
            ),
            actions=[
                ft.TextButton("Guardar", on_click=lambda e: handle_save(e)),
                ft.TextButton("Cancelar", on_click=lambda e: dialog.open == False)
            ]
        )

        def handle_save(e):
            if not contraseña_field.value:
                page.error("La contraseña es obligatoria")
                return

            updated_data = {
                'id': cuenta['id'],
                'nombre': nombre_field.value,
                'correo': correo_field.value,
                'telefono': int(telefono_field.value),
                'nivel': nivel_field.value,
                'empresa': empresa_field.value,
                'contraseña': contraseña_field.value
            }
            page.run_task(save_edicion, cuenta['id'], updated_data)
            dialog.open = False
            page.update()

    async def save_edicion(cuenta_id, updated_data):
        try:
            response = await cuenta_client.actualizar_cuenta(cuenta_id, updated_data)
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al actualizar: {str(e)}")

    async def eliminar_cuenta(cuenta):
        try:
            response = await cuenta_client.eliminar_cuenta(cuenta['id'])
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al eliminar: {str(e)}")

    def change_page(delta):
        new_page = state['current_page'] + delta
        if 1 <= new_page <= state['total_pages']:
            state['current_page'] = new_page
            update_ui()

    def handle_search_change(e):
        state['search_term'] = e.control.value
        filter_cuentas()
        update_ui()

    page.run_task(load_data)
    return main_container