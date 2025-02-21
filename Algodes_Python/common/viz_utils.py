import pygame
import math

def draw_arrow(surface, start_pos, end_pos, color, width=2, arrow_size=10):
    """
    Draw an arrow from start_pos to end_pos.
    
    Args:
        surface: Pygame surface to draw on
        start_pos (tuple): Starting position (x, y)
        end_pos (tuple): Ending position (x, y)
        color (tuple): RGB color tuple
        width (int): Line width
        arrow_size (int): Size of arrow head
    """
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    
    # Calculate arrow head
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    arrow_p1 = (
        end_pos[0] - arrow_size * math.cos(angle - math.pi/6),
        end_pos[1] - arrow_size * math.sin(angle - math.pi/6)
    )
    arrow_p2 = (
        end_pos[0] - arrow_size * math.cos(angle + math.pi/6),
        end_pos[1] - arrow_size * math.sin(angle + math.pi/6)
    )
    
    pygame.draw.polygon(surface, color, [end_pos, arrow_p1, arrow_p2])

def draw_dashed_line(surface, start_pos, end_pos, color, width=1, dash_length=10):
    """
    Draw a dashed line from start_pos to end_pos.
    
    Args:
        surface: Pygame surface to draw on
        start_pos (tuple): Starting position (x, y)
        end_pos (tuple): Ending position (x, y)
        color (tuple): RGB color tuple
        width (int): Line width
        dash_length (int): Length of each dash
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx * dx + dy * dy)
    dashes = int(distance / (2 * dash_length))
    
    cos_angle = dx / distance
    sin_angle = dy / distance
    
    for i in range(dashes):
        start = (
            x1 + (2 * i * dash_length) * cos_angle,
            y1 + (2 * i * dash_length) * sin_angle
        )
        end = (
            x1 + (2 * i * dash_length + dash_length) * cos_angle,
            y1 + (2 * i * dash_length + dash_length) * sin_angle
        )
        pygame.draw.line(surface, color, start, end, width)

def create_tooltip(text, font_size=20, padding=5, bg_color=(255, 255, 220), text_color=(0, 0, 0)):
    """
    Create a tooltip surface with text.
    
    Args:
        text (str): Tooltip text
        font_size (int): Font size
        padding (int): Padding around text
        bg_color (tuple): RGB color tuple for background
        text_color (tuple): RGB color tuple for text
        
    Returns:
        surface: Pygame surface containing the tooltip
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, text_color)
    
    # Create surface with padding
    width = text_surface.get_width() + 2 * padding
    height = text_surface.get_height() + 2 * padding
    surface = pygame.Surface((width, height))
    
    # Fill background
    surface.fill(bg_color)
    
    # Add text
    surface.blit(text_surface, (padding, padding))
    
    # Add border
    pygame.draw.rect(surface, text_color, surface.get_rect(), 1)
    
    return surface

def draw_progress_bar(surface, pos, size, progress, color, bg_color=(200, 200, 200)):
    """
    Draw a progress bar.
    
    Args:
        surface: Pygame surface to draw on
        pos (tuple): Top-left position (x, y)
        size (tuple): Width and height of bar
        progress (float): Progress value between 0 and 1
        color (tuple): RGB color tuple for progress
        bg_color (tuple): RGB color tuple for background
    """
    x, y = pos
    width, height = size
    
    # Draw background
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    
    # Draw progress
    progress_width = int(width * max(0, min(1, progress)))
    if progress_width > 0:
        pygame.draw.rect(surface, color, (x, y, progress_width, height))
    
    # Draw border
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 1)

def draw_grid(surface, cell_size, color=(200, 200, 200)):
    """
    Draw a grid on the surface.
    
    Args:
        surface: Pygame surface to draw on
        cell_size (int): Size of each grid cell
        color (tuple): RGB color tuple for grid lines
    """
    width = surface.get_width()
    height = surface.get_height()
    
    # Draw vertical lines
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    
    # Draw horizontal lines
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, color, (0, y), (width, y)) 