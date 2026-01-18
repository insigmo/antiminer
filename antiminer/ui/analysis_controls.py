from typing import Callable
import flet as ft
from antiminer.logic.models import AppState
from antiminer.constants import IssueStatus

class AnalysisControls(ft.Column):
    def __init__(self, on_analyze: Callable, on_fix: Callable):
        super().__init__()
        self.on_analyze = on_analyze
        self.on_fix = on_fix
        self.analyze_btn = ft.ElevatedButton("Start Analysis", on_click=self.on_analyze)
        self.fix_btn = ft.ElevatedButton("Fix Issues", on_click=self.on_fix)
        self.controls = [ft.Row([self.analyze_btn, self.fix_btn], alignment=ft.MainAxisAlignment.CENTER)]

    def update_ui(self, state: AppState):
        self.analyze_btn.disabled = state.is_running
        has_actionable = any(i.status != IssueStatus.FIXED for i in state.issues)
        self.fix_btn.disabled = state.is_running or not has_actionable
        self.update()
