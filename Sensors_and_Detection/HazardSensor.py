from Sensor import Sensor

class HazardSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.set_sensor_type('Hazard')

    def readSensor(self):
        """바로 앞의 칸이 위험 지점인지 감지하는 메서드"""
        # 실제 센서 데이터를 읽어 위험 지점 여부를 반환하는 로직 구현
        pass

    def detectHazard(self):
        """위험 지점을 감지하고 그 정보를 반환하는 메서드"""
        return self.get_sensor_data()
