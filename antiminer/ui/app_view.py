import asyncio
from typing import Callable

import flet as ft
import psutil

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
    
    # 3.2 State Invariants: Единственный источник истины — AppState
    # В Flet мы храним состояние и обновляем UI при его изменении
    state = AppState()
    scheduler = Scheduler()

    def update_state(fn: Callable[[AppState], AppState]):
        nonlocal state
        state = fn(state)
        # UI только читает state и диспатчит события
        controls.update_ui(state)
        progress.update_ui(state)
        issues.update_ui(state)

    analyzer = Analyzer(scheduler, update_state)
    fixer = Fixer(scheduler, update_state)
    
    async def on_analyze(_, mode: str = "Full Scan"):
        import os
        targets = []
        mounts = [p.mountpoint for p in psutil.disk_partitions()]
        for mount in mounts:
            for root, _, files in os.walk(mount):
                for file in files:
                    targets.append(os.path.join(root, file))
        
        if targets:
            # Scheduler изолирует исполнение от UI
            asyncio.create_task(analyzer.run_analysis(targets, mode))

    async def on_fix(_):
        # Scheduler изолирует исполнение от UI
        asyncio.create_task(fixer.fix_issues(state))

    controls = AnalysisControls(on_analyze, on_fix)
    progress = ProgressView()
    issues = IssueList()

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
    
    # Initial UI update
    update_state(lambda s: s)
