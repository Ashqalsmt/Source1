from .. import zedub
from ..core.managers import edit_or_reply
from telethon import events
import aiohttp
from yt_dlp import YoutubeDL
import re, asyncio

# API أكثر استقراراً
TIKTOK_API = "https://www.tikwm.com/api/"
INSTAGRAM_API = "https://snapinsta.io/action.php"  # SnapInsta

async def fetch_data(url, params=None, method="GET", data=None, return_json=True):
    async with aiohttp.ClientSession() as session:
        if method == "GET":
            async with session.get(url, params=params) as resp:
                return await (resp.json() if return_json else resp.text())
        else:
            async with session.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}) as resp:
                return await (resp.json() if return_json else resp.text())

@zedub.zed_cmd(pattern="تيك(?:\s+|$)(.*)")
async def tiktok_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1) or (reply.text if reply else "")

    if not link or "tiktok.com" not in link:
        return await edit_or_reply(event, "📌 أرسل رابط تيك توك بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من تيك توك...")
    try:
        data = await fetch_data(TIKTOK_API, method="POST", data={"url": link}, return_json=True)

        if data.get("code") != 0:
            return await zed.edit("⚠️ لم أستطع جلب الفيديو، تأكد من الرابط.")

        result = data["data"]

        # فيديو
        if result.get("play"):
            await event.client.send_file(event.chat_id, result["play"], caption="✅ تيك توك بدون علامة مائية")

        # صور متعددة
        if result.get("images"):
            for img in result["images"]:
                await event.client.send_file(event.chat_id, img, caption="📸 صورة من تيك توك")

        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")

@zedub.zed_cmd(pattern=r"انستا(?:\s+|$)(.*)")
async def insta_download(event):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1).strip() or (reply.text.strip() if reply else "")

    if not link or not re.search(r"(instagram\.com|instagr\.am)", link):
        return await edit_or_reply(event, "📌 أرسل رابط إنستقرام بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, "⏳ جاري التحميل من إنستقرام...")

    async def run_ytdlp(url):
        loop = asyncio.get_event_loop()
        def _download():
            ydl_opts = {
                "format": "best",
                "outtmpl": "/tmp/insta_%(id)s.%(ext)s",
                "quiet": True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        return await loop.run_in_executor(None, _download)

    try:
        filename = await run_ytdlp(link)
        await event.client.send_file(event.chat_id, filename, caption="✅ تم التحميل من إنستقرام")
        await zed.delete()
    except Exception as e:
        await zed.edit(f"❌ خطأ أثناء التحميل: {e}")
