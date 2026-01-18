from typing import Callable

import flet as ft

from antiminer.logic.models import AppState


class AnalysisControls(ft.BaseControl):
    def __init__(self, state: AppState, on_analyze: Callable, on_fix: Callable):
        super().__init__()
        self.fix_btn = None
        self.analyze_btn = None
        self.state = state
        self.on_analyze = on_analyze
        self.on_fix = on_fix

    def build(self):
        self.analyze_btn = ft.ElevatedButton(
            "Start Analysis", 
            on_click=self.on_analyze,
            disabled=self.state.is_running
        )
        self.fix_btn = ft.ElevatedButton(
            "Fix Issues", 
            on_click=self.on_fix,
            disabled=self.state.is_running or not any(i.status != "FIXED" for i in self.state.issues)
        )
        
        return ft.Row([self.analyze_btn, self.fix_btn], alignment=ft.MainAxisAlignment.CENTER)

    def update_ui(self):
        self.analyze_btn.disabled = self.state.is_running
        has_actionable = any(i.status != "FIXED" for i in self.state.issues)
        self.fix_btn.disabled = self.state.is_running or not has_actionable
        self.update()
