from dataclasses import dataclass, field
from typing import List, Optional
from antiminer.constants import IssueStatus

@dataclass(frozen=True)
class Issue:
    id: str
    title: str
    description: str
    status: IssueStatus

@dataclass(frozen=True)
class AppState:
    analysis_mode: Optional[str] = None
    issues: List[Issue] = field(default_factory=list)
    progress: float = 0.0
    processed_count: int = 0
    total_count: int = 0
    is_running: bool = False

    def with_update(self, **kwargs) -> "AppState":
        return AppState(**{**self.__dict__, **kwargs})

    def with_issue_update(self, issue_id: str, status: IssueStatus) -> "AppState":
        new_issues = []
        for issue in self.issues:
            if issue.id == issue_id:
                new_issues.append(Issue(issue.id, issue.title, issue.description, status))
            else:
                new_issues.append(issue)
        
        sorted_issues = sorted(
            new_issues,
            key=lambda x: (0 if x.status == IssueStatus.FAILED else 1)
        )
        return self.with_update(issues=sorted_issues)
