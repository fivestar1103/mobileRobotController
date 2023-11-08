from Sensor import Sensor

class ColorBlobSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.set_sensor_type('ColorBlob')

    def readSensor(self):
        """주변 네 칸 중 중요 지점을 감지하는 메서드"""
        # 실제 센서 데이터를 읽어 중요 지점 여부를 반환하는 로직 구현
        pass

    def detectColorBlob(self):
        """중요 지점을 감지하고 그 정보를 반환하는 메서드"""
        return self.get_sensor_data()
