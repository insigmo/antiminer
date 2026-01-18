import pytest
import asyncio
from antiminer.app.services.scheduler import Scheduler
from antiminer.app.constants import TaskType

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
