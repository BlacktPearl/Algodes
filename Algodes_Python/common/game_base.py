import pygame
import pygame_gui
from abc import ABC, abstractmethod

class GameBase(ABC):
    """
    Base class for all algorithm visualization games.
    Provides common functionality for game initialization, event handling,
    and visualization components.
    """
    
    def __init__(self, title, width=1024, height=768):
        """
        Initialize the game window and basic components.
        
        Args:
            title (str): Window title
            width (int): Window width in pixels
            height (int): Window height in pixels
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Initialize UI manager for better UI elements
        self.ui_manager = pygame_gui.UIManager((width, height))
        
        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        # Game state
        self.running = True
        self.paused = False
        
    def run(self):
        """Main game loop."""
        while self.running:
            time_delta = self.clock.tick(self.fps)/1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.ui_manager.process_events(event)
                self.handle_event(event)
            
            # Update game state
            self.ui_manager.update(time_delta)
            self.update(time_delta)
            
            # Draw frame
            self.screen.fill(self.WHITE)
            self.draw()
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()
        
        pygame.quit()
    
    @abstractmethod
    def handle_event(self, event):
        """
        Handle game-specific events.
        
        Args:
            event: Pygame event object
        """
        pass
    
    @abstractmethod
    def update(self, time_delta):
        """
        Update game state.
        
        Args:
            time_delta (float): Time since last frame in seconds
        """
        pass
    
    @abstractmethod
    def draw(self):
        """Draw game elements on the screen."""
        pass
    
    def draw_text(self, text, position, color=None, size=32, centered=True):
        """
        Draw text on the screen.
        
        Args:
            text (str): Text to draw
            position (tuple): (x, y) position
            color (tuple): RGB color tuple
            size (int): Font size
            centered (bool): Whether to center the text at the position
        """
        if color is None:
            color = self.BLACK
            
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        
        if centered:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)
            
        self.screen.blit(text_surface, text_rect)
    
    def create_button(self, text, rect, callback=None):
        """
        Create a UI button.
        
        Args:
            text (str): Button text
            rect (pygame.Rect): Button rectangle
            callback (callable, optional): Function to call when button is pressed
            
        Returns:
            pygame_gui.elements.UIButton: The created button
        """
        return pygame_gui.elements.UIButton(
            relative_rect=rect,
            text=text,
            manager=self.ui_manager
        ) 