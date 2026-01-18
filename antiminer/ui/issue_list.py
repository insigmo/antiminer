import flet as ft

from antiminer.constants import IssueStatus
from antiminer.logic.models import AppState


class IssueList(ft.BaseControl):
    def __init__(self, state: AppState):
        super().__init__()
        self.list_view = None
        self.state = state

    def build(self):
        self.list_view = ft.ListView(expand=1, spacing=10, padding=20)
        return self.list_view

    def update_ui(self):
        self.list_view.controls.clear()
        for issue in self.state.issues:
            color = ft.colors.RED if issue.status == IssueStatus.FAILED else \
                    ft.colors.GREEN if issue.status == IssueStatus.FIXED else \
                    ft.colors.AMBER
            
            self.list_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BUG_REPORT, color=color),
                    title=ft.Text(issue.title, color=color, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"{issue.description} | Status: {issue.status.value}"),
                    bgcolor=ft.colors.with_opacity(0.05, color)
                )
            )
        self.update()
