from playwright.sync_api import sync_playwright
from pathlib import Path
import json


ARTIST_LIST_URL = "https://www.kuwo.cn/singers"
BASE_DIR = Path(__file__).resolve().parent.parent
output_path = BASE_DIR / "data" / "artist_names_stage1.json"

def read_names_from_locator(name_elements, label):

    names = []

    count = name_elements.count()
    print(label, "数量：", count)


    for i in range(count):
        name_element = name_elements.nth(i)
        name = name_element.inner_text().strip()
        if name != "":
            names.append(name)
    return names


def get_artist_names_from_current_page(page):
    page.wait_for_selector(
    ".artist_con .artist .text, .artist_other .artist_line.flex_c .name span")

    big_name_elements = page.locator(".artist_con .artist .text")
    small_name_elements = page.locator(".artist_other .artist_line.flex_c .name")

    big_names = read_names_from_locator(big_name_elements, "大卡片歌手")
    small_names = read_names_from_locator(small_name_elements, "小卡片歌手")


    all_names = []
    all_names.extend(big_names)
    all_names.extend(small_names)

    return all_names


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500
    )

    page = browser.new_page()

    page.goto(ARTIST_LIST_URL, wait_until="networkidle")

    page1_names = get_artist_names_from_current_page(page)

    print("\n第一页歌手数量：", len(page1_names))
    print("第一页前 5 个：")
    for name in page1_names[:5]:
        print(name)

    print("\n准备点击第二页...")
    page.locator(".page-wrap span").filter(has_text="2").first.click()
    page2_names = get_artist_names_from_current_page(page)


    print("\n第二页歌手数量：", len(page2_names))
    print("第二页前 5 个：")
    for name in page2_names[:5]:
        print(name)

    browser.close()

    all_names = []
    all_names.extend(page1_names)
    all_names.extend(page2_names)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_names, f, ensure_ascii=False, indent=2)
