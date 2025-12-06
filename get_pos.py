"测试获得鼠标位置坐标"
"运行之后，3s后开始测试，每3秒获取一次鼠标坐标，ctrl+c结束运行"



import pyautogui
import time

print("3 秒后开始，每 3 秒打印一次鼠标位置，按 Ctrl+C 结束。")
time.sleep(3)

try:
    while True:
        x, y = pyautogui.position()
        print(f"当前鼠标位置: ({x}, {y})")
        time.sleep(3)
except KeyboardInterrupt:
    print("结束")