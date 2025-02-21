"""
Main game file for the Dungeon Loot Manager - Knapsack Problem visualization.
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
from common.viz_utils import create_tooltip
from knapsack import (
    Item, ItemType, VisualizationState, solve_knapsack,
    get_item_color, get_default_stats
)

class DungeonLootGame(GameBase):
    def __init__(self):
        super().__init__("Dungeon Loot Manager - Knapsack Problem")
        
        # Game state
        self.items = []  # List of available items
        self.capacity = 20  # Knapsack capacity
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.visualization_speed = 1.0
        self.step_timer = 0
        
        # Visual settings
        self.cell_size = 40
        self.table_x = 50
        self.table_y = 50
        self.items_x = 50
        self.items_y = 400
        
        # Create UI elements
        self.setup_ui()
        
        # Tutorial state
        self.show_tutorial = True
        self.tutorial_step = 0
        self.tutorial_messages = [
            "Welcome to Dungeon Loot Manager! Add items using the control panel.",
            "Each item has a weight and value - choose wisely!",
            "Watch how Dynamic Programming finds the optimal selection.",
            "The table shows the maximum value possible for each subproblem.",
            "Green cells show the current calculation.",
            "Selected items will be highlighted in gold.",
            "Try different combinations of items and capacities!",
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
        
        # Item type selection
        self.item_type_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=[t.name for t in ItemType],
            starting_option=ItemType.GOLDEN_CHALICE.name,
            relative_rect=pygame.Rect(
                self.width - 275,
                3 * spacing + 2 * button_height,
                button_width,
                button_height
            ),
            manager=self.ui_manager
        )
        
        # Add item button
        self.add_item_button = self.create_button(
            "Add Item",
            pygame.Rect(
                self.width - 275,
                4 * spacing + 3 * button_height,
                button_width,
                button_height
            )
        )
        
        # Capacity slider
        self.capacity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                self.width - 275,
                5 * spacing + 4 * button_height,
                button_width,
                button_height
            ),
            start_value=20,
            value_range=(10, 50),
            manager=self.ui_manager
        )
        
        # Capacity label
        self.capacity_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 275,
                6 * spacing + 5 * button_height,
                button_width,
                button_height // 2
            ),
            text="Capacity: 20",
            manager=self.ui_manager
        )
        
        # Speed slider
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                self.width - 275,
                7 * spacing + 6 * button_height,
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
                8 * spacing + 7 * button_height,
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
                9 * spacing + 8 * button_height,
                button_width,
                150
            ),
            manager=self.ui_manager
        )
        
        # Stats labels
        self.items_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 265,
                10 * spacing + 8 * button_height,
                button_width - 20,
                25
            ),
            text="Items: 0",
            manager=self.ui_manager
        )
        
        self.value_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 265,
                11 * spacing + 8 * button_height + 25,
                button_width - 20,
                25
            ),
            text="Best Value: -",
            manager=self.ui_manager
        )
    
    def handle_event(self, event):
        """Handle game-specific events."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.toggle_algorithm()
            elif event.ui_element == self.reset_button:
                self.reset_game()
            elif event.ui_element == self.add_item_button:
                self.add_random_item()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.toggle_algorithm()
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.visualization_speed = min(2.0, self.visualization_speed + 0.1)
            elif event.key == pygame.K_MINUS:
                self.visualization_speed = max(0.1, self.visualization_speed - 0.1)
        
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.item_type_dropdown:
                pass  # Item type selection changed
        
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.visualization_speed = event.value
            elif event.ui_element == self.capacity_slider:
                self.capacity = int(event.value)
                self.capacity_label.set_text(f"Capacity: {self.capacity}")
    
    def add_random_item(self):
        """Add a new item with default stats for its type."""
        # Fix the item type selection
        selected_type = self.item_type_dropdown.selected_option
        try:
            item_type = ItemType[selected_type]
        except KeyError:
            # Default to GOLDEN_CHALICE if there's an issue
            item_type = ItemType.GOLDEN_CHALICE
            
        weight, value = get_default_stats(item_type)
        
        # Add small random variation
        weight = max(1, weight + random.randint(-1, 1))
        value = max(1, value + random.randint(-2, 2))
        
        item = Item(
            name=f"Item {len(self.items) + 1}",
            weight=weight,
            value=value,
            item_type=item_type
        )
        
        self.items.append(item)
        self.items_label.set_text(f"Items: {len(self.items)}")
    
    def update(self, time_delta):
        """Update game state."""
        if self.algorithm_running:
            self.step_timer += time_delta
            if self.step_timer >= self.visualization_speed:
                self.step_timer = 0
                self.update_algorithm()
        
        # Update value label if we have a solution
        if self.viz_state.dp_table and len(self.items) > 0:
            best_value = self.viz_state.dp_table[len(self.items)][self.capacity]
            self.value_label.set_text(f"Best Value: {best_value}")
    
    def draw(self):
        """Draw game elements."""
        # Draw DP table
        if self.viz_state.dp_table:
            self.draw_dp_table()
        
        # Draw items
        self.draw_items()
        
        # Draw current step description
        if self.viz_state.step_description:
            tooltip = create_tooltip(
                self.viz_state.step_description,
                font_size=20
            )
            self.screen.blit(
                tooltip,
                (self.table_x, self.table_y - tooltip.get_height() - 10)
            )
            
        # Draw solution summary if algorithm is completed
        if self.viz_state.completed and self.viz_state.dp_table:
            n = len(self.items)
            max_value = self.viz_state.dp_table[n][self.capacity]
            selected_names = [item.name for item in self.viz_state.selected_items]
            summary = f"Take these items: {', '.join(selected_names)} for maximum value of {max_value}"
            tooltip = create_tooltip(
                summary,
                font_size=24,
                bg_color=(200, 255, 200)  # Light green background
            )
            self.screen.blit(
                tooltip,
                (self.table_x, self.table_y + len(self.viz_state.dp_table) * self.cell_size + 40)
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
    
    def draw_dp_table(self):
        """Draw the dynamic programming table."""
        if not self.viz_state.dp_table:
            return
            
        n = len(self.items)
        
        # Draw column headers (weights)
        for w in range(self.capacity + 1):
            x = self.table_x + w * self.cell_size
            y = self.table_y
            pygame.draw.rect(self.screen, self.GRAY,
                           (x, y, self.cell_size, self.cell_size))
            self.draw_text(str(w), (x + self.cell_size//2, y + self.cell_size//2),
                          size=20)
        
        # Draw row headers (items)
        for i in range(n + 1):
            x = self.table_x
            y = self.table_y + (i + 1) * self.cell_size
            pygame.draw.rect(self.screen, self.GRAY,
                           (x - self.cell_size, y, self.cell_size, self.cell_size))
            if i > 0:
                item = self.items[i - 1]
                color = get_item_color(item.item_type)
                pygame.draw.rect(self.screen, color,
                               (x - self.cell_size, y, self.cell_size, self.cell_size))
            self.draw_text(str(i), (x - self.cell_size//2, y + self.cell_size//2),
                          size=20)
        
        # Draw table cells
        for i in range(n + 1):
            for w in range(self.capacity + 1):
                x = self.table_x + w * self.cell_size
                y = self.table_y + (i + 1) * self.cell_size
                
                # Cell background
                color = self.WHITE
                if (i, w) == self.viz_state.current_cell:
                    color = (200, 255, 200)  # Light green
                elif (i, w) in self.viz_state.highlighted_cells:
                    color = (255, 255, 200)  # Light yellow
                
                pygame.draw.rect(self.screen, color,
                               (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, self.BLACK,
                               (x, y, self.cell_size, self.cell_size), 1)
                
                # Cell value
                if i <= len(self.viz_state.dp_table) and w < len(self.viz_state.dp_table[0]):
                    value = self.viz_state.dp_table[i][w]
                    self.draw_text(str(value),
                                 (x + self.cell_size//2, y + self.cell_size//2),
                                 size=20)
    
    def draw_items(self):
        """Draw the available items and their stats."""
        x = self.items_x
        y = self.items_y
        
        for item in self.items:
            # Item background
            color = get_item_color(item.item_type)
            if item in self.viz_state.selected_items:
                pygame.draw.rect(self.screen, (255, 215, 0),  # Gold
                               (x, y, 200, 60))
            pygame.draw.rect(self.screen, color, (x + 5, y + 5, 190, 50))
            
            # Item details
            self.draw_text(item.name, (x + 100, y + 20),
                          color=self.BLACK, size=20)
            self.draw_text(f"W: {item.weight} V: {item.value}",
                          (x + 100, y + 40), color=self.BLACK, size=16)
            
            y += 70
    
    def toggle_algorithm(self):
        """Start or stop the algorithm visualization."""
        if len(self.items) < 1:
            return
            
        self.algorithm_running = not self.algorithm_running
        if self.algorithm_running:
            self.viz_state = VisualizationState()
            self.start_button.set_text("Stop Algorithm")
        else:
            self.start_button.set_text("Start Algorithm")
    
    def reset_game(self):
        """Reset the game state."""
        self.items = []
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.start_button.set_text("Start Algorithm")
        self.items_label.set_text("Items: 0")
        self.value_label.set_text("Best Value: -")
    
    def update_algorithm(self):
        """Update algorithm visualization state."""
        if not self.algorithm_running:
            return
            
        # Run knapsack algorithm
        solve_knapsack(self.items, self.capacity, self.viz_state)
        
        if self.viz_state.completed:
            self.algorithm_running = False
            self.start_button.set_text("Start Algorithm")

if __name__ == "__main__":
    game = DungeonLootGame()
    game.run() 