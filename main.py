from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Spot import Spot
from Data_Structures.Hazard import Hazard
from Robot_Control_and_Monitoring.SIMController import SIMController

if __name__ == "__main__":
    # add-on 객체 생성
    addOn = SIMController()

    # 지도 정보 초기화
    rows, cols = 7, 7
    robotCoord = (1, 5, 0)  # (0,0)에 위치하고 북쪽을 바라보도록 초기화
    spots = [Spot(4,4), Spot(0,2), Spot(2,1)]
    hazards = [Hazard(1, 1, False), Hazard(3,3, True), Hazard(2, 4, True)]
    colorBlobs = [ColorBlob(1,3,True), ColorBlob(3,4,True), ColorBlob(5,4,True)]

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

    print("\n⭐ All Spots Have Been Explored!")