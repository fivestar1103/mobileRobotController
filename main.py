from Data_Structures.Spot import Spot
from Data_Structures.Hazard import Hazard
from Data_Structures.ColorBlob import ColorBlob
from Path_Planning_and_Map_Management.Map import Map
from Path_Planning_and_Map_Management.PathPlanner import PathPlanner

if __name__ == "__main__":
    # 지도 정보 초기화
    robotCoord = (0, 0)
    spots = [Spot(4,4), Spot(0,2), Spot(2,1)]
    hazards = [Hazard(1, 1, False), Hazard(3,3, False)]
    colorBlobs = []

    mapInstance = Map(7, 7)
    mapInstance.setRobotCoord(robotCoord)
    mapInstance.setSpots(spots)
    mapInstance.setHazards(hazards)
    mapInstance.setColorBlobs(colorBlobs)

    fullMap = mapInstance.getFullMap()
    # print the fullMap
    print("Map:")
    for row in reversed(fullMap):
        for col in row:
            print(col, end=' ')
        print()
    print()

    pathPlannerInstance = PathPlanner(mapInstance)
    newPath = pathPlannerInstance.planPath()

    # print the path
    print("Path:")
    for num, path in enumerate(newPath):
        print(f"{num}: {path}")
