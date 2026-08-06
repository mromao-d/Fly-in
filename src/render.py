import pygame
import math
from typing import Any
from .algo import Algo
from .hubs import ZoneType
from .read_confs import ReadConfs


class RenderMap:
    """
    class that renders the map
    Uses pgame
    """
    def __init__(
        self,
        ReadConfs: ReadConfs,
        debug: bool = False
    ):
        """
        initiates the class

        Args:
            confs (ReadConfs)
            debug (bool): possibility to print more stuff if needed
        """
        self.confs = ReadConfs
        self.grid_size = ReadConfs.grid_size
        self.debug = debug
        self.run()

    def handle_events(self) -> bool:
        """
        handles quit for exiting pygame

        returns:
            bool, to stop running the loop
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    @staticmethod
    def render_txt(
        font: Any,
        txt: str,
        color: tuple[int, int, int],
        xy: tuple[float, float],
        screen: Any
    ) -> None:
        """
        function to render text using pygame

        Args:
            font (Any): SysFont for pygame
            txt (str): text to display
            color(tuple[int, int, int]): color to be displayed
            xy (tuple[int, int]): position
            screen(Any): game screen
        """
        text = font.render(txt, True, color)
        text_rect = text.get_rect(center=xy)

        screen.blit(text, text_rect)

        return None

    @staticmethod
    def draw_arrow(
        screen: Any,
        color: tuple[int, int, int],
        start: tuple[float, float],
        end: tuple[float, float],
        radius
    ) -> None:
        """
        function to draw arrows between Hubs

        Args:
            font (Any): SysFont for pygame
            txt (str): text to display
            color(tuple[int, int, int]): color to be displayed
            start (tuple[int, int]): start position
            end (tuple[int, int]): end position
            screen(Any): game screen
        """
        angle = math.atan2(end[1] - start[1], end[0] - start[0])

        # Move the arrow tip back to the edge of the circle
        end = (
            end[0] - radius * math.cos(angle),
            end[1] - radius * math.sin(angle),
        )

        pygame.draw.line(screen, color, start, end, 2)

        arrow_length = int(radius / 2)
        arrow_angle = math.radians(30)

        left = (
            end[0] - arrow_length * math.cos(angle - arrow_angle),
            end[1] - arrow_length * math.sin(angle - arrow_angle),
        )

        right = (
            end[0] - arrow_length * math.cos(angle + arrow_angle),
            end[1] - arrow_length * math.sin(angle + arrow_angle),
        )

        pygame.draw.polygon(screen, color, [end, left, right])

        return None

    def run(self) -> None:
        """
        function That renders the map
        it also solves the puzzle as the program runs

        Args:
            None
        """

        pygame.init()
        WIDTH_main, HEIGHT_main = 1600, 900
        WIDTH = WIDTH_main - 100
        HEIGHT = HEIGHT_main - 100
        radius = 20
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont("Name", 15)
        running = True
        di = Algo(self.confs)

        drone_img = pygame.image.load(
            "./src/img/drone.png"
        ).convert_alpha()
        drone_img = pygame.transform.scale(drone_img, (50, 50))

        rest_img = pygame.image.load(
            "./src/img/rest.png"
        ).convert_alpha()
        rest_img = pygame.transform.scale(rest_img, (30, 30))

        pr_img = pygame.image.load(
            "./src/img/priority.png"
        ).convert_alpha()
        pr_img = pygame.transform.scale(pr_img, (30, 30))

        bl_img = pygame.image.load(
            "./src/img/blocked.png"
        ).convert_alpha()
        bl_img = pygame.transform.scale(bl_img, (30, 30))

        total_cost = 0

        while running:
            WIDTH, HEIGHT = screen.get_size()
            running = self.handle_events()
            screen.fill((255, 255, 255))

            for hub in self.confs.hubs:
                hub_x = (hub.coord[0] + 1) * (WIDTH / (self.grid_size[0] + 2))
                hub_y = (hub.coord[1] + 1) * (HEIGHT / (self.grid_size[1] + 2))

                for f_node in hub.conn_nodes:
                    f_x = (
                        (f_node.coord[0] + 1)
                        * (WIDTH / (self.grid_size[0] + 2))
                    )
                    f_y = (
                        (f_node.coord[1] + 1)
                        * (HEIGHT / (self.grid_size[1] + 2))
                    )

                    pygame.draw.line(
                        screen,
                        (0, 0, 0),
                        (hub_x, hub_y),
                        (f_x, f_y)
                    )

                    self.draw_arrow(
                        screen,
                        (0, 0, 0),
                        (hub_x, hub_y),
                        (f_x, f_y),
                        radius
                    )

                pygame.draw.circle(
                    screen,
                    pygame.Color(hub.color),
                    (hub_x, hub_y),
                    radius
                )
                if self.debug is True:
                    self.render_txt(
                        font,
                        hub.hub_name,
                        (0, 0, 0),
                        (hub_x, hub_y),
                        screen
                    )

                    self.render_txt(
                        font,
                        f"max_drones: {str(hub.max_drones)}",
                        (0, 0, 0),
                        (hub_x, hub_y - 40),
                        screen
                    )

                if hub.zone == ZoneType.restricted:
                    screen.blit(rest_img, (hub_x + 10, hub_y + 10))

                if hub.zone == ZoneType.priority:
                    screen.blit(pr_img, (hub_x + 10, hub_y + 10))

                if hub.zone == ZoneType.blocked:
                    screen.blit(bl_img, (hub_x + 10, hub_y + 10))

                arest = 20

            for i, drone in enumerate(self.confs.all_drones):
                drone_x = (
                    (drone.curr_coord[0] + 1)
                    * (WIDTH / (self.grid_size[0] + 2))
                )

                drone_y = (
                    (drone.curr_coord[1] + 1)
                    * (HEIGHT / (self.grid_size[1] + 2))
                )

                screen.blit(drone_img, (drone_x, drone_y))

                text = font.render(f"D{drone.id}", True, "black")
                text_rect = text.get_rect(
                    center=(drone_x + arest / 2, drone_y + arest / 2)
                )
                screen.blit(text, text_rect)

            if self.debug is True:
                self.render_txt(
                    font,
                    f"max_drones: {str(hub.max_drones)}",
                    (0, 0, 0),
                    (drone.curr_coord[0], drone.curr_coord[1] - 40),
                    screen
                )

            if not any(drone.moving for drone in self.confs.all_drones):
                simulation_turns, drones_moved = di.walk()

            for drone in self.confs.all_drones:
                drone.move()

            total_cost = sum([_.conn_turns for _ in self.confs.all_drones])
            self.render_txt(
                pygame.font.SysFont("Path Cost", 35),
                f"total path cost: {total_cost}",
                (0, 0, 0),
                (WIDTH - 150, HEIGHT - 100),
                screen
            )

            self.render_txt(
                pygame.font.SysFont("Drones Moved", 35),
                f"drones moved: {drones_moved}",
                (0, 0, 0),
                (WIDTH - 150, HEIGHT - 70),
                screen
            )

            self.render_txt(
                pygame.font.SysFont("Simulation Turns", 35),
                f"simulation turns: {simulation_turns}",
                (0, 0, 0),
                (WIDTH - 150, HEIGHT - 40),
                screen
            )

            pygame.display.flip()

        pygame.quit()
