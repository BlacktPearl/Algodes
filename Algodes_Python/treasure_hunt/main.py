"""
Main game file for the Treasure Hunt - Closest Pair visualization.
Handles game initialization, rendering, and user interaction.
"""

import os
import sys
import math
import pygame
import pygame_gui

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.game_base import GameBase
from common.viz_utils import create_tooltip
from closest_pair import Point, VisualizationState, closest_pair_recursive, brute_force

def create_treasure_surface(size):
    """Create a surface with a simple treasure chest drawing."""
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Colors
    BROWN = (139, 69, 19)
    GOLD = (255, 215, 0)
    
    # Draw chest
    width, height = size
    pygame.draw.polygon(surface, BROWN, [
        (width//4, height//4),
        (3*width//4, height//4),
        (7*width//8, height//2),
        (width//8, height//2),
    ])
    pygame.draw.polygon(surface, BROWN, [
        (width//8, height//2),
        (7*width//8, height//2),
        (3*width//4, 3*height//4),
        (width//4, 3*height//4),
    ])
    
    # Draw gold coins
    pygame.draw.circle(surface, GOLD, (3*width//8, height//2), width//8)
    pygame.draw.circle(surface, GOLD, (5*width//8, height//2), width//8)
    
    return surface

class TreasureHuntGame(GameBase):
    def __init__(self):
        super().__init__("Treasure Hunt - Closest Pair Algorithm")
        
        # Game state
        self.points = []  # List of treasure points
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.use_brute_force = False
        self.visualization_speed = 1.0  # Seconds per step
        self.step_timer = 0
        
        # Create treasure surface
        self.treasure_img = create_treasure_surface((30, 30))
        
        # Create UI elements
        self.setup_ui()
        
        # Tutorial state
        self.show_tutorial = True
        self.tutorial_step = 0
        self.tutorial_messages = [
            "Welcome to Treasure Hunt! Click anywhere to place treasure markers.",
            "Use the control panel to start the algorithm and adjust visualization speed.",
            "Watch how the divide-and-conquer approach efficiently finds the closest pair!",
            "Red lines show how the plane is divided into smaller regions.",
            "Green circles highlight points being compared.",
            "The blue line connects the current closest pair found.",
            "Try both divide-and-conquer and brute force to see the difference!",
        ]
    
    def setup_ui(self):
        """Create UI elements for the game."""
        # Control panel background
        panel_rect = pygame.Rect(self.width - 250, 0, 250, self.height)
        self.control_panel = pygame_gui.elements.UIPanel(
            relative_rect=panel_rect,
            manager=self.ui_manager
        )
        
        # Buttons
        button_width = 200
        button_height = 40
        spacing = 10
        
        # Start/Stop button
        self.start_button = self.create_button(
            "Start Algorithm",
            pygame.Rect(
                self.width - 225,
                spacing,
                button_width,
                button_height
            )
        )
        
        # Reset button
        self.reset_button = self.create_button(
            "Reset",
            pygame.Rect(
                self.width - 225,
                2 * spacing + button_height,
                button_width,
                button_height
            )
        )
        
        # Algorithm toggle
        self.algorithm_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                self.width - 225,
                3 * spacing + 2 * button_height,
                button_width,
                button_height
            ),
            text="Use Brute Force",
            manager=self.ui_manager
        )
        
        # Speed slider
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                self.width - 225,
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
                self.width - 225,
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
                self.width - 225,
                6 * spacing + 5 * button_height,
                button_width,
                150
            ),
            manager=self.ui_manager
        )
        
        # Stats labels
        self.points_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 215,
                7 * spacing + 5 * button_height,
                button_width - 20,
                25
            ),
            text="Points: 0",
            manager=self.ui_manager
        )
        
        self.distance_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.width - 215,
                8 * spacing + 5 * button_height + 25,
                button_width - 20,
                25
            ),
            text="Min Distance: -",
            manager=self.ui_manager
        )
    
    def handle_event(self, event):
        """Handle game-specific events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left click to add point
            x, y = event.pos
            if x < self.width - 250:  # Not in control panel
                self.points.append(Point(x, y))
                self.points_label.set_text(f"Points: {len(self.points)}")
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # Right click to remove point
            x, y = event.pos
            for point in self.points:
                if math.sqrt((x - point.x)**2 + (y - point.y)**2) < 15:
                    self.points.remove(point)
                    self.points_label.set_text(f"Points: {len(self.points)}")
                    break
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.toggle_algorithm()
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.visualization_speed = min(2.0, self.visualization_speed + 0.1)
            elif event.key == pygame.K_MINUS:
                self.visualization_speed = max(0.1, self.visualization_speed - 0.1)
        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.toggle_algorithm()
            elif event.ui_element == self.reset_button:
                self.reset_game()
            elif event.ui_element == self.algorithm_toggle:
                self.use_brute_force = not self.use_brute_force
                self.algorithm_toggle.set_text(
                    "Use Divide & Conquer" if self.use_brute_force else "Use Brute Force"
                )
        
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.speed_slider:
                self.visualization_speed = event.value
    
    def update(self, time_delta):
        """Update game state."""
        if self.algorithm_running:
            self.step_timer += time_delta
            if self.step_timer >= self.visualization_speed:
                self.step_timer = 0
                self.update_algorithm()
        
        # Update distance label if we have a current pair
        if self.viz_state.current_pair:
            p1, p2 = self.viz_state.current_pair
            dist = p1.distance_to(p2)
            self.distance_label.set_text(f"Min Distance: {dist:.1f}")
        else:
            self.distance_label.set_text("Min Distance: -")
    
    def draw(self):
        """Draw game elements."""
        # Draw grid
        for x in range(0, self.width - 250, 50):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, 50):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.width - 250, y), 1)
        
        # Draw dividing lines
        for line in self.viz_state.dividing_lines:
            x1, y1, x2, y2 = line
            pygame.draw.line(self.screen, self.RED, (x1, y1), (x2, y2), 2)
        
        # Draw strip bounds if present
        if self.viz_state.strip_bounds:
            left, right = self.viz_state.strip_bounds
            pygame.draw.rect(self.screen, (200, 200, 255), 
                           (left, 0, right - left, self.height), 1)
        
        # Draw points being compared
        for point in self.viz_state.current_points:
            pygame.draw.circle(self.screen, self.GREEN, 
                             (int(point.x), int(point.y)), 20, 2)
        
        # Draw current closest pair
        if self.viz_state.current_pair:
            p1, p2 = self.viz_state.current_pair
            pygame.draw.line(self.screen, self.BLUE, 
                           (p1.x, p1.y), (p2.x, p2.y), 2)
        
        # Draw all points (treasures)
        for point in self.points:
            self.screen.blit(
                self.treasure_img,
                (point.x - 15, point.y - 15)
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
        if len(self.points) < 2:
            return
            
        self.algorithm_running = not self.algorithm_running
        if self.algorithm_running:
            self.viz_state = VisualizationState()
            self.start_button.set_text("Stop Algorithm")
        else:
            self.start_button.set_text("Start Algorithm")
    
    def reset_game(self):
        """Reset the game state."""
        self.points = []
        self.viz_state = VisualizationState()
        self.algorithm_running = False
        self.start_button.set_text("Start Algorithm")
        self.points_label.set_text("Points: 0")
        self.distance_label.set_text("Min Distance: -")
    
    def update_algorithm(self):
        """Update algorithm visualization state."""
        if not self.algorithm_running:
            return
            
        # Run appropriate algorithm
        if self.use_brute_force:
            result = brute_force(self.points, self.viz_state)
        else:
            result = closest_pair_recursive(self.points, self.viz_state)
        
        if result:
            self.viz_state.completed = True
            self.algorithm_running = False
            self.start_button.set_text("Start Algorithm")

if __name__ == "__main__":
    game = TreasureHuntGame()
    game.run() 