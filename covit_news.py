# coding:utf-8
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json
import os
import requests


# 更新を通知する
def new_bs():
    url = "https://www.pref.akita.lg.jp/pages/archive/47957"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    old_file = "covit_news.txt"

    # 今回取り込んだ情報を取り出す
    new_elem = str(soup.select(".p-page-title"))

    # 前回のデータを取り込む
    try:
        with open(old_file) as f:
            old_elem = f.read()
    except:
        old_elem = ""

    if new_elem == old_elem:
        return False
    else:
        with open(old_file, "w") as f:
            f.write(new_elem)
        return True


# メッセージを送る
def send_message(talk):
    # メッセージ送信用に変換
    message = TextSendMessage(text=talk)
    access_token = os.environ['ACCESS_TOKEN']
    user_id = os.environ['LINE_ID']
    # LINEbotにトークンを入力
    line_bot_api = LineBotApi(access_token)
    # LINEbotでメッセージを送る
    # line_bot_api.push_message(user_id, messages=message)
    # bot友達の全員に送信
    line_bot_api.broadcast(messages=message)


# 自分にだけメッセージを送る
def send_me_message(talk):
    # メッセージ送信用に変換
    message = TextSendMessage(text=talk)
    # jsonファイルを読み込む
    file = open('info.json', 'r')
    info = json.load(file)
    access_token = info["CHANNEL_ACCESS_TOKEN"]
    user_id = info["USER_ID"]
    # LINEbotにトークンを入力
    line_bot_api = LineBotApi(access_token)
    # LINEbotでメッセージを送る
    line_bot_api.push_message(user_id, messages=message)
    # bot友達の全員に送信
    # line_bot_api.broadcast(messages=message)


# 感染者情報が更新されたら通知
def info_get():
    url = "https://www.pref.akita.lg.jp/pages/archive/47957"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    old_file = "covit_info.txt"

    # 今回取り込んだ情報を取り出す
    new_elem = soup.select(
        "#top > div.l-site-container > main > article > div > div.p-page-body > table > tbody")

    # 前回のデータを取り込む
    try:
        with open(old_file) as f:
            old = f.read()
    except:
        old = ""

    # スクレイピングデータの取得
    datas = new_elem[0].select("tr")
    # 一番最初の症例数のみ取得
    first_data = datas[0].select("td")[0].get_text()

    # 前回取り込んだ症例数と違う場合のみ実行
    if first_data == old:
        return False
    else:
        # 送る内容を保存する
        memory = ""
        place = {}
        for data in datas:
            count_num = data.select("td")[0].get_text()
            man_old = data.select("td")[2].get_text()
            area = data.select("td")[4].get_text()

            # 症例数が前回取り込んだ数と同じになるまで実行
            if count_num != old and old != "":
                memory += f"{count_num}\s{man_old}\s{area}\n"
                # 保健所管内の人数を計算
                if area in place:
                    place[area] += 1
                else:
                    place[area] = 1
            else:
                break

        # 更新された番号を保存
        with open(old_file, "w") as f:
            f.write(first_data)

        # トータルの人数を出力
        total = ""
        total_sum = 0
        for k, v in place.items():
            total += f"{k}:{v}人\n"
            total_sum += v
        total_sum = f"\n秋田県内合計：{str(total_sum)}人\n"

        # 最後にURLを送る内容に保存してメッセージを送信
        message = memory + total_sum + total + url
        send_message(message)
        # print(message)

# テスト用として実行して通知させない


def info_test():
    url = "https://www.pref.akita.lg.jp/pages/archive/47957"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    old_file = "covit_info.txt"

    # 今回取り込んだ情報を取り出す
    new_elem = soup.select(
        "#top > div.l-site-container > main > article > div > div.p-page-body > table > tbody")

    # 前回のデータを取り込む
    try:
        with open(old_file) as f:
            old = f.read()
    except:
        old = ""

    # スクレイピングデータの取得
    datas = new_elem[0].select("tr")
    # 一番最初の症例数のみ取得
    first_data = datas[0].select("td")[0].get_text()

    # 前回取り込んだ症例数と違う場合のみ実行
    if first_data == old:
        return False
    else:
        # 送る内容を保存する
        memory = ""
        place = {}
        for data in datas:
            count_num = data.select("td")[0].get_text()
            man_old = data.select("td")[2].get_text()
            area = data.select("td")[4].get_text()

            # 症例数が前回取り込んだ数と同じになるまで実行
            if count_num != old and old != "":
                memory += f"{count_num} {man_old}　{area}\n"
                # 保健所管内の人数を計算
                if area in place:
                    place[area] += 1
                else:
                    place[area] = 1
            else:
                break

        # 更新された番号を保存
        with open(old_file, "w") as f:
            f.write(first_data)

        # トータルの人数を出力
        total = ""
        total_sum = 0
        for k, v in place.items():
            total += f"{k}:{v}人\n"
            total_sum += v
        total_sum = f"\n秋田県内合計：{str(total_sum)}人\n"

        # 内容を保存してメッセージを表示
        message = memory + total_sum + total + url
        print(message)


if __name__ == "__main__":
    mess = "おはようございます。\n秋田コロナ感染者情報の作成者のJunです。\n\n昨日は誤った情報をお送りしてしまい申し訳ございませんでした。\n人数計算を追加した際のバグが原因でした。現在は修正を行い、最後にお送りした内容が正しい情報となりますのでご確認ください。\n\nまた、なにか不具合、お問い合わせなどある際には jun.mermaid.voice@gmail.com までご連絡をお願いします。"
    send_me_message(mess)
    # send_message(mess)
    # info_test()
