from Data_Structures.Hazard import Hazard
from Path_Planning_and_Map_Management.Map import Map
from Path_Planning_and_Map_Management.PathPlanner import PathPlanner
from Robot_Control_and_Monitoring.RobotController import RobotController

# 이 클래스는 SIM을 제어하여 다음 기능을 수행한다 즉, add-on을 구현한 클래스이다
# 계산된 경로를 토대로 SIM에 전진 또는 회전 명령을 내린다
# SIM으로부터 센서 값을 입력 받아서 지도에 표시하고 필요한 경우 새로운 경로를 계산한다
# 로봇이 지시를 불이행 했을 경우 새로운 경로를 계산한다


class SIMController:
    def __init__(self):
        self.mapObject = Map()
        self.pathPlanner = PathPlanner(self.mapObject)
        self.robotController = RobotController()

    def sendMovementCommand(self, path):
        # ----- 디버깅 용 - 경로 출력 ------
        # print("Path:")
        # for num, pathToPrint in enumerate(path):
        #     print(f"{num}: {pathToPrint}")
        if len(path) > 1:
            direction = ['N', 'E', 'S', 'W']
            print(f"Starting from {path[0][:2]} facing {direction[path[0][2]]}...")
        # ------------------------------------

        movementDict = {
            1: 0,  # up
            2: 1,  # right
            -1: 2,  # down
            -2: 3  # left
        }
        rotationDict = [[0, 3, 2, 1],  # movement에 따른 필요 회전 수
                        [1, 0, 3, 2],
                        [2, 1, 0, 3],
                        [3, 2, 1, 0]]

        currentCol, currentRow, currentDirection = path[0]  # 첫 지점은 시작점
        currentPosition = (currentCol, currentRow, currentDirection)

        # 이동하고자 하는 다음 지점에 대해 반복
        for i in range(1, len(path)):
            # ------- 디버깅 용 -------
            print(f"\n[Add-on]: Attempting to move to Point #{i}: {path[i]}...")
            # -----------------------

            # 중요지점, 시작지점, 위험지점 여부 탐색
            self.receiveSensorData(currentPosition, checkColorBlob=True, checkSpot=True, checkHazard=True)

            # 필요 회전 수 계산
            nextPosition = path[i]
            nextCol, nextRow = nextPosition
            colDiff, rowDiff = nextCol - currentCol, nextRow - currentRow
            movement = movementDict[2 * colDiff + rowDiff]
            requiredTurns = rotationDict[movement][currentDirection]

            # 회전이 필요한 만큼 회전 시킨다
            for turn in range(requiredTurns):
                self.robotController.rotate()
                currentDirection = (currentDirection + 1) % 4
                currentPosition = (currentCol, currentRow, currentDirection)
                self.mapObject.setRobotCoord(currentPosition)
                # 위험지점 여부 탐색
                self.receiveSensorData(currentPosition, checkHazard=True)

            # 전진 가능 여부 판단
            pathObstructed, wrongMovement = False, False
            revealedHazards = [hazard.getPosition() for hazard in self.mapObject.getHazards() if not hazard.isHidden()]
            if nextPosition in revealedHazards:
                # 전진 불가능
                print(f"\t🚧 Path obstructed when trying to move to {nextPosition}!")
                pathObstructed = True
            else:
                # 전진 가능하면 전진
                self.robotController.move(self.mapObject.getHazards(), self.mapObject.getMapLength())
                # 이동하고자 하는 지점으로 add-on 상의 로봇 위치 업데이트
                currentCol, currentRow = nextPosition
                currentPosition = (currentCol, currentRow, currentDirection)
                self.mapObject.setRobotCoord(currentPosition)

                # 지시 불이행 여부 판단
                actualPosition = self.receiveSensorData(currentPosition, checkCurrentPosition=True)
                if actualPosition != self.mapObject.getRobotCoord():
                    wrongMovement = True
                if wrongMovement:
                    self.mapObject.setRobotCoord(actualPosition)
                    print("\t❌ Robot has malfunctioned!!!")

            # 필요 시 경로 재계획
            if pathObstructed or wrongMovement:
                print("\t\t📝 Replanning path...\n")
                replannedPath = self.pathPlanner.planPath()
                self.sendMovementCommand(replannedPath)
                self.receiveSensorData(currentPosition, checkHazard=True, checkSpot=True, checkColorBlob=True)
                return

        # 모든 이동이 끝난 이후, 마지막 지점에 대해 센서 작동
        self.receiveSensorData(currentPosition, checkHazard=True, checkSpot=True, checkColorBlob=True)

    # 센서를 가동해서 센서의 값들을 불러오고 새로운 지점을 지도에 반영한다
    # 다음 경로를 입력받아서 경로 재계획이 필요한지 판단하여 반환
    def receiveSensorData(self, currentPosition=None, checkHazard=False, checkColorBlob=False, checkSpot=False, checkCurrentPosition=False):
        if checkHazard:
            newHazard = self.robotController.detectHazard(self.mapObject.getHazards())
            if newHazard:
                newHazard.setRevealed()

        if checkColorBlob:
            newColorBlobs = self.robotController.detectColorBlob(self.mapObject.getColorBlobs())
            for newColorBlob in newColorBlobs:
                newColorBlob.setRevealed()

        # 탐색 지점을 탐색 했는지 확인
        if checkSpot:
            spots = self.mapObject.getSpots()
            for spot in spots:
                if spot.getPosition() == currentPosition[:2] and not spot.isExplored():
                    spot.setExplored()

        if checkCurrentPosition:
            actualPosition = self.robotController.detectPosition()
            return actualPosition
