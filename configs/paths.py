from hubs import HubNodes, HubType, ZoneType


class Paths:
    """
    class that has all valid paths from start hub untill end hub
    """
    def __init__(
        self,
        hubs: list[HubNodes],
        priority: bool,
        restricted: bool
    ):
        """
        inits the class
        Args:
            hubs (HubNodes): List of hubs ordered from start to end
            priority (bool): tells if I chose the priority path for each turn
            restricted (bool): if path is restricted. Not used at the moment
        """
        self.hubs = hubs
        self.priority = priority
        self.restricted = restricted
        self.bottleneck_nb = self.calc_botle_neck()
        self.cost = self.calculate_cost()

    def calculate_cost(self) -> None:
        """
        calculates the total cost of the path
        """
        cost = 0
        for node in self.hubs:
            add_cost = 1 if node.zone == ZoneType.priority else node.zone.value
            cost += add_cost
        return cost

    def calc_botle_neck(self) -> int:
        """
        calculates the botle neck of the path
        """
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
