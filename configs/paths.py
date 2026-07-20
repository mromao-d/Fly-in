from hubs import HubNodes, HubType


class Paths:
    def __init__(
        self,
        path: list[HubNodes],
        # bottleneck_nb: int,
        priority: bool
    ):
        self.path = path
        self.priority = priority
        self.bottleneck_nb = self.calc_botle_neck()
        self.cost = self.calculate_cost()

    def calculate_cost(self) -> None:
        cost = 0
        for i, node in enumerate(self.path):
            cost += node.zone.value
        return cost

    def calc_botle_neck(self) -> int:
        botle = 0
        for hub in self.path:
            if hub.hub_type in (HubType.start_hub, HubType.end_hub):
                continue
            capacity = hub.max_drones - len(hub.drones)
            if botle == 0:
                botle = capacity
            elif botle > capacity:
                botle = capacity
        return botle
