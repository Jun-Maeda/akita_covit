# coding:utf-8
from bs4 import BeautifulSoup
import requests
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from covit_news import info_get

if __name__ == "__main__":
    info_get()
