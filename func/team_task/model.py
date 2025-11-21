from dataclasses import dataclass
from datetime import datetime

# Status constants
STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"

@dataclass
class Task:
    task_id: int
    title: str
    description: str
    assigned_to: str | None
    status: str
    created_at: str
