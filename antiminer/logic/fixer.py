import logging
import os
import re
import shutil
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
            
            async def io_fix_task(issue_obj):
                file_path = os.path.join(issue_obj.path, issue_obj.file_name)
                if not os.path.exists(file_path):
                    return False
                
                try:
                    # 1. Create Backup
                    backup_path = file_path + ".matrix_backup"
                    shutil.copy2(file_path, backup_path)
                    
                    # 2. Neutralize based on type
                    if file_path.endswith(('.exe', '.dll')):
                        # Simplified EXE neutralization: append signature
                        with open(file_path, "ab") as f:
                            f.write(b"\n\n[NEUTRALIZED_BY_MATRIX_RAT_REMOVAL]\n")
                    else:
                        # Script neutralization
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            
                            # Neutralize dangerous patterns
                            patterns = [r"CreateObject", r"\.Run\(", r"eval\(", r"invoke-expression"]
                            for p in patterns:
                                content = re.sub(p, "/* DISABLED_BY_MATRIX */", content, flags=re.IGNORECASE)
                            
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content)
                        except Exception:
                            return False
                    
                    return True
                except Exception as e:
                    LOGGER.error(f"Fix error: {e}")
                    return False
            
            success = await self.scheduler.schedule(TaskType.IO, io_fix_task, issue)
            
            new_status = IssueStatus.FIXED if success else IssueStatus.FAILED
            self.update_state(lambda s: s.with_issue_update(issue.id, new_status))
            
            self.update_state(lambda s: s.with_update(
                processed_count=s.processed_count + 1,
                progress=(s.processed_count + 1) / s.total_count
            ))
            
        self.update_state(lambda s: s.with_update(is_running=False))
