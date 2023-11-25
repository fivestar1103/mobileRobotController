# 이 클래스는 add-on을 구현한 것으로, SIM을 제어하여 다음 기능을 수행한다.
# - 계산된 경로를 토대로 SIM에 전진 또는 회전 명령을 내린다
# - SIM으로부터 센서 값을 입력 받아서 지도에 표시하고 필요한 경우 새로운 경로를 계산한다
# - 로봇이 지시를 불이행 했을 경우 새로운 경로를 계산한다

from Backend.Map_Management_and_Path_Planning.Map import Map
from Backend.Map_Management_and_Path_Planning.PathPlanner import PathPlanner
from Backend.Controllers.RobotController import RobotController
from Frontend.Map_Visualization_and_Initialization.Display import Display


class SIMController:
    def __init__(self, mapInstance: Map, pathPlanner: PathPlanner):
        self.__mapInstance = mapInstance
        self.__pathPlanner = pathPlanner
        self.__display = Display(self, mapInstance)
        self.__robotController = RobotController()

        self.__path = None
        self.__waitTime = 100
        self.__allGoalsVisited = False

    # 맵 객체를 반환
    def get_mapInstance(self):
        return self.__mapInstance

    # 맵 객체를 설정
    def set_mapInstance(self, mapInstance: Map):
        self.__mapInstance = mapInstance

    # 디스플레이 객체를 반환
    def get_display(self):
        return self.__display

    # 디스플레이 객체를 설정
    def set_display(self, display: Display):
        self.__display = display

    # 패스플래너 객체를 반환
    def get_pathPlanner(self):
        return self.__pathPlanner

    # 패스플래너 객체를 설정
    def set_pathPlanner(self, pathPlanner: PathPlanner):
        self.__pathPlanner = pathPlanner

    # 로봇컨트롤러 객체를 반환
    def get_robotController(self):
        return self.__robotController

    # 로봇컨트롤러 객체를 설정
    def set_robotController(self, robotController: RobotController):
        self.__robotController = robotController

    # 현재 경로를 반환
    def get_path(self):
        return self.__path

    # 현재 경로를 설정
    def set_path(self):
        self.__pathPlanner.plan_path()
        self.__path = self.__pathPlanner.get_current_path()
        return

    # 이동 동작 지시
    def send_movement_command(self):
        if self.__display.isStop:
            return
        self.receive_sensor_data(checkColorBlob=True, checkSpot=True, checkHazard=True)

        if self.__path:
            currentPosition = self.__mapInstance.get_robot_coord()
            nextPosition = self.__path[-1]

            direction = ["N", "E", "S", "W"]
            print(f"\n[Add-on]: Currently at {currentPosition[:2]} facing {direction[currentPosition[2]]}, attempting to move to {nextPosition}...")

            # 회전이 필요하다면 먼저 회전한다. 그 다음에 이동한다.
            isRotationRequired = self.calculate_rotation(nextPosition)
            if isRotationRequired:
                self.execute_rotation()
                self.__display.master.after(self.__waitTime, self.send_movement_command)
            else:
                self.check_and_move()
        else:
            self.complete_movement_process()  # 경로의 끝에 도달한 경우

    # 회전이 필요한지 확인
    def calculate_rotation(self, nextPosition):
        movementDict = {
            1: 0,  # up
            2: 1,  # right
            -1: 2,  # down
            -2: 3  # left
        }
        nextCol, nextRow = nextPosition
        currentPosition = self.__mapInstance.get_robot_coord()
        currentCol, currentRow, currentDirection = currentPosition
        colDiff, rowDiff = nextCol - currentCol, nextRow - currentRow
        movement = movementDict[2 * colDiff + rowDiff]  # 이동해야 하는 방향마다 colDiff * 2 + rowDiff로 계산한 값을 고유 key로 갖는다
        isRotationRequired = False if movement == currentDirection else True
        return isRotationRequired

    # 로봇을 회전시킨다
    def execute_rotation(self):
        self.__robotController.rotate()
        self.__mapInstance.rotate_robot_on_map()
        self.__display.update_display()
        self.__display.master.after(self.__waitTime)

    # 로봇을 이동시킨다
    def execute_move(self):
        self.__robotController.move(self.__mapInstance.get_hazards(), self.__mapInstance.get_map_length())
        self.__mapInstance.move_robot_on_map()
        self.__display.update_display()
        self.__display.master.after(self.__waitTime)

    # 앞으로 전진할 수 있는지 판단하고 제대로 이동했는지 확인
    def check_and_move(self):
        originalPosition = self.__mapInstance.get_robot_coord()  # 이동하기 전의 위치

        hazards = self.__mapInstance.get_hazards()
        revealedHazards = [hazard.get_position() for hazard in hazards if not hazard.is_hidden()]

        nextPosition = self.__path.pop()  # 다음으로 이동 할 위치
        if nextPosition in revealedHazards:  # 다음 위치에 위험 지점이 있는지 확인
            self.__display.master.after(self.__waitTime)
            print(f"\t🚧 Path obstructed! Replanning path...")
            self.__display.log_message(f"🚧 Path obstructed at {nextPosition}!\n\tReplanning path...\n")

            print("\t\t📝 Replanning path...\n")
            self.set_path()  # 이동 불가능하면 경로 재계획
        else:
            self.execute_move()  # 이동 가능하면 다음 지점으로 이동
            self.check_correct_movement(originalPosition)  # 제대로 이동했는지 확인
        self.__display.master.after(self.__waitTime, self.send_movement_command)  # 다음 지점으로 이동 지시

    # 제대로 이동했는지 확인
    def check_correct_movement(self, originalPosition):
        currentPosition = self.__mapInstance.get_robot_coord()
        actualPosition = self.receive_sensor_data(checkCurrentPosition=True)

        if actualPosition != currentPosition:
            print("\t❌ Robot has malfunctioned!!!")
            self.__display.log_message(
                f"❌ Robot has malfunctioned at {originalPosition[:2]}!\n\tReplanning path...\n")
            self.__mapInstance.set_robot_coord(actualPosition)

            print("\t\t📝 Replanning path...\n")
            self.set_path()  # 잘못 이동한 경우 경로 재계획
        self.__display.update_display()

    # 센서를 가동해서 센서의 값들을 불러오고 새로운 지점을 지도에 반영한다
    def receive_sensor_data(self, checkHazard=False, checkColorBlob=False, checkSpot=False, checkCurrentPosition=False):
        # 위험 지점 탐색
        if checkHazard:
            newHazard = self.__robotController.detect_hazard(self.__mapInstance.get_hazards())
            if newHazard:
                newHazard.set_revealed()
                self.__display.log_message(f"⚠️Hazard uncovered at {newHazard.get_position()}\n")

        # 중요 지점 탐색
        if checkColorBlob:
            newColorBlobs = self.__robotController.detect_color_blob(self.__mapInstance.get_color_blobs())
            for newColorBlob in newColorBlobs:
                newColorBlob.set_revealed()
                self.__display.log_message(f"🔵 ColorBlob uncovered at {newColorBlob.get_position()}\n")

        # 탐색 지점을 방문 했는지 확인
        if checkSpot:
            spots = self.__mapInstance.get_spots()
            for spot in spots:
                currentPosition = self.__mapInstance.get_robot_coord()
                if spot.get_position() == currentPosition[:2] and not spot.is_explored():
                    spot.set_explored()
                    self.__display.log_message(f"✅ Spot visited at {spot.get_position()}\n")

            unexploredSpots = [spot for spot in spots if not spot.is_explored()]
            if len(unexploredSpots) == 0:
                self.__display.update_display()
                self.complete_movement_process()

        # 현재 위치 확인
        if checkCurrentPosition:
            actualPosition = self.__robotController.detect_position()
            return actualPosition

        self.__display.update_display()
        self.__display.master.after(self.__waitTime)

    # 경로의 끝에 도달했거나 모든 지점을 방문 완료한 경우 종료 시퀀스 수행
    def complete_movement_process(self):
        if not self.__allGoalsVisited:  # 한번만 수행하기 위해 flag 설정
            self.__allGoalsVisited = True
            self.__path = []
            print("All spots explored!")
            self.__display.alert("⭐ All Spots Have Been Explored!")
            self.__display.on_goOrStop()

    # 한 지점으로 이동하기 전마다 음성인식으로 추가할 것인지 묻고 인터럽트 여부를 반환
    # def handle_voice_input(self):
    #     while True:
    #         goOrStop = input("Go or Stop?: ")
    #         if goOrStop.lower() in ["go", "stop"]:
    #             break
    #         print("\tinvalid input...")
    #     if goOrStop == "stop":
    #         # 음성 인식
    #         newPoints = self.voiceInputHandler.receive_voice_input()
    #         self.mapInstance.add_new_points(newPoints)
    #         # 새로운 정보를 기반으로 경로 재계획
    #         self.replan_path()
    #         return True
    #     else:
    #         print("\tContinuing as planned...\n")
    #         return False
