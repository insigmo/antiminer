import flet as ft

from antiminer.logic.models import AppState


class ProgressView(ft.BaseControl):
    def __init__(self, state: AppState):
        super().__init__()
        self.text = None
        self.bar = None
        self.state = state

    def build(self):
        self.bar = ft.ProgressBar(value=0, width=400, color=ft.colors.BLUE)
        self.text = ft.Text("Ready")
        return ft.Column([
            self.bar,
            self.text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def update_ui(self):
        self.bar.value = self.state.progress
        self.text.value = f"Processed: {self.state.processed_count} / {self.state.total_count}" if self.state.total_count > 0 else "Ready"
        self.update()
