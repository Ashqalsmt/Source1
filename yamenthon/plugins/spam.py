import asyncio
from ..Config import Config
from ..core.managers import edit_or_reply as eor
from .. import zedub
from telethon.errors import FloodWaitError

hl = "."  # البادئة الافتراضية للأوامر
plugin_category = "الإسبام"


@zedub.zed_cmd(pattern="سبام(?:\s|$)([\s\S]*)")
async def spammer(event):
    """إرسال رسالة عدد معين من المرات (حتى 100)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[6:].strip()
    if not msg_ or len(msg_.split()) < 2:
        return await eor(event, "❗ **يجب كتابة عدد الرسائل والنص المراد إرساله.**\nمثال: `.سبام 5 مرحبًا`")

    try:
        counter = int(msg_.split(" ")[0])
        spam_message = " ".join(msg_.split(" ")[1:])
    except ValueError:
        return await eor(event, "❗ **يرجى التأكد من كتابة رقم صحيح.**\nمثال: `.سبام 5 مرحبًا`")

    reply_message = await event.get_reply_message()
    if counter > 100:
        return await eor(event, f"❗ لا يمكنك إرسال أكثر من 100 رسالة باستخدام هذا الأمر.\nاستخدم: `{hl}سبام_كبير العدد النص`")
    msg = await eor(event, f"🔁 يتم إرسال الرسالة `{counter}` مرة...")
    for _ in range(counter):
        await event.client.send_message(event.chat_id, spam_message, reply_to=reply_message)
    await msg.delete()
    await event.client.send_message(lg_id, f"#SPAM \n\nتم إرسال `{counter}` رسالة.")


@zedub.zed_cmd(pattern="سبام_كبير(?:\s|$)([\s\S]*)")
async def bigspam(event):
    """سبام بعدد كبير بدون حد (قد يسبب حظر مؤقت)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[11:].strip()
    if not msg_ or len(msg_.split()) < 2:
        return await eor(event, "❗ **يرجى إدخال عدد الرسائل والنص.**\nمثال: `.سبام_كبير 500 هجوم`")
    
    try:
        counter = int(msg_.split(" ")[0])
        spam_message = " ".join(msg_.split(" ")[1:])
    except ValueError:
        return await eor(event, "❗ **يرجى التأكد من كتابة رقم صحيح.**\nمثال: `.سبام_كبير 500 هجوم`")

    reply_msg = await event.get_reply_message()
    message_to_send = reply_msg if reply_msg else spam_message
    for _ in range(counter):
        await event.client.send_message(event.chat_id, message_to_send, reply_to=reply_msg)
    await event.delete()
    await event.client.send_message(lg_id, f"#BIGSPAM \n\nتم إرسال `{counter}` رسالة.")


@zedub.zed_cmd(pattern="سبام_مؤقت(?:\s|$)([\s\S]*)")
async def delay_spam(event):
    """سبام بفاصل زمني بين كل رسالة"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[12:].strip()
    if not msg_ or len(msg_.split()) < 3:
        return await eor(event, "❗ **يرجى كتابة الفاصل الزمني وعدد الرسائل والنص.**\nمثال: `.سبام_مؤقت 1 10 اهلا`")

    try:
        parts = msg_.split(" ", 2)
        delay = float(parts[0])
        counter = int(parts[1])
        spam_message = parts[2]
    except Exception:
        return await eor(event, "❗ **خطأ في الصيغة. تأكد من كتابة الأرقام بشكل صحيح.**\nمثال: `.سبام_مؤقت 1 10 اهلا`")

    await event.delete()
    for _ in range(counter):
        await event.client.send_message(event.chat_id, spam_message)
        await asyncio.sleep(delay)
    await event.client.send_message(lg_id, f"#DELAYSPAM \n\nتم إرسال `{counter}` رسالة بفاصل `{delay}` ثانية.")


@zedub.zed_cmd(pattern="سبام_لا_نهائي(?:\s|$)([\s\S]*)")
async def uspam(event):
    """إرسال رسالة بشكل لا نهائي حتى حدوث FloodWait"""
    lg_id = Config.LOGGER_ID
    reply_msg = await event.get_reply_message()
    msg_text = event.text[13:].strip()
    input_msg = reply_msg.message if reply_msg else msg_text

    if not input_msg:
        return await eor(event, "❗ **يرجى كتابة نص الرسالة أو الرد على رسالة.**\nمثال: `.سبام_لا_نهائي اهلا`")

    await event.client.send_message(
        lg_id,
        f"#UNLIMITED_SPAM\n\nبدأ الإسبام غير النهائي. سيتم التوقف تلقائيًا عند حدوث FloodWait."
    )

    while True:
        try:
            await event.client.send_message(event.chat_id, input_msg)
        except FloodWaitError:
            break


@zedub.zed_cmd(pattern="سبام_مجزأ(?:\s|$)([\s\S]*)")
async def bspam(event):
    """إرسال سبام مجزأ لتفادي الحظر (دفعات مع تأخير)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[12:].strip()
    if not msg_ or len(msg_.split()) < 2:
        return await eor(event, "❗ **يرجى كتابة العدد والنص.**\nمثال: `.سبام_مجزأ 500 اهلا`")
    
    try:
        counter = int(msg_.split(" ")[0])
        spam_message = " ".join(msg_.split(" ")[1:])
    except ValueError:
        return await eor(event, "❗ **يرجى التأكد من كتابة رقم صحيح.**\nمثال: `.سبام_مجزأ 500 اهلا`")

    reply_msg = await event.get_reply_message()
    spam_message = reply_msg.message if reply_msg else spam_message

    rest = counter % 100
    sets = counter // 100
    delay = 30

    for _ in range(sets):
        for __ in range(100):
            await event.client.send_message(event.chat_id, spam_message)
        delay += 2
        await asyncio.sleep(delay)

    for _ in range(rest):
        await event.client.send_message(event.chat_id, spam_message)

    await event.delete()
    await event.client.send_message(lg_id, f"#BREAK_SPAM\n\nتم إرسال `{counter}` رسالة مجزأة.")


@zedub.zed_cmd(pattern="سبام_ميديا(?:\s|$)([\s\S]*)")
async def mspam(event):
    """إرسال وسائط (صور/ملصقات/فيديوهات) مكررة"""
    lg_id = Config.LOGGER_ID
    reply_msg = await event.get_reply_message()
    arg = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else ""

    if not arg or not arg.isdigit():
        return await eor(event, "❗ **يرجى كتابة عدد التكرارات والرد على الوسائط.**\nمثال: `.سبام_ميديا 10` مع الرد على صورة")

    count = int(arg)

    if not reply_msg or not reply_msg.media:
        return await eor(event, "❗ **يرجى الرد على صورة، ملصق، فيديو أو GIF لاستخدام هذا الأمر.**")
    
    media = reply_msg.media
    for _ in range(count):
        await event.client.send_file(event.chat_id, media)
    await event.delete()
    await event.client.send_message(lg_id, f"#MEDIA_SPAM\n\nتم إرسال الوسائط `{count}` مرة.")
