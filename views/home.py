import flet as ft

def main(page: ft.Page):
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    ventas_2023 = [35, 42, 67, 55, 72, 89, 95, 78, 64, 52, 48, 60]
    ventas_2024 = [45, 55, 70, 62, 85, 92, 98, 81, 73, 65, 58, 75]

    # Configurar gráfico lineal nativo de Flet
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

    # Crear una tabla con los datos de ventas
    rows = []
    for i, mes in enumerate(meses):
        rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(mes)),
            ft.DataCell(ft.Text(str(ventas_2023[i]))),
            ft.DataCell(ft.Text(str(ventas_2024[i])))
        ]))

    # Configurar la tabla
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

    # Contenedor de la página con scroll
    page.scroll = ft.ScrollMode.ALWAYS  # Habilitar el scroll en toda la página
    page.add(line_chart, data_table)

ft.app(target=main)
