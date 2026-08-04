import pygame
import math
from typing import Any
from algo import Algo
from hubs import ZoneType


class RenderMap:
    def __init__(
        self,
        ReadConfs,
        debug: bool = False
    ):
        self.confs = ReadConfs
        self.grid_size = ReadConfs.grid_size
        self.debug = debug
        self.run()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    @staticmethod
    def render_txt(
        font: Any,
        txt: str,
        color: tuple[int, int, int],
        xy: tuple[int, int],
        screen: Any
    ) -> None:
        text = font.render(txt, True, color)
        text_rect = text.get_rect(center=xy)

        screen.blit(text, text_rect)

        return None

    @staticmethod
    def draw_arrow(screen, color, start, end, radius) -> None:
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

    def run(self):

        pygame.init()
        WIDTH, HEIGHT = 1600, 900
        radius = 20
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont(None, 15)
        running = True
        di = Algo(self.confs)

        drone_img = pygame.image.load("./configs/img/drone.png").convert_alpha()
        drone_img = pygame.transform.scale(drone_img, (50, 50))

        rest_img = pygame.image.load("./configs/img/rest.png").convert_alpha()
        rest_img = pygame.transform.scale(rest_img, (30, 30))

        pr_img = pygame.image.load("./configs/img/priority.png").convert_alpha()
        pr_img = pygame.transform.scale(pr_img, (30, 30))
        # paths = di.all_paths
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

                # if hub.zone.value == ZoneType.priority.value:
                #     screen.blit(pr_img, (hub_x + 10, hub_y + 10))

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
                di.walk()

            for drone in self.confs.all_drones:
                drone.move()

            pygame.display.flip()

        pygame.quit()
