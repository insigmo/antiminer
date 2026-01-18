import asyncio

import pytest

from antiminer.constants import TaskType
from antiminer.services.scheduler import Scheduler


@pytest.mark.asyncio
async def test_scheduler_io():
    scheduler = Scheduler()
    async def io_task(x):
        await asyncio.sleep(0.01)
        return x * 2
    
    result = await scheduler.schedule(TaskType.IO, io_task, 21)
    assert result == 42

def cpu_task(x):
    return x * x

@pytest.mark.asyncio
async def test_scheduler_cpu():
    scheduler = Scheduler()
    result = await scheduler.schedule(TaskType.CPU, cpu_task, 10)
    assert result == 100
