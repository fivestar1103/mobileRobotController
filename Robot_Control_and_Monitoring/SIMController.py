from Display_and_Visualization.Display import Display
from Path_Planning_and_Map_Management.Map import Map
from Path_Planning_and_Map_Management.PathPlanner import PathPlanner
from Robot_Control_and_Monitoring.RobotController import RobotController
from User_Interface.VoiceInputHandler import VoiceInputHandler


# 이 클래스는 SIM을 제어하여 다음 기능을 수행한다 즉, add-on을 구현한 클래스이다
# 계산된 경로를 토대로 SIM에 전진 또는 회전 명령을 내린다
# SIM으로부터 센서 값을 입력 받아서 지도에 표시하고 필요한 경우 새로운 경로를 계산한다
# 로봇이 지시를 불이행 했을 경우 새로운 경로를 계산한다


class SIMController:
    def __init__(self):
        self.__path = None
        self.mapObject = Map()
        self.pathPlanner = PathPlanner(self.mapObject)
        self.robotController = RobotController()
        self.voiceInputHandler = VoiceInputHandler()
        self.display = Display(self.mapObject)

    def get_path(self):
        return self.__path

    def set_path(self):
        self.pathPlanner.plan_path()
        self.__path = self.pathPlanner.get_current_path()
        return

    def send_movement_command(self):
        # ----- 디버깅 용 - 경로 출력 ------
        currentPositionTemp = self.mapObject.get_robot_coord()
        direction = ['N', 'E', 'S', 'W']
        print(f"Starting from {currentPositionTemp[:2]} facing {direction[currentPositionTemp[2]]}...")

        while self.__path:
            nextPosition = self.__path.pop()
            currentPosition = self.mapObject.get_robot_coord()
            # 중요지점, 시작지점, 위험지점 여부 탐색
            self.receive_sensor_data(checkColorBlob=True, checkSpot=True, checkHazard=True)

            print(f"\n[Add-on]: Currently at {currentPosition[:2]}, attempting to move to {nextPosition}...")

            # STT로 새로운 정보 입력할지 결정
            isInterrupted = self.handle_voice_input()
            if isInterrupted:
                continue

            # 필요 회전 수 계산
            requiredTurns = self.calculate_rotation(nextPosition)
            # 회전이 필요한 만큼 회전 시킨다
            for _ in range(requiredTurns):
                self.execute_rotation()
                # 위험지점 여부 탐색
                self.receive_sensor_data(checkHazard=True)

            # 전진 가능 여부 판단
            hazards = self.mapObject.get_hazards()
            revealedHazards = [hazard.get_position() for hazard in hazards if not hazard.is_hidden()]
            if nextPosition in revealedHazards:
                # 전진 불가능하면 경로 재계획
                print(f"\t🚧 Path obstructed when trying to move to {nextPosition}!")
                self.replanPath()
            else:
                # 전진 가능하면 전진
                self.execute_move()
                # 지시 불이행 여부 판단
                self.check_correct_movement()

        # 모든 이동이 끝난 이후, 마지막 지점에서 센서 작동
        self.receive_sensor_data(checkHazard=True, checkSpot=True, checkColorBlob=True)

    # 센서를 가동해서 센서의 값들을 불러오고 새로운 지점을 지도에 반영한다
    # 다음 경로를 입력받아서 경로 재계획이 필요한지 판단하여 반환
    def receive_sensor_data(self, checkHazard=False, checkColorBlob=False, checkSpot=False, checkCurrentPosition=False):
        if checkHazard:
            newHazard = self.robotController.detect_hazard(self.mapObject.get_hazards())
            if newHazard:
                newHazard.set_revealed()

        if checkColorBlob:
            newColorBlobs = self.robotController.detect_color_blob(self.mapObject.get_color_blobs())
            for newColorBlob in newColorBlobs:
                newColorBlob.set_revealed()

        # 탐색 지점을 탐색 했는지 확인
        if checkSpot:
            spots = self.mapObject.get_spots()
            for spot in spots:
                currentPosition = self.mapObject.get_robot_coord()
                if spot.get_position() == currentPosition[:2] and not spot.is_explored():
                    spot.set_explored()

        if checkCurrentPosition:
            actualPosition = self.robotController.detect_position()
            return actualPosition

    # 한 지점으로 이동하기 전마다 음성인식으로 추가할 것인지 묻고 인터럽트 여부를 반환
    def handle_voice_input(self):
        while True:
            goOrStop = input("Go or Stop?: ")
            if goOrStop.lower() in ["go", "stop"]:
                break
            print("\tinvalid input...")
        if goOrStop == "stop":
            # 음성 인식
            newPoints = self.voiceInputHandler.receive_voice_input()
            self.mapObject.add_new_points(newPoints)
            # 새로운 정보를 기반으로 경로 재계획
            self.replanPath()
            return True
        else:
            print("\tContinuing as planned...\n")
            return False

    def replanPath(self):
        print("\t\t📝 Replanning path...\n")
        self.set_path()

    def execute_rotation(self):
        self.robotController.rotate()
        self.mapObject.rotate_robot_on_map()

    def execute_move(self):
        self.robotController.move(self.mapObject.get_hazards(), self.mapObject.get_map_length())
        self.mapObject.move_robot_on_map()

    def calculate_rotation(self, nextPosition):
        # 이동해야 하는 방향마다 colDiff * 2 + rowDiff로 계산한 값을 고유 key로 갖는다
        movementDict = {
            1: 0,  # up
            2: 1,  # right
            -1: 2,  # down
            -2: 3  # left
        }
        # 위에서 계산한 movement에 따른 필요 회전 수
        rotationDict = [[0, 3, 2, 1],
                        [1, 0, 3, 2],
                        [2, 1, 0, 3],
                        [3, 2, 1, 0]]

        nextCol, nextRow = nextPosition
        currentPosition = self.mapObject.get_robot_coord()
        currentCol, currentRow, currentDirection = currentPosition
        colDiff, rowDiff = nextCol - currentCol, nextRow - currentRow
        movement = movementDict[2 * colDiff + rowDiff]
        requiredTurns = rotationDict[movement][currentDirection]
        return requiredTurns

    def check_correct_movement(self):
        currentPosition = self.mapObject.get_robot_coord()
        actualPosition = self.receive_sensor_data(checkCurrentPosition=True)
        if actualPosition != currentPosition:
            print("\t❌ Robot has malfunctioned!!!")
            self.mapObject.set_robot_coord(actualPosition)
            self.replanPath()
