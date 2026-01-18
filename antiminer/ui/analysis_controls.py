from typing import Callable

import flet as ft

from antiminer.constants import IssueStatus
from antiminer.logic.models import AppState


class AnalysisControls(ft.Column):
    def __init__(self, on_analyze: Callable, on_fix: Callable):
        super().__init__()
        self.on_analyze = on_analyze
        self.on_fix = on_fix
        self.full_scan_btn = ft.ElevatedButton(
            "Full Scan", 
            icon=ft.icons.Icons.SEARCH,
            on_click=self._on_full_scan
        )
        self.deep_analysis_btn = ft.ElevatedButton(
            "Deep Analysis", 
            icon=ft.icons.Icons.SCREEN_SEARCH_DESKTOP,
            on_click=self._on_deep_analysis
        )
        self.fix_btn = ft.ElevatedButton(
            "Fix Issues", 
            icon=ft.icons.Icons.HOME_REPAIR_SERVICE,
            on_click=self.on_fix
        )
        self.controls = [
            ft.Row(
                [self.full_scan_btn, self.deep_analysis_btn, self.fix_btn], 
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

    async def _on_full_scan(self, e):
        await self.on_analyze(e, "Full Scan")

    async def _on_deep_analysis(self, e):
        await self.on_analyze(e, "Deep Analysis")

    def update_ui(self, state: AppState):
        self.full_scan_btn.disabled = state.is_running
        self.deep_analysis_btn.disabled = state.is_running
        has_actionable = any(i.status != IssueStatus.FIXED for i in state.issues)
        self.fix_btn.disabled = state.is_running or not has_actionable
        self.update()
