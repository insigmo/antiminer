import flet as ft
import asyncio
import sys
from antiminer.services.logger import setup_logger
from antiminer.ui.app_view import main_view

def main():
    setup_logger()
    
    # 2. Формальная цель: Использовать asyncio + uvloop для IO
    if sys.platform != "win32":
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass
            
    ft.app(target=main_view)

if __name__ == "__main__":
    main()
