import asyncio
import logging

from antiminer.constants import TaskType, IssueStatus
from antiminer.logic.models import AppState
from antiminer.services.scheduler import Scheduler

LOGGER = logging.getLogger("antiminer")


class Fixer:
    def __init__(self, scheduler: Scheduler, state: AppState):
        self.scheduler = scheduler
        self.state = state

    async def fix_issues(self):
        self.state.is_running = True
        pending_issues = [i for i in self.state.issues if i.status != IssueStatus.FIXED]
        self.state.total_count = len(pending_issues)
        self.state.processed_count = 0
        
        for issue in pending_issues:
            LOGGER.info(f"[FIX] Attempting to fix: {issue.id}")
            
            # Simulate IO-bound fix (e.g., deleting a file or updating a database)
            async def io_fix_task(iid):
                await asyncio.sleep(0.2)
                return iid.endswith("0") or iid.endswith("2") # Simulate some failures

            success = await self.scheduler.schedule(TaskType.IO, io_fix_task, issue.id)
            
            new_status = IssueStatus.FIXED if success else IssueStatus.FAILED
            self.state.update_issue(issue.id, new_status)
            
            self.state.processed_count += 1
            self.state.progress = self.state.processed_count / self.state.total_count
            
        self.state.is_running = False
