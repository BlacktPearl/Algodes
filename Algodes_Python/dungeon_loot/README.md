# Dungeon Loot Manager - Knapsack Problem Visualization

This interactive game demonstrates the Dynamic Programming solution to the 0/1 Knapsack Problem through a dungeon looting scenario. The algorithm efficiently determines the optimal selection of items to maximize value while respecting a weight constraint.

## Algorithm Overview

The Dynamic Programming approach to the Knapsack Problem works as follows:

1. Create a table of size (n+1) × (W+1), where n is the number of items and W is the weight capacity
2. Fill the table using the recurrence relation:
   - If item i's weight > current capacity w: dp[i][w] = dp[i-1][w]
   - Otherwise: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])
3. Backtrack through the table to find the selected items

### Key Concepts Visualized

- **Table Building**: Watch the DP table being filled cell by cell
- **Decision Making**: See how the algorithm decides between including or excluding each item
- **Optimal Substructure**: Understand how solutions to subproblems combine
- **Space/Time Tradeoff**: Compare with recursive and other approaches

## How to Play

1. Add items to the dungeon with:
   - Weight (how heavy the item is)
   - Value (how valuable the item is)
   - Type (affects visual representation)
2. Set the knapsack capacity (maximum weight)
3. Use the control panel to:
   - Start the algorithm visualization
   - Control visualization speed
   - Toggle between different visualization modes
4. Watch the algorithm in action:
   - DP table being filled
   - Current optimal value calculation
   - Selected items being highlighted
   - Backtracking process visualization

## Educational Features

- Step-by-step visualization of DP table construction
- Clear explanation of each decision
- Visual comparison of different solutions
- Interactive item management
- Detailed annotations and tooltips

## Controls

- Add Item: Click the "Add Item" button
- Remove Item: Right-click on an item
- Start/Stop: Space or Start button
- Reset: R key or Reset button
- Speed Control: +/- keys or slider

## Item Types

The game includes themed dungeon items such as:
- "Golden Chalice" (high value, medium weight)
- "Ancient Scroll" (high value, low weight)
- "Iron Sword" (medium value, high weight)
- "Health Potion" (low value, low weight)
- "Dragon Scale" (very high value, very high weight)

Each item type has unique visual representation and characteristics to make the learning experience more engaging. 