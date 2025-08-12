from .. import zedub
from ..core.managers import edit_or_reply
from telethon import events
import aiohttp
import re

# API مجانية
TIKTOK_API = "https://api.tiklydown.me/api/download"
INSTAGRAM_API = "https://saveinsta.io/core/ajax.php"

async def fetch_json(url, params=None, method="GET", data=None):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(url, params=params) as resp:
                return await resp.json()
        else:
            async with session.post(url, data=data) as resp:
                return await resp.text()

@zedub.zed_cmd(pattern="تيك(?:\s+|$)(.*)")
async def tiktok_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1) or (reply.text if reply else "")

    if not link or "tiktok.com" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط تيك توك بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من تيك توك...")
    try:
        data = await fetch_json(TIKTOK_API, params={"url": link})
        if data.get("status") != "success":
            return await zed.edit("⚠️ لم أستطع جلب الفيديو، تأكد من الرابط.")

        # فيديو
        if "video" in data:
            video_url = data["video"]["noWatermark"]
            await event.client.send_file(event.chat_id, video_url, caption="✅ تيك توك بدون علامة مائية")
        # صور
        elif "images" in data:
            for img in data["images"]:
                await event.client.send_file(event.chat_id, img, caption="📸 صورة من تيك توك")
        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")

@zedub.zed_cmd(pattern="انستا(?:\s+|$)(.*)")
async def insta_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1) or (reply.text if reply else "")

    if not link or not re.search(r"(instagram\.com|instagr\.am)", link):
        return await edit_or_reply(event, "📌 أرسل رابط إنستقرام بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من إنستقرام...")
    try:
        payload = {
            "q": link,
            "t": "media",
            "lang": "en"
        }
        html = await fetch_json(INSTAGRAM_API, method="POST", data=payload)

        # استخراج الروابط
        urls = re.findall(r'(https?://[^"\']+\.(?:jpg|mp4))', html)
        if not urls:
            return await zed.edit("⚠️ لم أستطع جلب الوسائط، تأكد من الرابط.")

        for media in urls:
            if media.endswith(".mp4"):
                await event.client.send_file(event.chat_id, media, caption="🎬 فيديو من إنستقرام")
            else:
                await event.client.send_file(event.chat_id, media, caption="📸 صورة من إنستقرام")
        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")
