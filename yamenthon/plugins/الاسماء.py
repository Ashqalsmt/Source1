import re
import asyncio
import calendar
import json
import os
from telethon import events
from asyncio.exceptions import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ExportChatInviteRequest
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import get_user_from_event, sanga_seperator
from bs4 import BeautifulSoup
from ..helpers.utils import _format
from datetime import datetime
from urllib.parse import quote
import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from yamenthon.utils import admin_cmd
from ..helpers import AioHttp
from ..helpers.utils import _catutils, _format, reply_id
LOGS = logging.getLogger(__name__)
from yamenthon import zedub
START_FLAG_FILE = "sangmata_started.json"

def has_started():
    return os.path.exists(START_FLAG_FILE)

def set_started():
    with open(START_FLAG_FILE, "w") as f:
        json.dump({"started": True}, f)

@zedub.on(admin_cmd(pattern="الاسماء(ألف)?(?:\s|$)([\s\S]*)"))
async def _(zedub):
    input_str = "".join(zedub.text.split(maxsplit=1)[1:])
    reply_message = await iqthon.get_reply_message()
    if not input_str and not reply_message:
        return await edit_delete(iqthon, "**♛ ⦙ قم بالـرد على رسالـة لمستخـدم ...**")

    user, rank = await get_user_from_event(iqthon, secondgroup=True)
    if not user:
        return

    uid = user.id
    chat = "@SangMata_BOT"
    iqevent = await edit_or_reply(iqthon, "**♛ ⦙ جـاري المعالجـة ↯**")

    async with iqthon.client.conversation(chat) as conv:
        try:
            # نرسل /start فقط إذا ما قد أرسلناه قبل
            if not has_started():
                await conv.send_message("/start")
                await asyncio.sleep(0.5)
                set_started()

            # نرسل الآيدي مباشرة
            await conv.send_message(str(uid))

        except YouBlockedUserError:
            return await edit_delete(iqthon, "**♛ ⦙ قم بإلغـاء حظـر @SangMata_BOT ثم حـاول !!**")

        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)

        await zedub.client.send_read_acknowledge(conv.chat_id)

    if not responses:
        return await edit_delete(iqthon, "**♛ ⦙ لا يستطيـع البـوت جلـب النتائـج ⚠️**")
    if "No records found" in responses:
        return await edit_delete(iqthon, "**♛ ⦙ المستخـدم ليـس لديـه أيّ سجـل ✕**")

    names, usernames = await sanga_seperator(responses)
    cmd = zedub.pattern_match.group(1)
    sandy = None
    check = usernames if cmd == "u" else names
    for i in check:
        if sandy:
            await iqthon.reply(i, parse_mode=_format.parse_pre)
        else:
            sandy = True
            await iqevent.edit(i, parse_mode=_format.parse_pre)
