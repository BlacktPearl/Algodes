"""
Implementation of the Dynamic Programming solution to the 0/1 Knapsack Problem.
Includes visualization state tracking for educational purposes.
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum, auto

class ItemType(Enum):
    """Types of dungeon items with different characteristics."""
    GOLDEN_CHALICE = auto()  # High value, medium weight
    ANCIENT_SCROLL = auto()  # High value, low weight
    IRON_SWORD = auto()      # Medium value, high weight
    HEALTH_POTION = auto()   # Low value, low weight
    DRAGON_SCALE = auto()    # Very high value, very high weight

@dataclass
class Item:
    """Represents a dungeon item with weight and value."""
    name: str
    weight: int
    value: int
    item_type: ItemType
    
    def __hash__(self):
        """Make Item hashable for use in sets."""
        return hash((self.name, self.weight, self.value, self.item_type))
    
    def __eq__(self, other):
        """Define equality for Item objects."""
        if not isinstance(other, Item):
            return False
        return (self.name == other.name and
                self.weight == other.weight and
                self.value == other.value and
                self.item_type == other.item_type)

class VisualizationState:
    """Tracks the current state of algorithm visualization."""
    def __init__(self):
        self.dp_table: List[List[int]] = []  # Dynamic programming table
        self.current_cell: Optional[Tuple[int, int]] = None  # Current cell being computed
        self.selected_items: Set[Item] = set()  # Items selected in current solution
        self.current_weight = 0  # Current weight being considered
        self.current_value = 0  # Current value being considered
        self.backtracking = False  # Whether we're in backtracking phase
        self.completed = False
        self.step_description = ""
        
        # For animating table fill
        self.table_fill_position = (0, 0)  # Current position in table fill animation
        self.highlighted_cells: List[Tuple[int, int]] = []  # Cells to highlight
        self.comparison_values: Optional[Tuple[int, int]] = None  # Values being compared

def get_item_color(item_type: ItemType) -> Tuple[int, int, int]:
    """Get the display color for an item type."""
    colors = {
        ItemType.GOLDEN_CHALICE: (255, 215, 0),     # Gold
        ItemType.ANCIENT_SCROLL: (255, 255, 200),    # Parchment
        ItemType.IRON_SWORD: (192, 192, 192),       # Silver
        ItemType.HEALTH_POTION: (255, 0, 0),        # Red
        ItemType.DRAGON_SCALE: (50, 205, 50),       # Green
    }
    return colors[item_type]

def get_default_stats(item_type: ItemType) -> Tuple[int, int]:
    """Get the default weight and value for an item type."""
    stats = {
        ItemType.GOLDEN_CHALICE: (5, 10),    # Medium weight, high value
        ItemType.ANCIENT_SCROLL: (1, 8),     # Low weight, high value
        ItemType.IRON_SWORD: (8, 6),         # High weight, medium value
        ItemType.HEALTH_POTION: (2, 3),      # Low weight, low value
        ItemType.DRAGON_SCALE: (10, 15),     # Very high weight, very high value
    }
    return stats[item_type]

def get_item_description(item_type: ItemType) -> str:
    """Get a description of the item type."""
    descriptions = {
        ItemType.GOLDEN_CHALICE: "A valuable golden chalice, somewhat heavy but worth the effort",
        ItemType.ANCIENT_SCROLL: "A lightweight scroll containing powerful magic",
        ItemType.IRON_SWORD: "A heavy iron sword, useful but weighs you down",
        ItemType.HEALTH_POTION: "A small health potion, light but not very valuable",
        ItemType.DRAGON_SCALE: "A massive dragon scale, extremely heavy but incredibly valuable",
    }
    return descriptions[item_type]

def solve_knapsack(items: List[Item], capacity: int, viz_state: VisualizationState) -> int:
    """
    Solve the 0/1 Knapsack Problem using dynamic programming.
    Updates visualization state for educational purposes.
    
    Args:
        items: List of items to choose from
        capacity: Maximum weight capacity
        viz_state: Current visualization state to update
        
    Returns:
        Maximum value achievable within weight constraint
    """
    n = len(items)
    
    # Initialize DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    viz_state.dp_table = dp
    
    # Fill DP table
    for i in range(1, n + 1):
        item = items[i - 1]
        for w in range(capacity + 1):
            # Update visualization state
            viz_state.current_cell = (i, w)
            viz_state.current_weight = w
            viz_state.table_fill_position = (i, w)
            
            if item.weight > w:
                # Item too heavy for current capacity
                dp[i][w] = dp[i - 1][w]
                viz_state.step_description = (
                    f"{item.name} is too heavy (weight {item.weight}) "
                    f"for current capacity {w}"
                )
                viz_state.comparison_values = None
            else:
                # Compare including vs excluding item
                exclude_value = dp[i - 1][w]
                include_value = dp[i - 1][w - item.weight] + item.value
                
                viz_state.comparison_values = (exclude_value, include_value)
                viz_state.highlighted_cells = [
                    (i - 1, w),                    # Cell for excluding
                    (i - 1, w - item.weight)       # Cell for including
                ]
                
                if include_value > exclude_value:
                    dp[i][w] = include_value
                    viz_state.step_description = (
                        f"Including {item.name} gives better value "
                        f"({include_value} > {exclude_value})"
                    )
                else:
                    dp[i][w] = exclude_value
                    viz_state.step_description = (
                        f"Excluding {item.name} gives better value "
                        f"({exclude_value} ≥ {include_value})"
                    )
    
    # Backtrack to find selected items
    viz_state.backtracking = True
    viz_state.step_description = "Backtracking to find selected items"
    
    w = capacity
    selected = set()
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item = items[i - 1]
            selected.add(item)
            w -= item.weight
            
            viz_state.selected_items = selected
            viz_state.current_cell = (i, w)
            viz_state.step_description = f"Selected {item.name}"
    
    viz_state.completed = True
    return dp[n][capacity] 