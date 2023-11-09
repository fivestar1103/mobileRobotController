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

        currentCol, currentRow, currentDirection = path[0]  # 경로의 첫 튜플의 마지막 값은 로봇의 방향이다
        movementDict = {
            1: 0,  # up
            2: 1,  # right
            -1: 2,  # down
            -2: 3  # left
        }
        rotationDict = [[0, 3, 2, 1],
                        [1, 0, 3, 2],
                        [2, 1, 0, 3],
                        [3, 2, 1, 0]]

        for i in range(1, len(path)):
            # ------- 디버깅 용 -------
            print(f"Attempting to move to Point #{i}: {path[i]}...")
            # -----------------------

            nextPosition = path[i]
            nextPath = path[i + 1] if i < len(path) - 1 else None  # 마지막 경로일 경우 다음 경로가 막힐 경우에 대한 판단 불필요

            nextCol, nextRow = nextPosition
            colDiff, rowDiff = nextCol - currentCol, nextRow - currentRow
            movement = movementDict[2 * colDiff + rowDiff]
            requiredTurns = rotationDict[movement][currentDirection]

            # 우선 회전이 필요한 만큼 회전 시킨다
            for turn in range(requiredTurns):
                self.robotController.rotate()
                currentDirection = (currentDirection + 1) % 4
                currentPosition = (currentCol, currentRow, currentDirection)

                # 회전 후 앞의 한 칸이 위험 지점 여부 감지
                movementAccordingToDirection = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                colDiff, rowDiff = movementAccordingToDirection[currentDirection]
                newCol, newRow = currentCol + colDiff, currentRow + rowDiff
                newPosition = (newCol, newRow)
                # 맵 밖으로 이동하는 경우는 예외 처리
                mapLength = self.mapObject.getMapLength()
                if (newCol < 0 or newCol >= mapLength[0]) or (newRow < 0 or newRow >= mapLength[1]):
                    newPosition = None
                self.receiveSensorData(currentPosition, newPosition, isRotation=True)

            # 그 다음에 앞으로 한 칸 전진 명령을 내린다
            self.robotController.move(self.mapObject.getHazards(), self.mapObject.getMapLength())
            currentCol, currentRow = nextPosition

            # 센서 값을 받아서 경로 재계획이 필요한지 판단하고 필요시 경로 재계획
            newPosition = (nextCol, nextRow, currentDirection)
            isNewPathRequired = self.receiveSensorData(newPosition, nextPath)
            if isNewPathRequired:
                print("\t\tReplanning path...\n")
                replannedPath = self.pathPlanner.planPath()
                self.sendMovementCommand(replannedPath)
                break

    # 센서를 가동해서 센서의 값들을 불러오고 새로운 지점을 지도에 반영한다
    # 다음 경로를 입력받아서 경로 재계획이 필요한지 판단하여 반환
    def receiveSensorData(self, currentPosition, nextPosition, isRotation=False):
        # 센서 가동 명령을 내린다
        revealedHazard = self.robotController.detectHazard(self.mapObject.getHazards())
        revealedColorBlobs = self.robotController.detectColorBlob(self.mapObject.getColorBlobs())
        actualPosition = self.robotController.detectPosition()

        # 회전만 한 경우는 위험 지점만 탐색
        if isRotation:
            # print(f"\tchecking hazard at {nextPosition}")
            if nextPosition and revealedHazard:  # 다음 경로가 존재하지 않는다면 검사하지 않는다.
                self.mapObject.revealHidden(revealedHazard)
                return

        for revealedColorBlob in revealedColorBlobs:
            self.mapObject.revealHidden(revealedColorBlob)

        # 실제 로봇 위치를 업데이트 한다
        self.mapObject.setRobotCoord(actualPosition)

        # 탐색 지점을 탐색 했는지 확인
        spots = self.mapObject.getSpots()
        for spot in spots:
            if spot.getPosition() == actualPosition[:2] and not spot.isExplored():
                spot.setExplored(True)

        # 지시를 불이행 한 경우
        if actualPosition != currentPosition:
            print("\t Robot has malfunctioned!")
            return True

        # 위험 지점으로 인해 다음 경로가 막힌 경우
        hazards = self.mapObject.getHazards()
        for hazard in hazards:
            if nextPosition and hazard.getPosition() == nextPosition[:2] and not hazard.isHidden():
                print(f"\t Path obstructed when trying to move to {nextPosition[:2]}!")
                return True

        return False
