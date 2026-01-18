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
        for issue in state.issues:
            color = ft.Colors.RED if issue.status == IssueStatus.FAILED else \
                    ft.Colors.GREEN if issue.status == IssueStatus.FIXED else \
                    ft.Colors.AMBER
            
            self.list_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.Icons.BUG_REPORT, color=color),
                    title=ft.Text(issue.title, color=color, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{issue.description} | Status: {issue.status.value}"),
                    bgcolor=ft.Colors.with_opacity(0.05, color)
                )
            )
        self.update()
