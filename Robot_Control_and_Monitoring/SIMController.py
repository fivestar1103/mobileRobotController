from Path_Planning_and_Map_Management.PathPlanner import PathPlanner
from Robot_Control_and_Monitoring.RobotController import RobotController


class SIMController:
    def __init__(self, pathPlanner: PathPlanner, robotController: RobotController):
        self.__pathPlanner = pathPlanner
        self.__robotController = robotController

    # 이동 명령을
    def sendMovementCommand(self, command):
        """이동 명령을 시뮬레이터에 전송"""
        # 명령 전송 로직 구현
        pass

    def receiveSensorData(self):
        """센서 데이터를 시뮬레이터로부터 받는다"""
        # 데이터 수신 로직 구현
        pass
