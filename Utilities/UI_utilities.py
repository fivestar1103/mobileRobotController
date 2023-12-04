# 색깔 테마
COLOR1 = "#79D6F7"
COLOR2 = "#F7F079"
COLOR3 = "#A0374A"
COLOR4 = "#3C6575"


# 화면 중앙에 창을 배치하는 함수
def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(window.winfo_screenheight() / 2 - window_height / 2)
    window.geometry("+{}+{}".format(position_right, position_down))
