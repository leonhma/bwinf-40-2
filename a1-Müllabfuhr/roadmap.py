from typing import List
from xmlrpc.client import MAXINT


class Junction:
    num: int = None
    connectedRoads = []
    distanceFromCenter: int = None

    def __init__(self, num) -> None:
        self.num = num


class Road:
    endingJunctions = []
    length = None

    def __init__(self, junction1: Junction, junction2: Junction, length: float) -> None:
        self.endingJunctions = [junction1, junction2]
        self.length = length
        junction1.connectedRoads.append(self)
        junction2.connectedRoads.append(self)
        # calculate new distance from center for farthest junction
        if junction1.distanceFromCenter is None:
            junction1.distanceFromCenter = 
        else:
            junction1.distanceFromCenter += length
        if junction2.distanceFromCenter is None:
            junction2.distanceFromCenter = length
        else:
            junction2.distanceFromCenter += length


class RoadMap:
    def __init__(data: str):
        pass

    def get5FarthestFromCenter() -> List[int]:
        pass

    def getClosestToCenter(junctions: List[Junction]) -> Junction:
        distance: float = MAXINT
        closest = None
        for junction in junctions:
            if junction.distanceFromCenter < distance:
                distance = junction.distanceFromCenter
                closest = junction
        return closest
