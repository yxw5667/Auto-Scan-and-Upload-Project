import time
import pyautogui

# ⚠️ 这里填“ERP 内容区”能滚动的坐标，例如页面中间的空白处
SCROLL_CLICK_POS = (1600, 502)  # ← 你要改成你的坐标

# 滚动值（负数向下滚，正数向上滚）
SCROLL_AMOUNT = -1000


def test_scroll(times):
    """
    测试滚动效果，不采集任何数据。
    times = 滚动次数
    """
    print(f"⏳ 程序将在 3 秒后开始滚动 {times} 次，请把鼠标移开不要动。")
    time.sleep(3)

    # 点击内容区
    pyautogui.click(*SCROLL_CLICK_POS)
    time.sleep(0.5)

    for i in range(times):
        pyautogui.scroll(SCROLL_AMOUNT)
        time.sleep(1)  # 给界面时间加载 & 停住
        print(f"✔ 已滚动 {i+1} 次")

    print("🎉 滚动测试结束！")


# ======= 你要测试几次就在这里改 =======
if __name__ == "__main__":
    test_scroll(9)     # ← 这里填 1、2、3、4 都可以
