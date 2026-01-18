import flet as ft
from antiminer.logic.models import AppState

class ProgressView(ft.Column):
    def __init__(self):
        super().__init__()
        self.bar = ft.ProgressBar(value=0, width=400, color=ft.Colors.BLUE)
        self.text = ft.Text("Ready")
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [self.bar, self.text]

    def update_ui(self, state: AppState):
        self.bar.value = state.progress
        self.text.value = f"Processed: {state.processed_count} / {state.total_count}" if state.total_count > 0 else "Ready"
        self.update()
