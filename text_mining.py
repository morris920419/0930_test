"""中文文字探勘範例：斷詞 -> 去停用詞 -> 詞頻統計 -> 文字雲。"""
import argparse
import os
import re
from collections import Counter

import jieba
from wordcloud import WordCloud

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 常見中文字型路徑（依序尋找），也可用 --font 自行指定
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",                # macOS
    "/System/Library/Fonts/STHeiti Medium.ttc",          # macOS
    "C:/Windows/Fonts/msjh.ttc",                         # Windows 微軟正黑體
    "C:/Windows/Fonts/msyh.ttc",                         # Windows 微軟雅黑
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",      # Linux
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",    # Linux
]


def find_font(user_font=None):
    if user_font:
        return user_font
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    raise SystemExit("找不到中文字型，請用 --font 指定 .ttf/.ttc/.otf 字型檔路徑。")


def load_stopwords(path):
    with open(path, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def tokenize(text, stopwords):
    """斷詞並過濾：停用詞、標點符號、空白、單字詞。"""
    words = []
    for w in jieba.lcut(text):
        w = w.strip()
        if not w or w in stopwords:
            continue
        if not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", w):  # 純標點
            continue
        if len(w) < 2:  # 單字通常資訊量低
            continue
        words.append(w)
    return words


def main():
    p = argparse.ArgumentParser(description="中文文字探勘範例")
    p.add_argument("--input", default=os.path.join(BASE_DIR, "data", "sample.txt"))
    p.add_argument("--stopwords", default=os.path.join(BASE_DIR, "data", "stopwords.txt"))
    p.add_argument("--output", default=os.path.join(BASE_DIR, "output"))
    p.add_argument("--top", type=int, default=20, help="顯示前幾個高頻詞")
    p.add_argument("--font", help="中文字型檔路徑")
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    with open(args.input, encoding="utf-8") as f:
        text = f.read()
    stopwords = load_stopwords(args.stopwords)

    words = tokenize(text, stopwords)
    counter = Counter(words)
    top = counter.most_common(args.top)

    print(f"斷詞後共 {len(words)} 個詞（不重複 {len(counter)} 個）\n")
    print(f"前 {args.top} 個高頻詞：")
    for rank, (w, c) in enumerate(top, 1):
        print(f"{rank:>2}. {w}\t{c}")

    # 存成 CSV，方便用 Excel 開啟（utf-8-sig 避免亂碼）
    csv_path = os.path.join(args.output, "top_words.csv")
    with open(csv_path, "w", encoding="utf-8-sig") as f:
        f.write("排名,詞彙,次數\n")
        for rank, (w, c) in enumerate(top, 1):
            f.write(f"{rank},{w},{c}\n")

    font = find_font(args.font)
    wc = WordCloud(
        font_path=font, width=1000, height=600,
        background_color="white", max_words=100,
    ).generate_from_frequencies(counter)
    img_path = os.path.join(args.output, "wordcloud.png")
    wc.to_file(img_path)

    print(f"\n已輸出：{csv_path}\n已輸出：{img_path}")


if __name__ == "__main__":
    main()
