# Treasure Hunt - Closest Pair Algorithm Visualization

This interactive game demonstrates the Divide and Conquer algorithm for finding the closest pair of points in a 2D plane. The algorithm has an efficient O(n log n) time complexity, compared to the naive O(n²) approach.

## Algorithm Overview

The Divide and Conquer approach for finding the closest pair works as follows:

1. Sort points by x-coordinate
2. Divide points into two halves
3. Recursively find closest pairs in each half
4. Find closest pair that crosses the dividing line
5. Return the minimum of all found distances

### Key Concepts Visualized

- **Divide**: The game shows how the plane is divided vertically into regions
- **Conquer**: Each sub-region's closest pair is highlighted
- **Combine**: The algorithm checks points near the dividing line
- **Efficiency**: Visual comparison with brute force approach

## How to Play

1. Click anywhere on the map to place treasure markers
2. Use the control panel to:
   - Start the algorithm visualization
   - Control visualization speed
   - Toggle between divide-and-conquer and brute force approaches
3. Watch the algorithm in action:
   - Red lines show the dividing process
   - Green circles highlight points being compared
   - Blue lines connect the current closest pair
   - Yellow highlight shows the final result

## Educational Features

- Step-by-step visualization of the algorithm
- Real-time distance calculations
- Comparison with brute force approach
- Interactive tooltips explaining each step
- Visual proof of correctness

## Controls

- Left Click: Place treasure marker
- Right Click: Remove treasure marker
- Space: Start/Pause visualization
- R: Reset game
- +/-: Adjust visualization speed 