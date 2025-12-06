'''


import time
import csv
import os
import pyautogui
import pyperclip
from PIL import Image

# ========== 1. 配置区域（用你自己的坐标替换） ==========

# 目前暂时不截取图片，先把图片区域配置整体注释掉
'''
IMAGE_REGION = {
    "left": 100,   # ← 换成你记录的“图片左上角 x”
    "top": 120,    # ← 图片左上角 y
    "right": 900,  # ← 图片右下角 x
    "bottom": 260  # ← 图片右下角 y
}
'''

# 各字段输入框的坐标（鼠标点击位置）
POS = {
    "pack_gross_weight": (1363, 751),  # 包装毛重
    "cost_price":        (1474, 853),  # 成本单价
    "country_freight":   (1391, 922),  # 国家运费显示区域

    "shipping_cost":     (1350, 892),  # 固定运费
    "collect_url":       (1530, 725),  # 采集网址

    "order_url":         (1532, 759),  # 下单采购
    "people":            (1399, 863),  # 适用人群
    "age_group":         (1734, 865),  # 年龄分组
    "title":             (1556, 753),  # 产品标题
    "bullet_points":     (1522, 579),  # 要点说明
    "description":       (1519, 435),  # 产品描述
}

# 导出的 CSV 文件名
CSV_FILE = "erp_products.csv"

# 截图保存目录（现在不用，但先保留）
IMAGE_DIR = "product_images"

# ========== 2. 工具函数 ==========

def click_and_copy(x, y, multiline=False):
    """点击指定位置，Ctrl+A 然后 Ctrl+C，返回剪贴板文字"""
    pyautogui.click(x, y)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.4)
    text = pyperclip.paste()
    if multiline:
        return text.strip()
    else:
        # 单行：去掉换行，避免 CSV 里乱行
        return text.strip().replace("\r", "").replace("\n", " ")

# 截图函数也整体注释掉，后面不再调用
'''
def grab_image(product_id):
    """截取图片区域，保存成文件，返回文件路径"""
    w = IMAGE_REGION["right"] - IMAGE_REGION["left"]
    h = IMAGE_REGION["bottom"] - IMAGE_REGION["top"]
    img = pyautogui.screenshot(
        region=(IMAGE_REGION["left"], IMAGE_REGION["top"], w, h)
    )
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    filename = os.path.join(IMAGE_DIR, f"{product_id}.png")
    img.save(filename)
    return filename
'''

# ========== 3. 主逻辑 ==========

def main():
    print("请在 5 秒内切换到 ERP 产品编辑页面，并不要再动鼠标和键盘。")
    time.sleep(5)

    # 先拿标题，当成 product_id
    title = click_and_copy(*POS["title"], multiline=False)
    product_id = title[:20].replace(" ", "_") or "product"

    data = {}

    data["产品标题"] = title
    data["包装毛重"] = click_and_copy(*POS["pack_gross_weight"])
    data["成本单价"] = click_and_copy(*POS["cost_price"])
    data["国家运费"] = click_and_copy(*POS["country_freight"], multiline=True)
    data["固定运费"] = click_and_copy(*POS["shipping_cost"])       # 用 shipping_cost 取“固定运费”
    data["采集网址"] = click_and_copy(*POS["collect_url"])
    data["下单采购"] = click_and_copy(*POS["order_url"])
    data["适用人群"] = click_and_copy(*POS["people"])
    data["年龄分组"] = click_and_copy(*POS["age_group"])
    data["要点说明"] = click_and_copy(*POS["bullet_points"], multiline=True)
    data["产品描述"] = click_and_copy(*POS["description"], multiline=True)

    # ===== 这里开始：原来是截图，现在先不用截图 =====
    # image_path = grab_image(product_id)
    # data["图片文件"] = image_path

    # 为了以后方便扩展，这里仍然保留“图片文件”字段，但先写空字符串
    image_path = ""
    data["图片文件"] = image_path
    # ===== 截图相关逻辑到此结束 =====

    # 写入 / 追加到 CSV
    file_exists = os.path.exists(CSV_FILE)
    fieldnames = [
        "产品标题",
        "包装毛重",
        "成本单价",
        "国家运费",
        "固定运费",   # 对应 shipping_cost
        "采集网址",
        "下单采购",
        "适用人群",
        "年龄分组",
        "要点说明",
        "产品描述",
        "图片文件",
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    print("✅ 采集完成，已写入：", CSV_FILE)
    # 现在不截图了，就不再打印截图信息
    # print("🖼 截图保存为：", image_path)

if __name__ == "__main__":
    main()

    

'''
























import time
import csv
import os
import pyautogui
import pyperclip
from PIL import Image

# ========== 1. 配置区域 ==========

# 暂时不截图片，如后续要用再打开
'''
IMAGE_REGION = {
    "left": 100,
    "top": 120,
    "right": 900,
    "bottom": 260
}
'''

# 各字段输入框的坐标（鼠标点击位置）
# ⚠️ 坐标要对应「字段在屏幕上的位置」，
#    第几屏没关系，只要你在那一屏时手动量的就行
POS = {
    # 第一次滚 9 次后能看到的字段（第 1 屏）
    "pack_gross_weight": (1365, 247),  # 包装毛重
    "cost_price":        (1471, 357),  # 成本单价
    "country_freight":   (1395, 422),  # 国家运费
    "shipping_cost":     (1352, 392),  # 固定运费
    "collect_url":       (1525, 725),  # 采集网址
    "order_url":         (1526, 756),  # 下单采购
    "people":            (1404, 864),  # 适用人群
    "age_group":         (1737, 868),  # 年龄分组

    # 第二次滚 9 次后能看到的字段（第 2 屏）
    "title":             (1505, 727),  # 产品标题
    "bullet_points":     (1558, 998),  # 要点说明

    # 第三次再滚 4 次后能看到的字段（第 3 屏）
    "description":       (1551, 902),  # 产品描述
}

# 导出的 CSV 文件名
CSV_FILE = "erp_products.csv"

# 截图保存目录（现在不用，但先保留）
IMAGE_DIR = "product_images"

# 滚动区域点击位置（能滚动内容的区域）
SCROLL_CLICK_POS = (1600, 502)   # 你测试滚动时用的坐标
SCROLL_AMOUNT = -1000            # 你测试成功的滚动值

# ========== 2. 工具函数 ==========

def click_and_copy(x, y, multiline=False):
    """点击指定位置，Ctrl+A 然后 Ctrl+C，返回剪贴板文字"""
    pyautogui.click(x, y)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.4)
    text = pyperclip.paste()
    if multiline:
        return text.strip()
    else:
        # 单行：去掉换行，避免 CSV 乱行
        return text.strip().replace("\r", "").replace("\n", " ")

# 截图函数先注释掉
'''
def grab_image(product_id):
    w = IMAGE_REGION["right"] - IMAGE_REGION["left"]
    h = IMAGE_REGION["bottom"] - IMAGE_REGION["top"]
    img = pyautogui.screenshot(
        region=(IMAGE_REGION["left"], IMAGE_REGION["top"], w, h)
    )
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    filename = os.path.join(IMAGE_DIR, f"{product_id}.png")
    img.save(filename)
    return filename
'''

def scroll_times(times):
    """滚动指定次数（用你已经测好的 SCROLL_AMOUNT）"""
    pyautogui.click(*SCROLL_CLICK_POS)
    time.sleep(0.2)
    for i in range(times):
        pyautogui.scroll(SCROLL_AMOUNT)
        time.sleep(0.2)  # 给界面一点反应时间

# ========== 3. 主逻辑 ==========

def main():
    print("请在 5 秒内切换到 ERP 产品编辑页面，并不要再动鼠标和键盘。")
    time.sleep(5)

    data = {}

    # ============ 第 1 屏：第一次滚 9 次 ============

    scroll_times(9)
    time.sleep(1)  # 等界面稳定

    data["包装毛重"] = click_and_copy(*POS["pack_gross_weight"])
    data["成本单价"] = click_and_copy(*POS["cost_price"])
    data["国家运费"] = click_and_copy(*POS["country_freight"], multiline=True)
    data["固定运费"] = click_and_copy(*POS["shipping_cost"])
    data["采集网址"] = click_and_copy(*POS["collect_url"])
    data["下单采购"] = click_and_copy(*POS["order_url"])
    data["适用人群"] = click_and_copy(*POS["people"])
    data["年龄分组"] = click_and_copy(*POS["age_group"])

    # ============ 第 2 屏：第二次再滚 9 次 ============

    scroll_times(9)
    time.sleep(1)

    data["产品标题"] = click_and_copy(*POS["title"])
    data["要点说明"] = click_and_copy(*POS["bullet_points"], multiline=True)

    # 这里顺便用标题生成一个 product_id（虽然你现在没用图片，但留着以后备份）
    title = data["产品标题"]
    product_id = title[:20].replace(" ", "_") or "product"

    # ============ 第 3 屏：第三次再滚 4 次 ============

    scroll_times(4)
    time.sleep(1)

    data["产品描述"] = click_and_copy(*POS["description"], multiline=True)

    # 图片先留空
    image_path = ""
    data["图片文件"] = image_path

    # ============ 写入 CSV ============

    file_exists = os.path.exists(CSV_FILE)
    fieldnames = [
        "产品标题",
        "包装毛重",
        "成本单价",
        "国家运费",
        "固定运费",
        "采集网址",
        "下单采购",
        "适用人群",
        "年龄分组",
        "要点说明",
        "产品描述",
        "图片文件",
    ]

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    print("✅ 采集完成，已写入：", CSV_FILE)

if __name__ == "__main__":
    main()
