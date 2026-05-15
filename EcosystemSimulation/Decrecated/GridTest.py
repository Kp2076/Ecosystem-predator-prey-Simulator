import threading
import random
import time

from Decrecated.FiniteGrid import FiniteGrid
from Decrecated.InfiniteGrid import InfiniteGrid
from UI.GridUI import GridUI
from Tests.Sample.EntitiesSample import create_animal_test
from Tests.Sample.GameSample import Game

# def terminal_initial_addition(sim, grid, ui):
#     print("\nEnter animal name.")
#     print("Predator = RED | Prey = GREEN")
#     print("Available: lion, wolf, deer, rabbit\n")

#     name = input(">> ").strip().lower()
#     if not name.isalpha():
#         print("Incorrect input")
#         return

#     animal = create_animal_test(name)
#     if animal is None:
#         print("Unknown animal. Try: lion, wolf, deer, rabbit")
#         return  

#     max_x = max(0, grid.width - animal.width)
#     max_y = max(0, grid.height - animal.height)
#     if max_x < 0 or max_y < 0:
#         print("Grid too small for that animal.")
#         return

#     x = random.randint(0, max_x)
#     y = random.randint(0, max_y)
#     grid.set_cell(animal, x, y)
#     sim.add_entity(animal)
#     ui.flag_redraw = True
#     print(f"Added {name} at ({x}, {y})")

# def terminal_loop(sim, grid, ui):
#     while True:
#         name = input("\nAdd another animal: ").strip().lower()
#         if not name.isalpha():
#             print("Incorrect input")
#             continue

#         animal = create_animal_test(name)
#         if animal is None:
#             print("Unknown animal")
#             continue

#         max_x = max(0, grid.width - animal.width)
#         max_y = max(0, grid.height - animal.height)
#         if max_x >= 0 and max_y >= 0:
#             x = random.randint(0, max_x)
#             y = random.randint(0, max_y)
#             grid.set_cell(animal, x, y)
#             sim.add_entity(animal)
#             ui.flag_redraw = True
#             print(f"Added {name} at ({x}, {y})")
#         else:
#             print("Could not place animal.")

def main():
    # print("=" * 50)
    # print("ECOSYSTEM SIMULATION")
    # print("=" * 50)
    # print("\nChoose grid type:")
    # print("  [f] Finite Grid")
    # print("  [i] Infinite Grid")
    
    # mode = input("\n>> ").strip().lower()
    w = int(75)
    h = int(30)

    # if mode == "f":
    grid = FiniteGrid(w, h)
    print(f"\nCreated {w}x{h} FINITE grid")
    # else:
    #     grid = InfiniteGrid(w, h)
    #     print(f"\nCreated {w}x{h} INFINITE grid")
    #     print(f"Max wall hits before direction change: {InfiniteGrid.MAX_WALL_HITS}")

    ui = GridUI(grid, cell_size=14, fps=7)
    sim = Game(grid, ui)

    # terminal_initial_addition(sim, grid, ui)
    name = ["lion", "wolf", "rabbit", "deer"]
    animal = create_animal_test(name) 

    max_x = max(0, grid.width - animal.width)
    max_y = max(0, grid.height - animal.height)

    x = random.randint(0, max_x)
    y = random.randint(0, max_y)
    grid.set_cell(animal, x, y)
    sim.add_entity(animal)
    ui.flag_redraw = True

    threading.Thread(target=sim.run_loop, daemon=True).start()
    # threading.Thread(target=terminal_loop, args=(sim, grid, ui), daemon=True).start()

    ui.run()

if __name__ == "__main__":
    main()
