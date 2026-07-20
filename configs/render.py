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
        WIDTH, HEIGHT = 800, 600
        radius = 40
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont(None, 15)
        running = True
        di = Algo(self.confs)
        paths = di.all_paths
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
                for i, drone in enumerate(hub.drones):
                    coords = (hub_x + 1.5 * i, hub_y + 1.5 * i)
                    pygame.draw.rect(screen, "grey", (coords[0], coords[1], arest, arest))
                    # print(f"D{hub.id}")
                    text = font.render(f"D{drone.id}", True, "black")
                    text_rect = text.get_rect(center=(coords[0] + arest / 2, coords[1] + arest / 2))
                    screen.blit(text, text_rect)

                # self.render_txt(
                #     font,
                #     f"{hub.zone.name}: {str(hub.zone.value)}",
                #     (0, 0, 0),
                #     (hub_x, hub_y + 25),
                #     screen
                # )

                # self.render_txt(
                #     font,
                #     f"level: {str(hub.level)}",
                #     (0, 0, 0),
                #     (hub_x, hub_y - 25),
                #     screen
                # )

                # self.render_txt(
                #     font,
                #     f"max_drones: {str(hub.max_drones)}",
                #     (0, 0, 0),
                #     (hub_x, hub_y - 40),
                #     screen
                # )

                # text = font.render(str(hub.drones), True, (0, 0, 0))
                # text_rect = text.get_rect(center=(hub_x, hub_y))

                # screen.blit(text, text_rect)

            pygame.display.flip()
            di.walk()
            # running = False

        pygame.quit()
