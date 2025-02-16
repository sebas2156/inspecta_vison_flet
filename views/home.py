import flet as ft
from sidemenu import create_sidemenu

def create_home_view(page: ft.Page):
    # Datos para el gráfico
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    ventas_2023 = [35, 42, 67, 55, 72, 89, 95, 78, 64, 52, 48, 60]
    ventas_2024 = [45, 55, 70, 62, 85, 92, 98, 81, 73, 65, 58, 75]

    # Crear el menú lateral
    sidebar, menu_button = create_sidemenu(page)

    # Configurar gráfico lineal
    data_series = [
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(i, valor) for i, valor in enumerate(ventas_2023)],
            color=ft.colors.BLUE,
            stroke_width=3,
            curved=True
        ),
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(i, valor) for i, valor in enumerate(ventas_2024)],
            color=ft.colors.GREEN,
            stroke_width=3,
            curved=True
        )
    ]

    line_chart = ft.LineChart(
        data_series=data_series,
        border=ft.Border(bottom=ft.BorderSide(1, ft.colors.GREY)),
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(i, label=ft.Text(mes)) for i, mes in enumerate(meses)],
            labels_size=20
        ),
        expand=True
    )

    # Crear tabla de datos
    rows = []
    for i, mes in enumerate(meses):
        rows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(mes)),
                ft.DataCell(ft.Text(str(ventas_2023[i]))),
                ft.DataCell(ft.Text(str(ventas_2024[i])))
        ]))

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Mes")),
            ft.DataColumn(ft.Text("Ventas 2023")),
            ft.DataColumn(ft.Text("Ventas 2024"))
        ],
        rows=rows,
        vertical_lines=ft.BorderSide(1, ft.colors.GREY),
        horizontal_lines=ft.BorderSide(1, ft.colors.GREY)
    )

    # Contenedor principal del contenido
    content = ft.Column(
        controls=[
            ft.Container(line_chart, height=400),
            ft.Container(data_table, padding=20)
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO
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

    return ft.View(
        route="/home",
        controls=[view_content],
        padding=0,
        bgcolor=ft.colors.GREY_100,

    )