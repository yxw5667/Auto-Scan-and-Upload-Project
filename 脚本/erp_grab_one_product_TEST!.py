import time
import csv
import os
import pyautogui
import pyperclip
from PIL import Image

# ========== 1. 配置区域 ==========

# 各字段输入框的坐标（鼠标点击位置）
# 坐标保持你提供的，不进行修改
POS = {
    # 第一次滚 9 次后的字段（第 1 屏）
    "pack_gross_weight": (1365, 247),  # 包装毛重
    "cost_price":        (1471, 357),  # 成本单价
    "country_freight":   (1395, 422),  # 国家运费
    "shipping_cost":     (1352, 392),  # 固定运费
    "collect_url":       (1525, 725),  # 采集网址
    "order_url":         (1526, 756),  # 下单采购（模板不需要）
    "people":            (1404, 864),  # 适用人群
    "age_group":         (1737, 868),  # 年龄分组（模板不需要）

    # 第二次滚 9 次后的字段（第 2 屏）
    "title":             (1505, 727),  # 产品标题
    "bullet_points":     (1558, 998),  # 要点说明

    # 第三次滚 4 次后的字段（第 3 屏）
    "description":       (1551, 902),  # 产品描述
}

# 导出的 CSV 文件名（严格对应 ERP 导入模板）
CSV_FILE = "导入产品模板_自动生成.csv"

# 滚动配置
SCROLL_CLICK_POS = (1600, 502)
SCROLL_AMOUNT = -1000  # 你的 ERP 测试确定滚动值

# 导入模板列名（不能改）
TEMPLATE_COLUMNS = [
    "父SKU(必填)",
    "SKU",
    "成人",
    "颜色",
    "尺码",
    "品牌",
    "分类",
    "中文简称",
    "英文简称",
    "库存",
    "币种",
    "成本价(必填)",
    "运费",
    "挂号模板",
    "海关编码",
    "申报价(美元)",
    "分销价",
    "毛重(克)",
    "包装尺寸",
    "适用人群",
    "材料",
    "包装材料",
    "金属",
    "珠宝",
    "语言",
    "标题(必填)",
    "关键字",
    "要点1",
    "要点2",
    "要点3",
    "要点4",
    "要点5",
    "简介",
    "产品图",
    "简介图",
    "参考网址",
    "安全等级",
    "产品级别",
]

# ========== 2. 工具函数 ==========

def click_and_copy(x, y, multiline=False):
    """点击 → Ctrl+A → Ctrl+C → 返回内容"""
    pyautogui.click(x, y)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.4)
    text = pyperclip.paste()

    if multiline:
        return text.strip()
    return text.strip().replace("\r", "").replace("\n", " ")

def scroll_times(times):
    """滚动指定次数"""
    pyautogui.click(*SCROLL_CLICK_POS)
    for i in range(times):
        pyautogui.scroll(SCROLL_AMOUNT)
        time.sleep(0.2)

def split_bullet_points(text):
    """要点说明拆成 5 条"""
    if not text:
        return ["", "", "", "", ""]
    parts = [p.strip() for p in text.split("\n") if p.strip()]
    parts = parts[:5]
    while len(parts) < 5:
        parts.append("")
    return parts

# ========== 3. 主逻辑 ==========

def main():
    print("⚠️ 请在 5 秒内切换到 ERP 产品编辑页面，不要再动键鼠。")
    time.sleep(5)

    # ========== 第 1 屏：滚动 9 次 ==========
    scroll_times(9)
    time.sleep(1)

    pack_gross_weight = click_and_copy(*POS["pack_gross_weight"])
    cost_price        = click_and_copy(*POS["cost_price"])
    country_freight   = click_and_copy(*POS["country_freight"], multiline=True)
    fixed_shipping    = click_and_copy(*POS["shipping_cost"])
    collect_url       = click_and_copy(*POS["collect_url"])
    people            = click_and_copy(*POS["people"])

    # ========== 第 2 屏：滚动 9 次 ==========
    scroll_times(9)
    time.sleep(1)

    title         = click_and_copy(*POS["title"])
    bullet_text   = click_and_copy(*POS["bullet_points"], multiline=True)

    # ========== 第 3 屏：滚动 4 次 ==========
    scroll_times(4)
    time.sleep(1)

    description   = click_and_copy(*POS["description"], multiline=True)

    # ====== 拆分要点说明为 5 条 ======
    bp1, bp2, bp3, bp4, bp5 = split_bullet_points(bullet_text)

    # ========== 映射到模板列 ==========

    row = {col: "" for col in TEMPLATE_COLUMNS}

    # 你要求的固定字段
    row["库存"] = "20"
    row["币种"] = "CNY"

    # 映射关系（你指定）
    row["成本价(必填)"] = cost_price
    row["运费"] = fixed_shipping
    row["挂号模板"] = country_freight
    row["毛重(克)"] = pack_gross_weight
    row["适用人群"] = people
    row["标题(必填)"] = title
    row["简介"] = description
    row["参考网址"] = collect_url

    # 要点说明
    row["要点1"] = bp1
    row["要点2"] = bp2
    row["要点3"] = bp3
    row["要点4"] = bp4
    row["要点5"] = bp5

    # 图片列暂时留空
    row["产品图"] = ""
    row["简介图"] = ""

    # ========== 写入 CSV ==========
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print("✅ 已成功采集并按模板写入：", CSV_FILE)


if __name__ == "__main__":
    main()
