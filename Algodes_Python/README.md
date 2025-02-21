# Algodes_Python: Interactive Algorithm Learning Through Games

This repository contains three interactive games that teach fundamental algorithms through engaging visualizations and gameplay. Each game is designed to demonstrate a specific algorithmic concept while providing an enjoyable learning experience.

## Games Included

### 1. Treasure Hunt (Divide and Conquer - Closest Pair)
Find the closest pair of treasures on a map using the divide and conquer algorithm. Watch as the algorithm recursively divides the map and efficiently finds the closest treasures.

### 2. Delivery Rush (Greedy Algorithm - Minimizing Lateness)
Manage a drone delivery service by scheduling deliveries to minimize maximum lateness. Experience how a greedy approach can lead to optimal solutions in scheduling problems.

### 3. Dungeon Loot Manager (Dynamic Programming - Knapsack Problem)
Optimize your loot collection in a dungeon by solving the classic knapsack problem. Visualize how dynamic programming builds solutions to complex optimization problems.

## Requirements
- Python 3.8+
- Pygame
- Additional requirements listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BlacktPearl/Algodes/Algodes_Python.git
cd Algodes_Python
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Games

Each game can be run independently from its respective directory:

1. Treasure Hunt:
```bash
python treasure_hunt/main.py
```

2. Delivery Rush:
```bash
python delivery_rush/main.py
```

3. Dungeon Loot:
```bash
python dungeon_loot/main.py
```

## Project Structure
```
Algodes_Python/
├── common/             # Common utilities and shared components
├── treasure_hunt/      # Closest Pair visualization game
├── delivery_rush/      # Minimizing Lateness visualization game
└── dungeon_loot/      # Knapsack Problem visualization game
```

## Educational Goals

Each game is designed with the following educational principles:
- Visual demonstration of algorithm steps
- Interactive learning through gameplay
- Detailed explanations and annotations
- Real-time visualization of algorithm progress
- Comprehensive documentation and comments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
