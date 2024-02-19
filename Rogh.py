from tabulate import tabulate
import random
import math

class MyVacummEnvironment:
    def __init__(instance):
        # Initializes the environment with a grid size and sets the initial state
        instance.size = instance.get_Nsize()  # Size of the grid determined by user input
        instance.grid = [['Clean' for _ in range(instance.size)] for _ in range(instance.size)]  # Initializes all cells as 'Clean'
        instance.add_Waste()  # Adds waste to specified locations
        instance.set_cleaner_start_position()  # Sets the starting position of the cleaner

    def get_Nsize(instance):
        # Asks the user to input the size of the grid and ensures it is within an acceptable range
        while True:
            try:
                n = int(input("\nEnter the Size (N) for the grid (up to 5): "))
                if 0 < n <= 5:
                    return n
                else:
                    print("Please enter a natural number no larger than 5.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def add_Waste(instance):
        # Prompts user for waste locations and adds them to the grid
        while True:
            try:
                waste_locations = input("\nEnter the waste locations as coordinates separated by space (e.g., '1,1 2,1 3,2'): ")
                waste_locations = [tuple(map(int, coord.split(','))) for coord in waste_locations.split()]
                if all(0 < x <= instance.size and 0 < y <= instance.size for x, y in waste_locations):
                    break
                else:
                    print(f"Please enter coordinates within the range (1 to {instance.size}).")
            except ValueError:
                print("Invalid input. Please enter valid coordinates.")
        
        for x, y in waste_locations:
            instance.grid[x-1][y-1] = 'Waste'  # Marks specified locations as 'Waste'

    def set_cleaner_start_position(instance):
        # Sets the cleaner's initial position based on user input
        while True:
            try:
                start_pos = input("\nEnter the cleaner's start position as coordinates (e.g., '1,1'): ")
                start_pos = tuple(map(int, start_pos.split(',')))
                if 0 < start_pos[0] <= instance.size and 0 < start_pos[1] <= instance.size:
                    instance.cleaner_location = (start_pos[0] - 1, start_pos[1] - 1)
                    break
                else:
                    print(f"Please enter coordinates within the range (1 to {instance.size}).")
            except ValueError:
                print("Invalid input. Please enter valid coordinates.")

    def DisplayMyVacummEnvironment(instance):
        # Uses the tabulate library to visually display the grid and cleaner location
        table = [[f"({i+1},{j+1})\n{instance.grid[i][j]}" + (f'\nVacuum' if (i, j) == instance.cleaner_location else '') for j in range(instance.size)] for i in range(instance.size)]
        print(tabulate(table, tablefmt="grid"))

    def find_nearest_waste(instance):
        # Calculates the nearest waste location to the cleaner using Manhattan distance
        x, y = instance.cleaner_location
        nearest_waste = None
        min_distance = math.inf
        for i in range(instance.size):
            for j in range(instance.size):
                if instance.grid[i][j] == 'Waste':
                    distance = abs(i - x) + abs(j - y)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_waste = (i, j)
        return nearest_waste

    def cleaner_action(instance):
        # Determines the next action for the cleaner: clean or move towards the nearest waste
        x, y = instance.cleaner_location
        if instance.grid[x][y] == 'Waste':
            return 'clean'
        else:
            nearest_waste = instance.find_nearest_waste()
            if nearest_waste is None:
                return None  # No action if no waste is found
            nx, ny = nearest_waste
            if nx < x: return 'up'
            if nx > x: return 'down'
            if ny < y: return 'left'
            if ny > y: return 'right'

    def apply_action(instance, action):
        # Applies the specified action and moves the cleaner or cleans the current location
        x, y = instance.cleaner_location
        if action == 'clean':
            instance.grid[x][y] = 'Clean'
            print("Action taken: Clean")
        elif action == 'up':
            instance.cleaner_location = (x - 1, y)
            print("Action taken: Move Up")
        elif action == 'down':
            instance.cleaner_location = (x + 1, y)
            print("Action taken: Move Down")
        elif action == 'left':
            instance.cleaner_location = (x, y - 1)
            print("Action taken: Move Left")
        elif action == 'right':
            instance.cleaner_location = (x, y + 1)
            print("Action taken: Move Right")

    def ISaGoalState(instance):
        # Checks if all cells in the grid are clean, indicating the goal state has been reached
        return all(all(cell == 'Clean' for cell in row) for row in instance.grid)

    def StartCleaning(instance):
        # Initiates the cleaning process and continues until the goal state is reached
        steps = 0
        while not instance.ISaGoalState():
            action = instance.cleaner_action()
            if action:
                instance.apply_action(action)
                steps += 1
            instance.DisplayMyVacummEnvironment()  # To visualize the process
        print(f"\nCleaning completed in {steps} steps.")

# Runing the environment
env = MyVacummEnvironment()
env.DisplayMyVacummEnvironment()
env.StartCleaning()