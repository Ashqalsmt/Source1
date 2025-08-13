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

@zedub.zed_cmd(pattern=r"(لايكي|سناب)(?:\s+|$)(.*)")
async def likee_snap_download(event):
    platform = event.pattern_match.group(1)
    query = event.pattern_match.group(2).strip()

    reply = await event.get_reply_message()
    link = query or (reply.text.strip() if reply else "")

    if not link or not re.search(r"(likee\.video|snapchat\.com)", link):
        return await edit_or_reply(event, f"📌 أرسل رابط {platform} بعد الأمر أو بالرد على الرابط.")

    zed = await edit_or_reply(event, f"⏳ جاري التحميل من {platform}...")

    try:
        # API خارجي موحد
        api_url = f"https://api.akashsir.in/download?url={link}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await zed.edit(f"⚠️ لم أستطع جلب الوسائط من {platform}، جرّب رابط آخر.")
                data = await resp.json()

        # استخراج الرابط
        media_url = data.get("url") or data.get("download_url")
        if not media_url:
            return await zed.edit(f"⚠️ لم أجد أي وسائط في الرابط المرسل.")

        await event.client.send_file(
            event.chat_id,
            media_url,
            caption=f"📥 تم التحميل من {platform}"
        )

        await zed.delete()

    except Exception as e:
        await zed.edit(f"❌ خطأ: {str(e)}")
