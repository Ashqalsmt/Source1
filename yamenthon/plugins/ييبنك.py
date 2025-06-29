import random
from datetime import datetime
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon import events

from yamenthon import zedub
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus

temp = """{PING_TEXT}
┏━━━━━━━┓
┃ ✦ {ping}
┃ ✦ {mention}
┗━━━━━━━┛"""

plugin_category = "utils"


@zedub.zed_cmd(pattern="بنك(?:\s|$)([\s\S]*)")
async def jokerping(event):
    reply_to_id = await reply_id(event)
    start = datetime.now()
    await edit_or_reply(event, "** ᯽︙ يتـم التـأكـد من البنك انتـظر قليلا رجاءا**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✇ ◅"
    PING_TEXT = gvarstatus("PING_TEXT") or "**[ 𝗜 𝗝𝘂𝘀𝘁 𝗔𝘀𝗸𝗲𝗱 𝗙𝗼𝗿 𝗦𝗼𝗺𝗲 𝗣𝗲𝗮𝗰𝗲 🎀 ](t.me/YamenThon)**"
    PING_IMG = gvarstatus("PING_PIC") or Config.P_PIC or "https://telegra.ph/file/fb62d70ce09f4a78dfc86.jpg"
    HuRe_caption = gvarstatus("PING_TEMPLATE") or temp

    mention_user = f"[{event.sender.first_name}](tg://user?id={event.sender_id})"

    caption = HuRe_caption.format(
        PING_TEXT=PING_TEXT,
        EMOJI=EMOJI,
        mention=mention_user,
        ping=ms,
    )

    JEP = [x for x in PING_IMG.split()]
    if not JEP:
        return await edit_or_reply(event, "✖️ لا يوجد رابط صورة صالح.")
    PIC = random.choice(JEP)
    try:
        await event.client.send_file(
            event.chat_id, PIC, caption=caption, reply_to=reply_to_id
        )
        await event.delete()
    except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
        return await edit_or_reply(
            event,
            f"**الميـديا خـطأ **\nغـير الرابـط بأستـخدام الأمـر  \n `.اضف_فار ALIVE_PIC رابط صورتك`\n\n**لا يمـكن الحـصول عـلى صـورة من الـرابـط :-** `{PIC}`",
    )
