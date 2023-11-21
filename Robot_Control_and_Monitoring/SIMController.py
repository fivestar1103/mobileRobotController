from Path_Planning_and_Map_Management.Map import Map
from Path_Planning_and_Map_Management.PathPlanner import PathPlanner
from Robot_Control_and_Monitoring.RobotController import RobotController


# 이 클래스는 SIM을 제어하여 다음 기능을 수행한다 즉, add-on을 구현한 클래스이다
# 계산된 경로를 토대로 SIM에 전진 또는 회전 명령을 내린다
# SIM으로부터 센서 값을 입력 받아서 지도에 표시하고 필요한 경우 새로운 경로를 계산한다
# 로봇이 지시를 불이행 했을 경우 새로운 경로를 계산한다
class SIMController:
    def __init__(self):
        self.__path = None
        self.mapInstance = Map()
        self.display = None
        self.pathPlanner = PathPlanner(self.mapInstance)
        self.robotController = RobotController()
        self.waitTime = 100
        self.allGoalsVisited = False

    def get_path(self):
        return self.__path

    def set_path(self):
        self.pathPlanner.plan_path()
        self.__path = self.pathPlanner.get_current_path()
        return

    def send_movement_command(self):
        if self.display.isStop:
            return
        self.receive_sensor_data(checkColorBlob=True, checkSpot=True, checkHazard=True)

        if self.__path:
            currentPosition = self.mapInstance.get_robot_coord()
            nextPosition = self.__path[-1]

            direction = ["N", "E", "S", "W"]
            print(
                f"\n[Add-on]: Currently at {currentPosition[:2]} facing {direction[currentPosition[2]]}, attempting to move to {nextPosition}...")

            isRotationRequired = self.calculate_rotation(nextPosition)
            if isRotationRequired:
                self.execute_rotation()
                # Schedule the next rotation or movement after the wait time
                self.display.master.after(self.waitTime, self.send_movement_command)
            else:
                self.execute_move_and_plan()
        else:
            self.complete_movement_process()

    def calculate_rotation(self, nextPosition):
        # 이동해야 하는 방향마다 colDiff * 2 + rowDiff로 계산한 값을 고유 key로 갖는다
        movementDict = {
            1: 0,  # up
            2: 1,  # right
            -1: 2,  # down
            -2: 3  # left
        }
        nextCol, nextRow = nextPosition
        currentPosition = self.mapInstance.get_robot_coord()
        currentCol, currentRow, currentDirection = currentPosition
        colDiff, rowDiff = nextCol - currentCol, nextRow - currentRow
        movement = movementDict[2 * colDiff + rowDiff]
        isRotationRequired = False if movement == currentDirection else True
        return isRotationRequired

    def execute_rotation(self):
        self.robotController.rotate()
        self.mapInstance.rotate_robot_on_map()
        self.display.update_display()
        self.display.master.after(self.waitTime)  # Then wait for the specified time

    def execute_move_and_plan(self):
        originalPosition = self.mapInstance.get_robot_coord()
        # Check if the next position is blocked by a revealed hazard
        hazards = self.mapInstance.get_hazards()
        revealedHazards = [hazard.get_position() for hazard in hazards if not hazard.is_hidden()]

        # If there are still steps in the path, check for hazards and execute the move
        if self.__path:
            nextPosition = self.__path.pop()  # Peek at the next position

            # Check if the next position is a hazard
            if nextPosition in revealedHazards:
                self.display.master.after(self.waitTime)
                print(f"\t🚧 Path obstructed! Replanning path...")
                self.display.log_message(f"🚧 Path obstructed at {nextPosition}!\n\tReplanning path...\n")
                self.replan_path()
            else:
                # If the path is clear, execute the move
                self.execute_move()
                self.check_correct_movement(originalPosition)

            self.display.master.after(self.waitTime, self.send_movement_command)
        else:
            # If the path is complete, finalize the movement process
            self.complete_movement_process()

    def execute_move(self):
        self.robotController.move(self.mapInstance.get_hazards(), self.mapInstance.get_map_length())
        self.mapInstance.move_robot_on_map()
        self.display.master.after(self.waitTime)  # Then wait for the specified time

    # 센서를 가동해서 센서의 값들을 불러오고 새로운 지점을 지도에 반영한다
    def receive_sensor_data(self, checkHazard=False, checkColorBlob=False, checkSpot=False,
                            checkCurrentPosition=False):
        if checkHazard:
            newHazard = self.robotController.detect_hazard(self.mapInstance.get_hazards())
            if newHazard:
                newHazard.set_revealed()
                self.display.log_message(f"⚠️Hazard uncovered at {newHazard.get_position()}\n")

        if checkColorBlob:
            newColorBlobs = self.robotController.detect_color_blob(self.mapInstance.get_color_blobs())
            for newColorBlob in newColorBlobs:
                newColorBlob.set_revealed()
                self.display.log_message(f"🔵 ColorBlob uncovered at {newColorBlob.get_position()}\n")

        # 탐색 지점을 탐색 했는지 확인
        if checkSpot:
            spots = self.mapInstance.get_spots()
            for spot in spots:
                currentPosition = self.mapInstance.get_robot_coord()
                if spot.get_position() == currentPosition[:2] and not spot.is_explored():
                    spot.set_explored()
                    self.display.log_message(f"✅ Spot visited at {spot.get_position()}\n")

            unexploredSpots = [spot for spot in spots if not spot.is_explored()]
            if len(unexploredSpots) == 0:
                self.display.update_display()
                self.complete_movement_process()

        if checkCurrentPosition:
            actualPosition = self.robotController.detect_position()
            return actualPosition

        self.display.update_display()
        self.display.master.after(self.waitTime)

    def complete_movement_process(self):
        if not self.allGoalsVisited:  # Check if the flag is False
            self.allGoalsVisited = True  # Set the flag to True
            self.__path = []
            print("All spots explored!")
            self.display.alert("⭐ All Spots Have Been Explored!")
            self.display.on_goOrStop()

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

    def replan_path(self):
        print("\t\t📝 Replanning path...\n")
        self.set_path()

    def check_correct_movement(self, originalPosition):
        currentPosition = self.mapInstance.get_robot_coord()
        actualPosition = self.receive_sensor_data(checkCurrentPosition=True)

        if actualPosition != currentPosition:
            print("\t❌ Robot has malfunctioned!!!")
            self.display.log_message(f"❌ Robot has malfunctioned at {originalPosition[:2]}!\n\tReplanning path...\n")
            self.mapInstance.set_robot_coord(actualPosition)

            self.replan_path()
        self.display.update_display()
        self.display.master.after(self.waitTime)  # Then wait for the specified time

