class RobotController:
    def __init__(self):
        self._currentPosition = None  # 로봇의 현재 위치
        self._path = []  # 로봇이 따라갈 경로

    def getCurrentPosition(self):
        """로봇의 현재 위치를 반환"""
        return self._currentPosition

    def setCurrentPosition(self, row, col):
        """로봇의 현재 위치를 설정"""
        self._current_position = (row, col)

    def getPath(self):
        """로봇의 경로를 반환"""
        return self._path

    def setPath(self, path):
        """로봇의 경로를 설정"""
        self._path = path

    def move(self):
        """로봇을 이동시킨다"""
        # 이동 로직 구현
        pass

    def rotate(self):
        """로봇을 회전시킨다"""
        # 회전 로직 구현
        pass

    def detectHazard(self):
        """위험 지점을 감지"""
        # 위험 지점 감지 로직 구현
        pass

    def detectColorBlob(self):
        """중요 지점을 감지"""
        # 중요 지점 감지 로직 구현
        pass
