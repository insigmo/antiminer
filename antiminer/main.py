import asyncio

import flet as ft

from antiminer.services.logger import setup_logger
from antiminer.ui.app_view import main_view


async def main_async():
    setup_logger()
    await ft.run_async(main_view)


def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
