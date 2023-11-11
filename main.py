from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Spot import Spot
from Data_Structures.Hazard import Hazard
from Robot_Control_and_Monitoring.SIMController import SIMController

if __name__ == "__main__":
    print("Hello! Booting...")
    # add-on 객체 생성
    addOn = SIMController()
    print("\tBooting complete...")

    print("Initialize map: ")
    # 지도 정보 초기화
    cols, rows = 9, 8
    robotCoord = (5, 1, 0)  # (5, 1)에 위치하고 북쪽을 바라보도록 초기화
    spots = [
        Spot(4,4, False),
        Spot(2,0, False),
        Spot(1,2, False),
        Spot(8,7, False),
        Spot(0, 5, False)
    ]
    hazards = [
        Hazard(1, 1, False),
        Hazard(3,3, True),
        Hazard(4, 2, True),
        Hazard(7, 7, True),
        Hazard(7,6,True),
        Hazard(7, 5, True),
    ]
    colorBlobs = [
        ColorBlob(3,1,True),
        ColorBlob(4,3,True),
        ColorBlob(4,5,True)
    ]

    mapInstance = addOn.mapObject
    mapInstance.setMapLength(cols, rows)
    mapInstance.setRobotCoord(robotCoord)
    mapInstance.setSpots(spots)
    mapInstance.setHazards(hazards)
    mapInstance.setColorBlobs(colorBlobs)

    # 초기 맵 상태 출력
    print("\tMap initialized...")
    mapInstance.printFullMap("Initial")

    # 경로 계산
    pathPlannerInstance = addOn.pathPlanner
    newPath = pathPlannerInstance.planPath()

    # 이동 지시
    addOn.robotController.setCurrentPosition(robotCoord)
    addOn.sendMovementCommand(newPath)

    print("\n⭐ All Spots Have Been Explored!\n")
    # 최종 맵 상태 출력
    mapInstance.printFullMap("Final")

    print("\n\tExiting... Good bye!")
