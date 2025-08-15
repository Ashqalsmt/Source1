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

API_BASE = "https://secretv1.sbs/api/v9?url="

async def fetch_media(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_BASE + link) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

async def download_media(event, platform_name, url_pattern):
    reply = await event.get_reply_message()
    link = event.pattern_match.group(1) or (reply.text.strip() if reply else "")

    if not link or not re.search(url_pattern, link):
        return await edit_or_reply(event, f"📌 أرسل رابط {platform_name} بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, f"⏳ جاري التحميل من {platform_name}...")

    try:
        data = await fetch_media(link)
        if not data or "url" not in data:
            return await zed.edit("⚠️ لم أجد أي وسائط في الرابط المرسل.")

        media_url = data["url"]
        await event.client.send_file(event.chat_id, media_url, caption=f"📥 تم التحميل من {platform_name}")
        await zed.delete()

    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")


@zedub.zed_cmd(pattern=r"سناب(?:\s+|$)(.*)")
async def snap_download(event):
    await download_media(event, "سناب شات", r"snapchat\.com")


@zedub.zed_cmd(pattern=r"لايكي(?:\s+|$)(.*)")
async def likee_download(event):
    await download_media(event, "لايكي", r"likee\.video")


@zedub.zed_cmd(pattern=r"فيس(?:\s+|$)(.*)")
async def facebook_download(event):
    await download_media(event, "فيسبوك", r"(facebook\.com|fb\.watch)")


@zedub.zed_cmd(pattern=r"(تويتر|اكس)(?:\s+|$)(.*)")
async def twitter_download(event):
    await download_media(event, "تويتر (X)", r"(twitter\.com|x\.com)")
