import flet as ft
from dataclasses import dataclass


@dataclass
class Producto:
    sku: str
    nombre: str
    categoria: str
    ubicacion: str
    stock_minimo: int
    stock_ideal: int
    stock_actual: list[int]
    historico: list[int]


productos = [
    Producto("LT-001", "Laptop Gamer", "Tecnología", "A1-B2", 10, 50,
             [45, 40, 38, 35, 32, 30, 28, 25, 22, 20, 18, 15],
             [120, 115, 110, 105, 100, 95, 90, 85, 80, 75, 70, 65]),

    Producto("SH-002", "Silla Ergonómica", "Mobiliario", "C3-D4", 5, 30,
             [28, 25, 22, 20, 18, 15, 12, 10, 8, 5, 3, 1],
             [50, 48, 45, 43, 40, 38, 35, 33, 30, 28, 25, 22]),

    Producto("TL-003", "Taladro Profesional", "Herramientas", "E5-F6", 15, 40,
             [38, 35, 33, 30, 28, 25, 23, 20, 18, 15, 12, 10],
             [80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25])
]

meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']


def create_home_content(page: ft.Page):
    # Controles de filtrado
    dropdown_categorias = ft.Dropdown(
        options=[ft.dropdown.Option("Todas")] +
                [ft.dropdown.Option(cat) for cat in {"Tecnología", "Mobiliario", "Herramientas"}],
        label="Filtrar por categoría",
        width=300,
        value="Todas"
    )

    search_field = ft.TextField(
        label="Buscar producto",
        icon=ft.icons.SEARCH,
        width=300
    )

    # Gráfico principal
    line_chart = ft.LineChart(
        border=ft.Border(bottom=ft.BorderSide(1, ft.colors.GREY)),
        left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Unidades")),
        bottom_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(i, label=ft.Text(mes)) for i, mes in enumerate(meses)],
            labels_size=20,
            title=ft.Text("Meses")
        ),
        expand=True,
        tooltip_bgcolor=ft.colors.WHITE,
        interactive=True,
    )

    # Tabla de datos
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("SKU")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Ubicación")),
            ft.DataColumn(ft.Text("Stock Actual")),
            ft.DataColumn(ft.Text("Mínimo")),
            ft.DataColumn(ft.Text("Estado"))
        ],
        vertical_lines=ft.BorderSide(1, ft.colors.GREY),
        horizontal_lines=ft.BorderSide(1, ft.colors.GREY_300),
    )

    # Alertas y estadísticas
    alertas_container = ft.Column([])
    stats_cards = ft.Row(spacing=20)

    def update_ui(e=None):
        productos_filtrados = [
            p for p in productos
            if (dropdown_categorias.value == "Todas" or p.categoria == dropdown_categorias.value) and
               search_field.value.lower() in p.nombre.lower()
        ]

        # Actualizar gráfico
        line_chart.data_series = []
        for idx, p in enumerate(productos_filtrados):
            line_chart.data_series.append(
                ft.LineChartData(
                    data_points=[ft.LineChartDataPoint(i, val) for i, val in enumerate(p.stock_actual)],
                    color=ft.colors.CYAN if idx % 2 == 0 else ft.colors.AMBER,
                    stroke_width=3,
                    curved=True
                )
            )

        # Actualizar tabla
        data_table.rows = []
        for p in productos_filtrados:
            ultimo_stock = p.stock_actual[-1]
            estado = ft.Text(
                "ALERTA" if ultimo_stock < p.stock_minimo else
                "BAJO" if ultimo_stock < p.stock_ideal else "OK",
                color=ft.colors.RED if ultimo_stock < p.stock_minimo else
                ft.colors.ORANGE if ultimo_stock < p.stock_ideal else ft.colors.GREEN
            )

            data_table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p.sku)),
                    ft.DataCell(ft.Text(p.nombre)),
                    ft.DataCell(ft.Text(p.categoria)),
                    ft.DataCell(ft.Text(p.ubicacion)),
                    ft.DataCell(ft.Text(str(ultimo_stock))),
                    ft.DataCell(ft.Text(str(p.stock_minimo))),
                    ft.DataCell(estado)
                ]
            ))

        # Actualizar estadísticas
        total_stock = sum(p.stock_actual[-1] for p in productos_filtrados)
        productos_bajo_stock = sum(1 for p in productos_filtrados if p.stock_actual[-1] < p.stock_minimo)
        rotacion = sum(p.historico[-1] for p in productos_filtrados) / total_stock if total_stock > 0 else 0

        stats_cards.controls = [
            stats_card("Total Stock", f"{total_stock:,}", ft.colors.BLUE_100),
            stats_card("Alertas Activas", productos_bajo_stock, ft.colors.RED_100),
            stats_card("Rotación Mensual", f"{rotacion:.1f}x", ft.colors.GREEN_100)
        ]

        # Actualizar alertas
        alertas_container.controls = [
            ft.ListTile(
                title=ft.Text(f"{p.nombre} - Stock crítico: {p.stock_actual[-1]} unidades"),
                leading=ft.Icon(ft.icons.WARNING, color=ft.colors.RED),
                subtitle=ft.Text(f"Mínimo requerido: {p.stock_minimo} | Ubicación: {p.ubicacion}")
            ) for p in productos_filtrados if p.stock_actual[-1] < p.stock_minimo
        ]

        page.update()

    def stats_card(title, value, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16),
                ft.Text(str(value), size=24, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            bgcolor=color,
            border_radius=10,
            expand=True
        )

    # Configurar eventos
    dropdown_categorias.on_change = update_ui
    search_field.on_change = update_ui

    # Construir interfaz
    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Dashboard de Inventarios",
                            size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([dropdown_categorias, search_field])
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            stats_cards,
            ft.Container(line_chart, height=400, padding=10),
            ft.Text("Alertas de Stock", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=alertas_container,
                bgcolor=ft.colors.RED_50,
                padding=10,
                border_radius=10
            ),
            ft.Text("Detalle de Inventario", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(data_table, padding=10)
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=20
    )