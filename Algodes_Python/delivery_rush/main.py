"""
Main game file for the Delivery Rush - Minimizing Lateness visualization.
Handles game initialization, rendering, and user interaction.
"""

import os
import sys
import random
import pygame
import pygame_gui

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.game_base import GameBase
from common.viz_utils import create_tooltip, draw_progress_bar
from scheduler import (
    Task, TaskType, VisualizationState, schedule_tasks,
    get_task_color, get_default_processing_time,
    get_default_deadline_range, get_task_description
)

class TaskCreationDialog:
    def __init__(self, ui_manager, window_size, task_type):
        width = 300
        height = 250
        x = (window_size[0] - width) // 2
        y = (window_size[1] - height) // 2
        
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((x, y), (width, height)),
            manager=ui_manager,
            window_display_title="Create New Task"
        )
        
        # Task name entry
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, width-20, 25),
            text="Task Name:",
            manager=ui_manager,
            container=self.window
        )
        
        self.name_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 40, width-20, 30),
            manager=ui_manager,
            container=self.window
        )
        
        # Processing time entry
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 80, width-20, 25),
            text="Processing Time:",
            manager=ui_manager,
            container=self.window
        )
        
        self.processing_time_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 110, width-20, 30),
            manager=ui_manager,
            container=self.window
        )
        
        # Deadline entry
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 150, width-20, 25),
            text="Deadline:",
            manager=ui_manager,
            container=self.window
        )
        
        self.deadline_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 180, width-20, 30),
            manager=ui_manager,
            container=self.window
        )
        
        # Create button
        self.create_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(width-110, height-40, 100, 30),
            text="Create",
            manager=ui_manager,
            container=self.window
        )
        
        # Set default values
        proc_time = get_default_processing_time(task_type)
        deadline_min, deadline_max = get_default_deadline_range(task_type)
        self.name_entry.set_text(f"Task {task_type.name}")
        self.processing_time_entry.set_text(str(proc_time))
        self.deadline_entry.set_text(str(deadline_min))

class DeliveryRushGame(GameBase):
    def __init__(self):
        super().__init__("Delivery Rush - Minimizing Lateness Algorithm")
        
        # Game state
        self.tasks = []  # List of delivery tasks
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.visualization_speed = 1.0
        self.step_timer = 0
        self.task_creation_dialog = None
        
        # Visual settings
        self.timeline_height = 400
        self.timeline_y = 100
        self.task_height = 40
        self.pixels_per_time_unit = 10
        self.task_list_rect = pygame.Rect(50, 450, self.width - 400, 250)
        
        # Create UI elements
        self.setup_ui()
        
        # Tutorial state
        self.show_tutorial = True
        self.tutorial_step = 0
        self.tutorial_messages = [
            "Welcome to Delivery Rush! Add delivery tasks using the control panel.",
            "Enter task details in the dialog that appears.",
            "Watch how the Earliest Deadline First algorithm minimizes maximum lateness.",
            "The timeline shows task schedules and deadlines.",
            "Different colors represent different types of deliveries.",
            "Try creating tasks with varying deadlines to see how the schedule changes!",
        ]
    
    def setup_ui(self):
        """Create UI elements for the game."""
        # Control panel background
        panel_rect = pygame.Rect(self.width - 300, 0, 300, self.height)
        self.control_panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=self.ui_manager
        )
        
        # Buttons and controls
        button_width = 250
        button_height = 40
        spacing = 10
        
        # Start/Stop button
        self.start_button = self.create_button(
            "Start Algorithm",
            pygame.Rect(
                self.width - 275,
                spacing,
                button_width,
                button_height
            )
        )
        
        # Reset button
        self.reset_button = self.create_button(
            "Reset",
            pygame.Rect(
                self.width - 275,
                2 * spacing + button_height,
                button_width,
                button_height
            )
        )
        
        # Add task button
        self.add_task_button = self.create_button(
            "Add Task",
            pygame.Rect(
                self.width - 275,
                3 * spacing + 2 * button_height,
                button_width,
                button_height
            )
        )
        
        # Speed slider
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                self.width - 275,
                4 * spacing + 3 * button_height,
                button_width,
                button_height
            ),
            start_value=1.0,
            value_range=(0.1, 2.0),
            manager=self.ui_manager
        )
        
        # Speed label
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 275,
                5 * spacing + 4 * button_height,
                button_width,
                button_height // 2
            ),
            text="Visualization Speed",
            manager=self.ui_manager
        )
        
        # Stats panel
        self.stats_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                self.width - 275,
                6 * spacing + 5 * button_height,
                button_width,
                150
            ),
            manager=self.ui_manager
        )
        
        # Stats labels
        self.tasks_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 265,
                7 * spacing + 5 * button_height,
                button_width - 20,
                25
            ),
            text="Tasks: 0",
            manager=self.ui_manager
        )
        
        self.lateness_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 265,
                8 * spacing + 5 * button_height + 25,
                button_width - 20,
                25
            ),
            text="Max Lateness: -",
            manager=self.ui_manager
        )
    
    def handle_event(self, event):
        """Handle game-specific events."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.toggle_algorithm()
            elif event.ui_element == self.reset_button:
                self.reset_game()
            elif event.ui_element == self.add_task_button:
                self.show_task_creation_dialog()
            elif self.task_creation_dialog and event.ui_element == self.task_creation_dialog.create_button:
                self.create_task_from_dialog()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.toggle_algorithm()
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.visualization_speed = min(2.0, self.visualization_speed + 0.1)
            elif event.key == pygame.K_MINUS:
                self.visualization_speed = max(0.1, self.visualization_speed - 0.1)
        
        elif event.type == pygame_gui.UI_WINDOW_CLOSE:
            if self.task_creation_dialog and event.ui_element == self.task_creation_dialog.window:
                self.task_creation_dialog = None
        
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.visualization_speed = event.value
    
    def show_task_creation_dialog(self):
        """Show dialog for creating a new task."""
        self.task_creation_dialog = TaskCreationDialog(
            self.ui_manager,
            (self.width, self.height),
            TaskType.REGULAR  # Default type
        )

    def create_task_from_dialog(self):
        """Create a task from the dialog input."""
        if not self.task_creation_dialog:
            return
            
        try:
            name = self.task_creation_dialog.name_entry.get_text()
            processing_time = int(self.task_creation_dialog.processing_time_entry.get_text())
            deadline = int(self.task_creation_dialog.deadline_entry.get_text())
            
            task = Task(
                name=name,
                processing_time=processing_time,
                deadline=deadline,
                task_type=TaskType.REGULAR  # All tasks are regular type
            )
            
            self.tasks.append(task)
            self.tasks_label.set_text(f"Tasks: {len(self.tasks)}")
            
            # Close the dialog
            self.task_creation_dialog.window.kill()
            self.task_creation_dialog = None
            
        except ValueError:
            # Handle invalid input
            pass
    
    def add_random_task(self):
        """Add a new task with random but sensible timing."""
        # Fix the task type selection
        selected_type = self.task_type_dropdown.selected_option
        try:
            task_type = TaskType[selected_type]
        except KeyError:
            # Default to REGULAR if there's an issue
            task_type = TaskType.REGULAR
            
        processing_time = get_default_processing_time(task_type)
        deadline_min, deadline_max = get_default_deadline_range(task_type)
        deadline = random.randint(deadline_min, deadline_max)
        
        task = Task(
            name=f"Task {len(self.tasks) + 1}",
            processing_time=processing_time,
            deadline=deadline,
            task_type=task_type
        )
        
        self.tasks.append(task)
        self.tasks_label.set_text(f"Tasks: {len(self.tasks)}")
    
    def update(self, time_delta):
        """Update game state."""
        if self.algorithm_running:
            self.step_timer += time_delta
            if self.step_timer >= self.visualization_speed:
                self.step_timer = 0
                self.update_algorithm()
        
        # Update lateness label
        if self.viz_state.scheduled_tasks:
            self.lateness_label.set_text(f"Max Lateness: {self.viz_state.max_lateness}")
    
    def draw(self):
        """Draw game elements."""
        # Draw timeline background
        timeline_rect = pygame.Rect(
            50, self.timeline_y,
            self.width - 400, self.timeline_height
        )
        pygame.draw.rect(self.screen, self.WHITE, timeline_rect)
        pygame.draw.rect(self.screen, self.BLACK, timeline_rect, 2)
        
        # Draw task list background
        pygame.draw.rect(self.screen, self.WHITE, self.task_list_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.task_list_rect, 2)
        
        # Draw task list title
        self.draw_text(
            "Task List",
            (self.task_list_rect.centerx, self.task_list_rect.y + 20),
            size=24
        )
        
        # Draw tasks in list
        y = self.task_list_rect.y + 50
        for task in self.tasks:
            color = get_task_color(task.task_type)
            pygame.draw.rect(self.screen, color,
                           (self.task_list_rect.x + 10, y, 
                            self.task_list_rect.width - 20, 30))
            
            self.draw_text(
                f"{task.name} (Process: {task.processing_time}, Deadline: {task.deadline})",
                (self.task_list_rect.centerx, y + 15),
                color=self.BLACK,
                size=20
            )
            
            y += 40
        
        # Draw time markers
        max_time = max(
            (task.deadline for task in self.tasks),
            default=120
        )
        
        for t in range(0, max_time + 30, 10):
            x = 50 + t * self.pixels_per_time_unit
            if x < self.width - 400:
                pygame.draw.line(
                    self.screen, self.GRAY,
                    (x, self.timeline_y),
                    (x, self.timeline_y + self.timeline_height)
                )
                self.draw_text(
                    str(t),
                    (x, self.timeline_y - 20),
                    size=20
                )
        
        # Draw scheduled tasks
        y_offset = self.timeline_y + 10
        for task, start, end in self.viz_state.scheduled_tasks:
            # Task rectangle
            task_rect = pygame.Rect(
                50 + start * self.pixels_per_time_unit,
                y_offset,
                (end - start) * self.pixels_per_time_unit,
                self.task_height
            )
            pygame.draw.rect(self.screen, get_task_color(task.task_type), task_rect)
            pygame.draw.rect(self.screen, self.BLACK, task_rect, 2)
            
            # Task name
            self.draw_text(
                task.name,
                (task_rect.centerx, task_rect.centery),
                color=self.BLACK,
                size=20
            )
            
            # Deadline marker
            deadline_x = 50 + task.deadline * self.pixels_per_time_unit
            if deadline_x < self.width - 400:
                pygame.draw.line(
                    self.screen, self.RED,
                    (deadline_x, y_offset),
                    (deadline_x, y_offset + self.task_height),
                    2
                )
            
            y_offset += self.task_height + 10
        
        # Draw current task highlight
        if self.viz_state.current_task:
            task = self.viz_state.current_task
            y_offset = self.timeline_y + 10
            for t, _, _ in self.viz_state.scheduled_tasks:
                if t == task:
                    task_rect = pygame.Rect(
                        50 + self.viz_state.current_time * self.pixels_per_time_unit,
                        y_offset,
                        task.processing_time * self.pixels_per_time_unit,
                        self.task_height
                    )
                    pygame.draw.rect(self.screen, self.GREEN, task_rect, 3)
                    break
                y_offset += self.task_height + 10
        
        # Draw algorithm completion message
        if self.viz_state.completed and self.viz_state.scheduled_tasks:
            max_lateness = self.viz_state.max_lateness
            summary = f"Schedule complete! Maximum lateness: {max_lateness} time units"
            tooltip = create_tooltip(
                summary,
                font_size=24,
                bg_color=(200, 255, 200)  # Light green background
            )
            self.screen.blit(
                tooltip,
                (50, self.task_list_rect.bottom + 20)
            )
        
        # Draw tutorial if active
        if self.show_tutorial and self.tutorial_step < len(self.tutorial_messages):
            tooltip = create_tooltip(
                self.tutorial_messages[self.tutorial_step],
                font_size=24
            )
            self.screen.blit(
                tooltip,
                (10, self.height - tooltip.get_height() - 10)
            )
    
    def toggle_algorithm(self):
        """Start or stop the algorithm visualization."""
        if len(self.tasks) < 1:
            return
            
        self.algorithm_running = not self.algorithm_running
        if self.algorithm_running:
            self.viz_state = VisualizationState()
            self.start_button.set_text("Stop Algorithm")
        else:
            self.start_button.set_text("Start Algorithm")
    
    def reset_game(self):
        """Reset the game state."""
        self.tasks = []
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.start_button.set_text("Start Algorithm")
        self.tasks_label.set_text("Tasks: 0")
        self.lateness_label.set_text("Max Lateness: -")
    
    def update_algorithm(self):
        """Update algorithm visualization state."""
        if not self.algorithm_running:
            return
            
        # Run scheduling algorithm
        schedule_tasks(self.tasks, self.viz_state)
        
        if self.viz_state.completed:
            self.algorithm_running = False
            self.start_button.set_text("Start Algorithm")

if __name__ == "__main__":
    game = DeliveryRushGame()
    game.run() 