# Delivery Rush - Minimizing Lateness Algorithm Visualization

This interactive game demonstrates the Greedy Algorithm approach for minimizing maximum lateness in scheduling problems. The algorithm has an optimal O(n log n) time complexity and provides a simple yet effective solution for scheduling tasks with deadlines.

## Algorithm Overview

The Greedy Algorithm for minimizing maximum lateness works as follows:

1. Sort all tasks by their deadlines (Earliest Deadline First - EDF)
2. Schedule tasks in this order, starting at time 0
3. For each task, calculate its lateness (completion time - deadline)
4. The maximum lateness across all tasks is minimized

### Key Concepts Visualized

- **Sorting**: Watch tasks being sorted by deadline
- **Scheduling**: See how tasks are assigned in sequence
- **Lateness**: Visual representation of each task's lateness
- **Optimality**: Proof that this simple approach is optimal

## How to Play

1. Add delivery tasks with:
   - Processing time (how long the delivery takes)
   - Deadline (when it needs to be delivered by)
   - Priority (optional, for visualization)
2. Use the control panel to:
   - Start the scheduling algorithm
   - Control visualization speed
   - Add/remove tasks
3. Watch the algorithm in action:
   - Tasks being sorted by deadline
   - Drone assignments and routes
   - Real-time lateness calculations
   - Final schedule visualization

## Educational Features

- Step-by-step visualization of the scheduling process
- Real-time lateness calculations
- Visual proof of optimality
- Interactive task creation and modification
- Detailed explanations of each step

## Controls

- Add Task: Click the "Add Task" button
- Remove Task: Right-click on a task
- Start/Stop: Space or Start button
- Reset: R key or Reset button
- Speed Control: +/- keys or slider

## Task Types

The game includes themed delivery tasks such as:
- "Hot Pizza Delivery" (short processing time, tight deadline)
- "Medical Supplies" (medium processing time, critical deadline)
- "Regular Package" (longer processing time, flexible deadline)
- "Express Mail" (short processing time, moderate deadline)

Each task type has unique visual representation and characteristics to make the learning experience more engaging. 