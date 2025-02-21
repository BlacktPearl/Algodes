"""
Implementation of the Earliest Deadline First (EDF) scheduling algorithm
for minimizing maximum lateness in delivery scheduling.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum, auto

class TaskType(Enum):
    """Types of delivery tasks with different characteristics."""
    HOT_PIZZA = auto()      # Short processing, tight deadline
    MEDICAL = auto()        # Medium processing, critical deadline
    REGULAR = auto()        # Longer processing, flexible deadline
    EXPRESS = auto()        # Short processing, moderate deadline

@dataclass
class Task:
    """Represents a delivery task with timing constraints."""
    name: str
    processing_time: int    # Time needed to complete delivery
    deadline: int          # When delivery must be completed
    task_type: TaskType
    
    def lateness(self, completion_time: int) -> int:
        """Calculate how late the task is based on completion time."""
        return max(0, completion_time - self.deadline)

class VisualizationState:
    """Tracks the current state of algorithm visualization."""
    def __init__(self):
        self.current_time = 0
        self.current_task: Optional[Task] = None
        self.scheduled_tasks: List[Tuple[Task, int, int]] = []  # (task, start, end)
        self.remaining_tasks: List[Task] = []
        self.max_lateness = 0
        self.step_description = ""
        self.sorting_indices: List[int] = []  # Indices being compared during sort
        self.completed = False

def schedule_tasks(tasks: List[Task], viz_state: VisualizationState) -> List[Tuple[Task, int, int]]:
    """
    Schedule tasks using Earliest Deadline First to minimize maximum lateness.
    
    Args:
        tasks: List of tasks to schedule
        viz_state: Current visualization state to update
        
    Returns:
        List of (task, start_time, end_time) tuples representing the schedule
    """
    if not tasks:
        return []
    
    # Sort tasks by deadline (EDF)
    tasks_sorted = sorted(tasks, key=lambda t: t.deadline)
    
    # Update visualization state
    viz_state.remaining_tasks = tasks_sorted.copy()
    viz_state.step_description = "Sorting tasks by deadline (Earliest Deadline First)"
    
    current_time = 0
    schedule = []
    max_lateness = 0
    
    # Schedule each task in EDF order
    for task in tasks_sorted:
        # Update visualization state
        viz_state.current_task = task
        viz_state.current_time = current_time
        
        # Schedule task
        start_time = current_time
        end_time = current_time + task.processing_time
        schedule.append((task, start_time, end_time))
        
        # Update maximum lateness
        lateness = max(0, end_time - task.deadline)
        max_lateness = max(max_lateness, lateness)
        
        # Update visualization state
        viz_state.scheduled_tasks.append((task, start_time, end_time))
        viz_state.max_lateness = max_lateness
        viz_state.remaining_tasks.remove(task)
        viz_state.step_description = (
            f"Scheduled {task.name} (Start: {start_time}, End: {end_time}, "
            f"Deadline: {task.deadline}, Lateness: {lateness})"
        )
        
        # Move time forward
        current_time = end_time
    
    viz_state.completed = True
    return schedule

def get_task_color(task_type: TaskType) -> Tuple[int, int, int]:
    """Get the display color for a task type."""
    colors = {
        TaskType.HOT_PIZZA: (255, 100, 100),  # Red
        TaskType.MEDICAL: (100, 255, 100),    # Green
        TaskType.REGULAR: (100, 100, 255),    # Blue
        TaskType.EXPRESS: (255, 255, 100),    # Yellow
    }
    return colors[task_type]

def get_default_processing_time(task_type: TaskType) -> int:
    """Get the default processing time for a task type."""
    times = {
        TaskType.HOT_PIZZA: 10,   # Quick delivery
        TaskType.MEDICAL: 20,     # Medium delivery
        TaskType.REGULAR: 30,     # Longer delivery
        TaskType.EXPRESS: 15,     # Moderate delivery
    }
    return times[task_type]

def get_default_deadline_range(task_type: TaskType) -> Tuple[int, int]:
    """Get the default deadline range for a task type."""
    ranges = {
        TaskType.HOT_PIZZA: (15, 30),    # Tight deadline
        TaskType.MEDICAL: (30, 60),      # Critical but realistic
        TaskType.REGULAR: (60, 120),     # Flexible
        TaskType.EXPRESS: (25, 45),      # Moderate
    }
    return ranges[task_type]

def get_task_description(task_type: TaskType) -> str:
    """Get a description of the task type."""
    descriptions = {
        TaskType.HOT_PIZZA: "Hot pizza delivery - Must be delivered quickly!",
        TaskType.MEDICAL: "Medical supplies - Critical delivery with strict deadline",
        TaskType.REGULAR: "Regular package - Standard delivery with flexible timing",
        TaskType.EXPRESS: "Express mail - Priority delivery with moderate deadline",
    }
    return descriptions[task_type] 