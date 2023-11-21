from Data_Structures.ColorBlob import ColorBlob
from Data_Structures.Hazard import Hazard
from Data_Structures.Spot import Spot
from Robot_Control_and_Monitoring.SIMController import SIMController
from User_Interface.Display import Display
from User_Interface.OperatorInterface import OperatorInterface

if __name__ == "__main__":
    # add-on 객체 생성
    print("Hello! Booting...")
    addOn = SIMController()
    print("\tBooting complete...")

    # 지도 정보 초기화
    print("Initialize map: ")
    # ------------- debug ---------------
    debug = True
    if debug:
        cols, rows = 9, 8
        robotCoord = (5, 1, 0)  # (5, 1)에 위치하고 북쪽을 바라보도록 초기화
        spots = [
            Spot(4,4, False),
            Spot(2,0, False),
            Spot(1,2, False),
            Spot(8,7, False),
            Spot(0, 5, False)
        ]
        colorBlobs = [
            ColorBlob(3,1,False),
            ColorBlob(4,3,True),
            ColorBlob(4,5,True)
        ]
        hazards = [
            Hazard(1, 1, False),
            Hazard(3,3, True),
            Hazard(4, 2, True),
            Hazard(7, 7, True),
            Hazard(7,6,True),
            Hazard(7, 5, True),
        ]

        mapInstance = addOn.mapInstance
        mapInstance.set_map_length(cols, rows)
        mapInstance.set_robot_coord(robotCoord)
        mapInstance.set_spots(spots)
        mapInstance.set_hazards(hazards)
        mapInstance.set_color_blobs(colorBlobs)
        addOn.robotController.set_current_position(robotCoord)
    # --------------------------------------------------------
    else:
        operatorInterface = OperatorInterface(addOn.mapInstance)
        operatorInterface.run()

    # 경로 계산
    mapInstance = addOn.mapInstance
    robotCoord = mapInstance.get_robot_coord()
    addOn.robotController.set_current_position(robotCoord)
    addOn.set_path()

    # 초기 맵 상태 출력
    print("\tMap initialized...")
    mapInstance.print_full_map("Initial")

    # GUI로 표시
    addOn.display = Display(addOn)
    addOn.display.run()

    # 최종 맵 상태 출력
    print("\n⭐ All Spots Have Been Explored!\n")
    mapInstance.print_full_map("Final")
    print("\n\tExiting... Good bye!")
