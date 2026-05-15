import pygame
import sys

# Color 
EMPTY_COLOR = (230, 230, 230)
GRID_COLOR = (180, 180, 180)

# Role-based colors
PREDATOR_COLOR = (0, 0, 250)      # red
PREY_COLOR = (120, 255, 120)      # green (255, 120, 120)  # red
TERRAIN = (120, 255, 120)         # green (255, 120, 120)  # red
DEFAULT_COLOR = (150, 150, 200)   # fallback

class GridUI:
    MIN_WIN_SIZE = 250

    def __init__(self, grid, cell_size=25, fps=15):
        pygame.init()
        self.grid = grid
        self.cell_size = cell_size
        self.fps = fps
        self.flag_redraw = True

        # Calculate initial window size
        w = max(self.MIN_WIN_SIZE, grid.width * cell_size)
        h = max(self.MIN_WIN_SIZE, grid.height * cell_size)

        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        pygame.display.set_caption("Ecosystem Grid")

        self.font = pygame.font.SysFont("Arial", 12, bold=True)
        self.clock = pygame.time.Clock()

    # Resize window when grid expands (for infinite grids)
    def resize(self):
        w = max(self.MIN_WIN_SIZE, self.grid.width * self.cell_size)
        h = max(self.MIN_WIN_SIZE, self.grid.height * self.cell_size)

        screen = pygame.display.get_surface()
        if screen.get_width() != w or screen.get_height() != h:
            self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    # Draw - grid cells and organisms
    def draw_grid(self):
        """Draw grid cells and organisms."""
        self.screen.fill(EMPTY_COLOR)

        drawn = set() 

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Draw background cell
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, EMPTY_COLOR, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

                organisms = self.grid.get_cell(x, y)

                if not organisms:
                    continue

                for org in organisms:
                    if org in drawn:
                        continue

                    # Only draw once 
                    if org.x == x and org.y == y:
                        if hasattr(org, "role"):
                            if org.role and org.role.lower() == "predator":
                                color = PREDATOR_COLOR
                            elif org.role and org.role.lower() == "prey":
                                color = PREY_COLOR
                            else:
                                color = DEFAULT_COLOR
                        else:
                            color = DEFAULT_COLOR

                        # Draw footprint cell by cell
                        for dx in range(org.width):
                            for dy in range(org.height):
                                footprint_rect = pygame.Rect(
                                    (org.x + dx) * self.cell_size,
                                    (org.y + dy) * self.cell_size,
                                    self.cell_size,
                                    self.cell_size
                                )
                                pygame.draw.rect(self.screen, color, footprint_rect)
                                pygame.draw.rect(self.screen, GRID_COLOR, footprint_rect, 2)

                        # Draw label once
                        # label = self.font.render(org.name, True, (0, 0, 0))
                        # self.screen.blit(label, (org.x * self.cell_size + 1, org.y * self.cell_size + 1))

                        # DEBUGGING in terminal
                        # drawn.add(org)
                        # print(f"{org.name} at ({org.x},{org.y}) size=({org.width}x{org.height})")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.resize()
            
            self.draw_grid()

            pygame.display.flip()
            self.clock.tick(self.fps)
