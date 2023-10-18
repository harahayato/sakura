import re
import os
import pandas as pd

# 日付行で分割
def get_date_content(text):
    # 正規表現を修正し、正しく戻り値を返すように修正
    re_date = re.compile(r"\n((\d{4})/(\d{2})/(\d{2})\(([月火水木金土日])\))\n(\d{2}:\d{2}\t.+?)(?=\n\d{4}/\d{2}/\d{2}\([月火水木金土日]\))", re.DOTALL)
    text = f"\n{text}\n1900/01/01(月)\n00:00\t"  # 最初と最後の要素をfindallできるように日付業を末尾で足す

    # 正規表現にマッチする要素を抽出
    contents = re_date.findall(text)
    logs = []
    for datestr, year, month, day, weekday, content in contents:
        obj = {
            "datestr": datestr,
            "year": year,
            "month": month,
            "day": day,
            "weekday": weekday,
            "content": content
        }
        logs.append(obj)

    return logs

# 時刻で分割
def get_time_content(text):
    # 正規表現を修正し、正しく戻り値を返すように修正
    re_time = re.compile(r"(?<=\n)(\d{2}:\d{2})\t(.+?)(?=\n\d{2}:\d{2}\t)", re.DOTALL)
    text = f"\n{text}\n00:00\t"  # 最初と最後の要素をfindallできるように時刻から始まる行を足す

    # 正規表現にマッチする要素を抽出
    contents = re_time.findall(text)
    logs = []
    for timestr, content in contents:
        obj = {
            "timestr": timestr,
            "content": content
        }
        logs.append(obj)

    return logs

# 時刻に紐づくcontentから名前と投稿文字列を取得
def get_name_and_post(text):
    post = text.split("\t")

    if len(post) == 1:
        name = "system"
        content = post[0]
    else:
        name = post[0] if post[0] else "system"
        content = "\t".join(post[1:])

    return {
        "name": name,
        "content": content
    }

# 投稿の種類を決定し、必要な情報と合わせて返す
def parse_post(content):
    re_url = re.compile(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)")

    log = {
        "param0_key": "",
        "param0_val": "",
        "param1_key": "",
        "param1_val": ""
    }

    if re.fullmatch(r"\[(?:ファイル|スタンプ|写真|動画|ボイスメッセージ|連絡先|プレゼント)\]", content):
        log["send_type"] = content[1:-1]
    elif content == "[アルバム] (null)":
        log["send_type"] = "アルバム"
    elif content.startswith("[位置情報]"):
        log["send_type"] = "位置情報"
    elif content.startswith("[ノート] "):
        log["send_type"] = "ノート"
    elif re.fullmatch(r"☎ 通話時間 \d+:\d+", content):
        phone_time = content.split(" ")[-1].split(":")
        phone_sec = int(phone_time[0]) * 60 + int(phone_time[1])
        log.update({
            "send_type": "phone_start",
            "param0_key": "phone_sec",
            "param0_val": phone_sec
        })
    elif content == "☎ 通話をキャンセルしました":
        log.update({
            "send_type": "phone_cancel"
        })
    else:
        urls = re_url.findall(content)
        log.update({
            "send_type": "text",
            "param0_key": "url_num",
            "param0_val": len(urls),
            "param1_key": "url_remove_length",
            "param1_val": len(content) + len(urls) - sum([len(url) for url in urls])
        })

    log["length"] = len(content)
    return log

# lineのトーク履歴から各投稿の情報を抽出する
def parse_linelog(textdata):
    logs = []
    for date_content_info in get_date_content(textdata):
        date_content = date_content_info.pop("content")
        date_info = {
            "year": date_content_info.pop("year"),
            "month": date_content_info.pop("month"),
            "day": date_content_info.pop("day"),
            "weekday": date_content_info.pop("weekday"),
            "datestr": date_content_info.pop("datestr")
        }
        for time_content_info in get_time_content(date_content):
            time_content = time_content_info.pop("content")
            time_info = {
                "timestr": time_content_info.pop("timestr")
            }
            name_and_post_info = get_name_and_post(time_content)
            name = name_and_post_info.pop("name")
            post = name_and_post_info.pop("content")
            postinfo = parse_post(post)
            post_no_tab_and_br = "<br>".join(post.replace("\t", "<tab>").splitlines())
            log = {}
            log.update(date_info)
            log.update(time_info)
            log.update({
                "name": name,
                "content": post,
                "send_type": postinfo.pop("send_type"),
                "length": postinfo.pop("length"),
                "content_no_tab_and_br": post_no_tab_and_br,
                "param0_key": postinfo.pop("param0_key"),
                "param0_val": postinfo.pop("param0_val"),
                "param1_key": postinfo.pop("param1_key"),
                "param1_val": postinfo.pop("param1_val")
            })
            logs.append(log)
    
    return logs

# チャットログファイルのパスを指定
PATH = "ichiha-talk.txt"

# ファイルを読み込んでtextdataに格納
with open(PATH, "r", encoding='UTF-8') as f:
    textdata = f.read()

# DataFrameのカラム名を定義
header = ["datestr", "timestr", "name", "content_no_tab_and_br", "send_type", "year", "month", "day", "weekday", "timestr", "length", "param0_key", "param0_val", "param1_key", "param1_val"]

# LINEのチャットログのパース結果を取得
logs = parse_linelog(textdata)

# データをDataFrameに変換
df = pd.DataFrame({k: [v.get(k, "") for v in logs] for k in header})

# カラム名を変更（content_no_tab_and_brをcontentに変更）
df = df.rename(columns={"content_no_tab_and_br": "content"})

# 結果を保存
df.to_csv("log.tsv", sep="\t", index=False, header=True, encoding='utf-8')