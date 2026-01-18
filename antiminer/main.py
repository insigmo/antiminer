import flet as ft

from antiminer.services.logger import setup_logger
from antiminer.ui.app_view import main_view

def main():
    setup_logger()
    ft.app(target=main_view)

if __name__ == "__main__":
    main()
