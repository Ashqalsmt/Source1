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
import json

#  إعدادات API
APIFY_TOKEN = "apify_api_sE44lke7pdJwXQTlIah28sHv3Jp5dw3EjYgD"
APIFY_SNAP_URL = "https://api.apify.com/v2/acts/bytepulselabs~snapchat-video-downloader/run-sync-get-dataset-items?token=" + APIFY_TOKEN

LIKEE_API_URL = "https://likee-downloader-video.p.rapidapi.com/"
LIKEE_API_HOST = "likee-downloader-video.p.rapidapi.com"
RAPIDAPI_KEY = "75e4c64b61mshf5ca7e24bacfaa5p1d45e2jsn27e7d689dd7f"

async def fetch_json(url, method="GET", headers=None, json_data=None):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(url, headers=headers) as resp:
                return await resp.json(), resp.status
        else:
            async with session.post(url, headers=headers, json=json_data) as resp:
                return await resp.json(), resp.status

@zedub.zed_cmd(pattern=r"سناب(?:\s+|$)(.*)")
async def snapchat_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")
    if not link or "snapchat.com" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط سناب شات بعد الأمر أو بالرد عليه.")
    zed = await edit_or_reply(event, "⏳ جاري التحميل من سناب شات...")
    payload = {
        "urls":[{"url": link}],
        "quality":"480",
        "proxy":{"useApifyProxy": False}
    }
    data, status = await fetch_json(APIFY_SNAP_URL, method="POST", json_data=payload)
    if status != 200 or not data or not isinstance(data, dict) or not data.get("items"):
        return await zed.edit("⚠️ لم أستطع جلب الفيديو من سناب شات.")
    # البيانات ترجع كمصفوفة داخل "items" تحمل `videoUrl`
    item = data["items"][0]
    video_url = item.get("videoUrl") or item.get("video")
    if not video_url:
        return await zed.edit("⚠️ الفيديو غير متاح.")
    await event.client.send_file(event.chat_id, video_url, caption="📥 تم التحميل من سناب شات")
    await zed.delete()

@zedub.zed_cmd(pattern=r"لايكي(?:\s+|$)(.*)")
async def likee_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")
    if not link or "likee.video" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط فيديو لايكي بعد الأمر أو بالرد عليه.")
    zed = await edit_or_reply(event, "⏳ جاري التحميل من لايكي...")
    headers = {
        "x-rapidapi-host": LIKEE_API_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {"url": link}
    data, status = await fetch_json(LIKEE_API_URL, method="GET", headers=headers, json_data=None)
    if status != 200 or not data or not data.get("video"):
        return await zed.edit("⚠️ لم أستطع تنزيل الفيديو من لايكي.")
    await event.client.send_file(event.chat_id, data["video"], caption="📥 تم التحميل من لايكي")
    await zed.delete()
