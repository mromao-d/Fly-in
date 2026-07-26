from hubs import HubNodes, HubType


class Paths:
    def __init__(
        self,
        hubs: list[HubNodes],
        # bottleneck_nb: int,
        priority: bool,
        restricted: bool
    ):
        self.hubs = hubs
        self.priority = priority
        self.restricted = restricted
        self.bottleneck_nb = self.calc_botle_neck()
        self.cost = self.calculate_cost()

    def calculate_cost(self) -> None:
        cost = 0
        for i, node in enumerate(self.hubs):
            cost += node.zone.value
        return cost

    def calc_botle_neck(self) -> int:
        botle = 0
        for hub in self.hubs:
            if hub.hub_type in (HubType.start_hub, HubType.end_hub):
                continue
            capacity = hub.max_drones - len(hub.drones)
            if botle == 0:
                botle = capacity
            elif botle > capacity:
                botle = capacity
        return botle
