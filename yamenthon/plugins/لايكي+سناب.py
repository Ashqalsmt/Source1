#الملف حقوق وكتابه الاسطوره عاشق الصمت 
#تبي تخمط الملف تابع لسورس يمنثون 
#احترم عقلك وكتب كود تحميـل ترا سهل 
#بس شغلكم تخميط بس ههههه😂
#خذ الكود عادي بس لا تقول انه تبعك

from .. import zedub
from ..core.managers import edit_or_reply
from telethon import events
import aiohttp
import re

# ================== إعدادات API ==================
LIKEE_API_URL = "https://likee-video-downloader-without-watermark.p.rapidapi.com/likee"
LIKEE_API_KEY = "75e4c64b61mshf5ca7e24bacfaa5p1d45e2jsn27e7d689dd7f"

SNAPCHAT_API_URL = "https://snapchat-video-downloader.p.rapidapi.com/snapchat"
SNAPCHAT_API_KEY = "75e4c64b61mshf5ca7e24bacfaa5p1d45e2jsn27e7d689dd7f"

# ================== دالة جلب البيانات ==================
async def fetch_api(url, headers=None, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            return None

# ================== تحميل من Likee ==================
@zedub.zed_cmd(pattern=r"لايكي(?:\s+|$)(.*)")
async def likee_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")

    if not link or "likee.video" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط لايكي بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من لايكي...")

    headers = {
        "X-RapidAPI-Key": LIKEE_API_KEY,
        "X-RapidAPI-Host": "likee-video-downloader-without-watermark.p.rapidapi.com"
    }
    params = {"url": link}

    data = await fetch_api(LIKEE_API_URL, headers=headers, params=params)
    if not data or not data.get("video"):
        return await zed.edit("⚠️ لم أستطع جلب الفيديو من لايكي.")

    await event.client.send_file(
        event.chat_id,
        data["video"],
        caption="📥 تم التحميل من **Likee**"
    )
    await zed.delete()

# ================== تحميل من Snapchat ==================
@zedub.zed_cmd(pattern=r"سناب(?:\s+|$)(.*)")
async def snapchat_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")

    if not link or "snapchat.com" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط سناب شات بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من سناب شات...")

    headers = {
        "X-RapidAPI-Key": SNAPCHAT_API_KEY,
        "X-RapidAPI-Host": "snapchat-video-downloader.p.rapidapi.com"
    }
    params = {"url": link}

    data = await fetch_api(SNAPCHAT_API_URL, headers=headers, params=params)
    if not data or not data.get("video"):
        return await zed.edit("⚠️ لم أستطع جلب الفيديو من سناب شات.")

    await event.client.send_file(
        event.chat_id,
        data["video"],
        caption="📥 تم التحميل من **Snapchat**"
    )
    await zed.delete()
