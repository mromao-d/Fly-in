import pygame
import math
from typing import Any
from algo import Algo


class RenderMap:
    def __init__(self, ReadConfs):
        self.confs = ReadConfs
        self.grid_size = ReadConfs.grid_size
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
        radius = 40
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont(None, 15)
        running = True
        di = Algo(self.confs)
        # paths = di.all_paths
        while running:
            WIDTH, HEIGHT = screen.get_size()
            running = self.handle_events()
            screen.fill((255, 255, 255))

            for hub in self.confs.hubs:
                hub_x = (hub.coord[0] + 1) * (WIDTH / (self.grid_size[0] + 2))
                hub_y = (hub.coord[1] + 1) * (HEIGHT / (self.grid_size[1] + 2))

                for f_node in hub.conn_nodes:
                    f_x = (f_node.coord[0] + 1) * (WIDTH / (self.grid_size[0] + 2))
                    f_y = (f_node.coord[1] + 1) * (HEIGHT / (self.grid_size[1] + 2))

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
                self.render_txt(
                    font,
                    hub.hub_name,
                    (0, 0, 0),
                    (hub_x, hub_y),
                    screen
                )

                arest = 20

            for i, drone in enumerate(self.confs.all_drones):
                drone_x = (drone.curr_coord[0] + 1) * (WIDTH / (self.grid_size[0] + 2))
                drone_y = (drone.curr_coord[1] + 1) * (HEIGHT / (self.grid_size[1] + 2))
                pygame.draw.rect(screen, "grey", (drone_x, drone_y, arest, arest))
                text = font.render(f"D{drone.id}", True, "black")
                text_rect = text.get_rect(center=(drone_x + arest / 2, drone_y + arest / 2))
                screen.blit(text, text_rect)

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
