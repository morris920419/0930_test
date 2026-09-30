# 0930_test_文字探勘練習

一個簡單的中文文字探勘範例：

1. 讀取中文範例文章（`data/sample.txt`）
2. 使用 [jieba](https://github.com/fxsjy/jieba) 斷詞
3. 去除停用詞、標點符號與單字詞
4. 統計前 20 個高頻詞
5. 產生文字雲圖片

## 什麼是文字探勘？

文字探勘（Text Mining）是從大量非結構化文字中萃取有用資訊的技術。
常見流程為：**取得文字 → 斷詞 → 清理（停用詞）→ 統計／分析 → 視覺化**。
中文詞與詞之間沒有空白，所以必須先「斷詞」；「停用詞」是像「的、了、是」這類出現很多但沒有實質意義的詞，會先被移除，否則高頻詞榜單全是它們。

## 專案結構

```
├── text_mining.py     # 主程式
├── requirements.txt   # 相依套件
├── data/
│   ├── sample.txt     # 範例文章（可換成自己的文字）
│   └── stopwords.txt  # 停用詞表（一行一個，可自行增減）
└── output/            # 執行後產生
    ├── top_words.csv  # 高頻詞統計
    └── wordcloud.png  # 文字雲
```

## 執行方式

需要 Python 3.8 以上。

```bash
# 1. （建議）建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate        # Windows：.venv\Scripts\activate

# 2. 安裝套件
pip install -r requirements.txt

# 3. 執行
python text_mining.py
```

執行後終端機會顯示前 20 個高頻詞，並在 `output/` 產生 `top_words.csv` 與 `wordcloud.png`。

### 選用參數

| 參數 | 說明 | 預設 |
| --- | --- | --- |
| `--input` | 要分析的文字檔（UTF-8） | `data/sample.txt` |
| `--stopwords` | 停用詞檔 | `data/stopwords.txt` |
| `--output` | 輸出資料夾 | `output/` |
| `--top` | 顯示前幾個高頻詞 | `20` |
| `--font` | 中文字型檔路徑 | 自動尋找 |

例如分析自己的文章：

```bash
python text_mining.py --input my_article.txt --top 30
```

## 常見問題

- **文字雲出現方框或亂碼／出現「找不到中文字型」**：系統缺少中文字型。
  請用 `--font` 指定字型檔，例如
  `python text_mining.py --font "C:/Windows/Fonts/msjh.ttc"`；
  Linux 可先安裝 `fonts-noto-cjk` 或 `fonts-wqy-zenhei`。
- **某些詞斷得不理想**：可在程式中加入 `jieba.add_word("你的詞")`，
  或用 `jieba.load_userdict("dict.txt")` 載入自訂詞典。
- **高頻詞裡還有無意義的詞**：把它加進 `data/stopwords.txt` 即可。
- **想斷繁體中文更準確**：jieba 預設詞典偏簡體，可下載
  [繁體詞典](https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big)
  後以 `jieba.set_dictionary("dict.txt.big")` 使用。
