from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Spot import Spot
from Data_Structures.Hazard import Hazard
from Robot_Control_and_Monitoring.SIMController import SIMController

if __name__ == "__main__":
    # add-on 객체 생성
    addOn = SIMController()

    # 지도 정보 초기화
    rows, cols = 7, 7
    robotCoord = (5, 1, 0)  # (0,0)에 위치하고 북쪽을 바라보도록 초기화
    spots = [Spot(4,4), Spot(2,0), Spot(1,2)]
    hazards = [Hazard(1, 1, False), Hazard(3,3, True), Hazard(4, 2, True)]
    colorBlobs = [ColorBlob(3,1,True), ColorBlob(4,3,True), ColorBlob(4,5,True)]

    mapInstance = addOn.mapObject
    mapInstance.setMapLength(rows, cols)
    mapInstance.setRobotCoord(robotCoord)
    mapInstance.setSpots(spots)
    mapInstance.setHazards(hazards)
    mapInstance.setColorBlobs(colorBlobs)

    # 경로 계산
    pathPlannerInstance = addOn.pathPlanner
    newPath = pathPlannerInstance.planPath()

    # 이동 지시
    addOn.robotController.setCurrentPosition(robotCoord)
    addOn.sendMovementCommand(newPath)

    print("\n⭐ All Spots Have Been Explored!\n\tExiting...")