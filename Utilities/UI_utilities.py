# 색깔 테마
COLOR1 = "#ebe0ff"
COLOR2 = "#7151a9"
COLOR3 = "#660099"
COLOR4 = "#46325d"


# 화면 중앙에 창을 배치하는 함수
def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    position_right = int(window.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(window.winfo_screenheight() / 2 - window_height / 2)
    window.geometry("+{}+{}".format(position_right, position_down))
