from dataclasses import dataclass, field

from antiminer.constants import IssueStatus


@dataclass(frozen=True)
class Issue:
    id: str
    title: str
    description: str
    status: IssueStatus


@dataclass
class AppState:
    analysis_mode: str | None = None
    issues: list[Issue] = field(default_factory=list)
    progress: float = 0.0
    processed_count: int = 0
    total_count: int = 0
    is_running: bool = False

    def update_issue(self, issue_id: str, status: IssueStatus) -> None:
        new_issues = []
        for issue in self.issues:
            if issue.id == issue_id:
                new_issues.append(Issue(issue.id, issue.title, issue.description, status))
            else:
                new_issues.append(issue)

        # Sort: FAILED issues move to top in the table
        self.issues = sorted(
            new_issues,
            key=lambda x: (0 if x.status == IssueStatus.FAILED else 1)
        )
