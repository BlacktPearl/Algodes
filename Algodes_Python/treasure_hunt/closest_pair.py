"""
Implementation of the Divide and Conquer algorithm for finding the closest pair of points.
This module contains both the algorithm implementation and visualization state tracking.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Point:
    """Represents a point (treasure) in 2D space."""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

@dataclass
class ClosestPairResult:
    """Stores the result of a closest pair calculation."""
    point1: Point
    point2: Point
    distance: float

class VisualizationState:
    """Tracks the current state of algorithm visualization."""
    def __init__(self):
        self.dividing_lines: List[Tuple[float, float, float, float]] = []  # (x1, y1, x2, y2)
        self.current_points: List[Point] = []  # Points being compared
        self.current_pair: Optional[Tuple[Point, Point]] = None  # Current closest pair
        self.strip_bounds: Optional[Tuple[float, float]] = None  # Bounds of strip around divide
        self.completed = False
        self.step_description = ""

def closest_pair_recursive(points: List[Point], viz_state: VisualizationState) -> ClosestPairResult:
    """
    Find the closest pair of points using divide and conquer.
    
    Args:
        points: List of points to process
        viz_state: Current visualization state to update
        
    Returns:
        ClosestPairResult containing the closest pair and their distance
    """
    n = len(points)
    
    # Base cases
    if n <= 1:
        return None
    if n == 2:
        dist = points[0].distance_to(points[1])
        return ClosestPairResult(points[0], points[1], dist)
    
    # Sort points by x coordinate
    points_sorted = sorted(points, key=lambda p: p.x)
    mid = n // 2
    mid_x = points_sorted[mid].x
    
    # Add dividing line to visualization
    viz_state.dividing_lines.append((mid_x, 0, mid_x, 1000))  # Assuming 1000 is max height
    
    # Recursively solve left and right halves
    left_result = closest_pair_recursive(points_sorted[:mid], viz_state)
    right_result = closest_pair_recursive(points_sorted[mid:], viz_state)
    
    # Find minimum distance from recursive results
    if left_result is None:
        min_result = right_result
    elif right_result is None:
        min_result = left_result
    else:
        min_result = left_result if left_result.distance < right_result.distance else right_result
    
    if min_result is None:
        return None
    
    # Find points in strip around dividing line
    strip_width = min_result.distance
    strip_points = [p for p in points_sorted 
                   if abs(p.x - mid_x) < strip_width]
    
    # Update visualization state for strip
    viz_state.strip_bounds = (mid_x - strip_width, mid_x + strip_width)
    
    # Check points in strip
    strip_points.sort(key=lambda p: p.y)  # Sort by y coordinate
    for i in range(len(strip_points)):
        # Only need to check 7 points ahead (proof in algorithm analysis)
        for j in range(i + 1, min(i + 8, len(strip_points))):
            # Update visualization state
            viz_state.current_points = [strip_points[i], strip_points[j]]
            
            dist = strip_points[i].distance_to(strip_points[j])
            if dist < min_result.distance:
                min_result = ClosestPairResult(strip_points[i], strip_points[j], dist)
                viz_state.current_pair = (strip_points[i], strip_points[j])
    
    return min_result

def brute_force(points: List[Point], viz_state: VisualizationState) -> ClosestPairResult:
    """
    Find closest pair using brute force approach (for comparison).
    
    Args:
        points: List of points to process
        viz_state: Current visualization state to update
        
    Returns:
        ClosestPairResult containing the closest pair and their distance
    """
    if len(points) < 2:
        return None
        
    min_dist = float('inf')
    result = None
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # Update visualization state
            viz_state.current_points = [points[i], points[j]]
            
            dist = points[i].distance_to(points[j])
            if dist < min_dist:
                min_dist = dist
                result = ClosestPairResult(points[i], points[j], dist)
                viz_state.current_pair = (points[i], points[j])
    
    return result 