import flet as ft
from api.productos_api import ProductoClient

def create_productos_content(page: ft.Page):
    state = {
        'current_page': 1,
        'items_per_page': 10,
        'total_pages': 1,
        'search_term': '',
        'all_products': [],
        'filtered_products': []
    }

    producto_client = ProductoClient()

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

    # Controles
    content_column = ft.Column()
    main_container = ft.Container(
        content=content_column,
        padding=20,
        expand=True
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

    def filter_products():
        search_lower = state['search_term'].lower()
        state['filtered_products'] = [
            p for p in state['all_products']
            if search_lower in p.get('nombre_producto', '').lower()
               or search_lower in p.get('codigo', '').lower()
        ]
        state['total_pages'] = max(
            1,
            (len(state['filtered_products']) + state['items_per_page'] - 1) // state['items_per_page']
        )

    def update_ui():
        content_column.controls.clear()

        if not state['filtered_products']:
            content_column.controls.append(ft.Text("No se encontraron productos"))
            page.update()
            return

        # Generar filas de la tabla
        start = (state['current_page'] - 1) * state['items_per_page']
        end = start + state['items_per_page']
        current_products = state['filtered_products'][start:end]

        rows = []
        for producto in current_products:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto['codigo'])),
                        ft.DataCell(ft.Text(producto['nombre_producto'])),
                        ft.DataCell(ft.Text(str(producto['stock']))),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_600,
                                    tooltip="Editar producto",
                                    on_click=lambda e, p=producto: open_edit_modal(page, p)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_600,
                                    tooltip="Eliminar producto",
                                    on_click=lambda e, p=producto: page.run_task(eliminar_producto, p)
                                )
                            ])
                        )
                    ]
                )
            )

        # Construir tabla
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código", style=header_style)),
                ft.DataColumn(ft.Text("Nombre", style=header_style)),
                ft.DataColumn(ft.Text("Stock", style=header_style)),
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
            ft.TextField(label="Buscar...", on_change=update_search),
            ft.Divider(),
            data_table,
            pagination
        ])
        page.update()

    async def load_data():
        try:
            show_loading()
            response = await producto_client.obtener_productos()
            if response and 'data' in response:
                state['all_products'] = response['data']
                filter_products()
                update_ui()
        except Exception as e:
            page.error(f"Error: {str(e)}")
        finally:
            page.update()

    def change_page(delta):
        new_page = state['current_page'] + delta
        if 1 <= new_page <= state['total_pages']:
            state['current_page'] = new_page
            update_ui()

    def update_search(e):
        state['search_term'] = e.control.value
        filter_products()
        update_ui()

    def open_edit_modal(page, producto):
        # Campos del formulario
        nombre_field = ft.TextField(label="Nombre", value=producto.get('nombre_producto', ''))
        codigo_field = ft.TextField(label="Código", value=producto.get('codigo', ''))
        stock_field = ft.TextField(label="Stock", value=str(producto.get('stock', '')))
        descripcion_field = ft.TextField(label="Descripción", value=producto.get('descripcion', ''))
        categoria_field = ft.TextField(label="Categoría", value=producto.get('categoria', ''))
        sector_field = ft.TextField(label="Sector", value=producto.get('sector', ''))
        minimo_field = ft.TextField(label="Mínimo", value=str(producto.get('minimo', '')))

        # Diálogo modal
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Producto"),
            content=ft.Column(
                controls=[
                    nombre_field,
                    codigo_field,
                    stock_field,
                    descripcion_field,
                    categoria_field,
                    sector_field,
                    minimo_field
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
            updated_data = {
                'codigo': codigo_field.value,
                'nombre_producto': nombre_field.value,
                'stock': int(stock_field.value),
                'descripcion': descripcion_field.value,
                'categoria': categoria_field.value,
                'sector': sector_field.value,
                'minimo': int(minimo_field.value)
            }
            page.run_task(save_edicion, producto['codigo'], updated_data)
            dialog.open = False
            page.update()

        # Agregar diálogo al overlay y mostrarlo
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    async def save_edicion(producto_codigo, updated_data):
        try:
            response = await producto_client.actualizar_producto(producto_codigo, updated_data)
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al actualizar producto: {str(e)}")

    async def eliminar_producto(producto):
        try:
            response = await producto_client.eliminar_producto(producto['codigo'])
            if response:
                await load_data()
        except Exception as e:
            page.error(f"Error al eliminar producto: {str(e)}")

    # Iniciar carga de datos
    page.run_task(load_data)

    return main_container