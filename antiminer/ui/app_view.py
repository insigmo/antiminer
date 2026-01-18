import flet as ft
import asyncio

from antiminer.logic.analyzer import Analyzer
from antiminer.logic.fixer import Fixer
from antiminer.logic.models import AppState
from antiminer.services.scheduler import Scheduler
from antiminer.ui.analysis_controls import AnalysisControls
from antiminer.ui.issue_list import IssueList
from antiminer.ui.progress_view import ProgressView


async def main_view(page: ft.Page):
    page.title = "AntiMiner"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 600
    
    state = AppState()
    scheduler = Scheduler()
    analyzer = Analyzer(scheduler, state)
    fixer = Fixer(scheduler, state)
    
    async def on_analyze(e):
        targets = [f"file_{i}.exe" for i in range(10)]
        asyncio.create_task(analyzer.run_analysis(targets))
        asyncio.create_task(ui_update_loop())

    async def on_fix(e):
        asyncio.create_task(fixer.fix_issues())
        asyncio.create_task(ui_update_loop())

    async def ui_update_loop():
        while state.is_running:
            controls.update_ui()
            progress.update_ui()
            issues.update_ui()
            await asyncio.sleep(0.1)
        controls.update_ui()
        progress.update_ui()
        issues.update_ui()

    controls = AnalysisControls(state, on_analyze, on_fix)
    progress = ProgressView(state)
    issues = IssueList(state)

    page.add(
        ft.Column([
            ft.Text("AntiMiner System Analysis", size=30, weight=ft.FontWeight.BOLD),
            controls,
            progress,
            ft.Divider(),
            ft.Text("Detected Issues", size=20),
            issues
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
