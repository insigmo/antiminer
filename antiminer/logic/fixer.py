import asyncio
import logging
from typing import Callable
from antiminer.constants import TaskType, IssueStatus
from antiminer.logic.models import AppState
from antiminer.services.scheduler import Scheduler

LOGGER = logging.getLogger("antiminer")

class Fixer:
    def __init__(self, scheduler: Scheduler, update_state: Callable):
        self.scheduler = scheduler
        self.update_state = update_state

    async def fix_issues(self, current_state: AppState):
        self.update_state(lambda s: s.with_update(is_running=True))
        
        pending_issues = [i for i in current_state.issues if i.status != IssueStatus.FIXED]
        self.update_state(lambda s: s.with_update(
            total_count=len(pending_issues),
            processed_count=0,
            progress=0.0
        ))
        
        for issue in pending_issues:
            LOGGER.info(f"[FIX] Attempting to fix: {issue.id}")
            
            async def io_fix_task(iid):
                await asyncio.sleep(0.2)
                return iid.endswith("0") or iid.endswith("2")
            
            success = await self.scheduler.schedule(TaskType.IO, io_fix_task, issue.id)
            
            new_status = IssueStatus.FIXED if success else IssueStatus.FAILED
            self.update_state(lambda s: s.with_issue_update(issue.id, new_status))
            
            self.update_state(lambda s: s.with_update(
                processed_count=s.processed_count + 1,
                progress=(s.processed_count + 1) / s.total_count
            ))
            
        self.update_state(lambda s: s.with_update(is_running=False))
