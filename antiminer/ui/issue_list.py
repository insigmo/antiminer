import flet as ft

from antiminer.constants import IssueStatus
from antiminer.logic.models import AppState


class IssueList(ft.Column):
    def __init__(self):
        super().__init__()
        self.list_view = ft.ListView(expand=1, spacing=10, padding=20)
        self.expand = True
        self.controls = [self.list_view]

    def update_ui(self, state: AppState):
        self.list_view.controls.clear()
        if not state.issues:
            self.update()
            return

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("File Name")),
                ft.DataColumn(ft.Text("Path")),
                ft.DataColumn(ft.Text("Vulnerability")),
                ft.DataColumn(ft.Text("Description")),
                ft.DataColumn(ft.Text("Status")),
            ],
            rows=[]
        )

        for issue in state.issues:
            color = ft.Colors.RED if issue.status == IssueStatus.FAILED else \
                    ft.Colors.GREEN if issue.status == IssueStatus.FIXED else \
                    ft.Colors.AMBER
            
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(issue.file_name, color=color, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(issue.path, size=12)),
                        ft.DataCell(ft.Text(issue.vulnerability, color=color)),
                        ft.DataCell(ft.Text(issue.description)),
                        ft.DataCell(ft.Text(issue.status.value, italic=True)),
                    ]
                )
            )
        
        self.list_view.controls.append(table)
        self.update()
