import asyncio
import logging
from typing import Callable, Any

from antiminer.constants import TaskType
from antiminer.services.executors import ExecutorManager

LOGGER = logging.getLogger("antiminer")

class Scheduler:
    def __init__(self):
        self.cpu_executor = ExecutorManager.get_cpu_executor()

    async def schedule(self, task_type: TaskType, func: Callable, *args, **kwargs) -> Any:
        LOGGER.info(f"[{task_type.value}] Scheduling task: {func.__name__}")
        
        if task_type == TaskType.IO:
            # IO-bound code NEVER in ProcessPool
            return await func(*args, **kwargs)
        elif task_type == TaskType.CPU:
            # CPU-bound code NEVER in event loop
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(self.cpu_executor, func, *args, **kwargs)
        else:
            raise ValueError(f"Unknown TaskType: {task_type}")
