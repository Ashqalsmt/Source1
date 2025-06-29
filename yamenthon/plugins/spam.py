import asyncio
from ..Config import Config
from ..core.managers import edit_or_reply as eor
from .. import zedub
from telethon.errors import FloodWaitError

hl = "."  # البادئة الافتراضية للأوامر (مثل .سبام)

plugin_category = "الإسبام"


@zedub.zed_cmd(pattern="سبام(?:\s|$)([\s\S]*)")
async def spammer(event):
    """إرسال رسالة عدد معين من المرات (حتى 100)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[6:]
    try:
        counter = int(msg_.split(" ")[0])
        spam_message = msg_.replace(str(counter), "").strip()
    except:
        return await eor(event, f"الاستخدام: `{hl}سبام 10 مرحباً`")
    
    reply_message = await event.get_reply_message()
    if counter > 100:
        return await eor(event, f"❗ لإرسال أكثر من 100 رسالة، استخدم:\n`{hl}سبام_كبير العدد النص`")
    msg = await eor(event, f"🔁 يتم إرسال الرسالة {counter} مرة...")
    for _ in range(counter):
        await event.client.send_message(event.chat_id, spam_message, reply_to=reply_message)
    await msg.delete()
    await event.client.send_message(lg_id, f"#SPAM \n\nتم إرسال `{counter}` رسالة.")


@zedub.zed_cmd(pattern="سبام_كبير(?:\s|$)([\s\S]*)")
async def bigspam(event):
    """سبام بعدد كبير بدون حد (قد يسبب حظر مؤقت)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[11:]
    try:
        counter = int(msg_.split(" ")[0])
        spam_message = msg_.replace(str(counter), "").strip()
    except:
        return await eor(event, f"الاستخدام: `{hl}سبام_كبير 500 قصف`")

    reply_msg = await event.get_reply_message()
    message_to_send = reply_msg if reply_msg else spam_message
    for _ in range(counter):
        await event.client.send_message(event.chat_id, message_to_send, reply_to=reply_msg)
    await event.delete()
    await event.client.send_message(lg_id, f"#BIGSPAM \n\nتم إرسال `{counter}` رسالة.")


@zedub.zed_cmd(pattern="سبام_مؤقت(?:\s|$)([\s\S]*)")
async def delay_spam(event):
    """سبام برسائل مؤقتة بفاصل زمني"""
    lg_id = Config.LOGGER_ID
    try:
        input_str = "".join(event.text.split(maxsplit=1)[1:])
        delay = float(input_str.split(" ", 2)[0])
        counter = int(input_str.split(" ", 2)[1])
        spam_message = str(input_str.split(" ", 2)[2])
    except:
        return await eor(event, f"الاستخدام: `{hl}سبام_مؤقت 2 10 مرحباً`")
    await event.delete()
    for _ in range(counter):
        await event.client.send_message(event.chat_id, spam_message)
        await asyncio.sleep(delay)
    await event.client.send_message(lg_id, f"#DELAYSPAM \n\nتم إرسال `{counter}` رسالة بفاصل `{delay}` ثانية.")


@zedub.zed_cmd(pattern="سبام_لا_نهائي(?:\s|$)([\s\S]*)")
async def uspam(event):
    """إرسال رسالة بشكل غير نهائي حتى حدوث FloodWait"""
    lg_id = Config.LOGGER_ID
    reply_msg = await event.get_reply_message()
    msg_text = event.text[13:].strip()
    input_msg = reply_msg or msg_text

    if not input_msg:
        return await eor(event, f"الاستخدام: `{hl}سبام_لا_نهائي مرحباً` أو بالرد على رسالة")

    await event.client.send_message(
        lg_id,
        f"#UNLIMITED_SPAM\n\nبدأ الإسبام غير النهائي. سيتم التوقف تلقائيًا عند حدوث FloodWait."
    )

    while True:
        try:
            await event.client.send_message(event.chat_id, input_msg)
        except FloodWaitError as e:
            break


@zedub.zed_cmd(pattern="سبام_مجزأ(?:\s|$)([\s\S]*)")
async def bspam(event):
    """إرسال سبام مجزأ لتجنب الحظر (دفعات مع تأخير)"""
    lg_id = Config.LOGGER_ID
    msg_ = event.text[12:]
    try:
        counter = int(msg_.split(" ")[0])
    except:
        return await eor(event, f"الاستخدام: `{hl}سبام_مجزأ 500 مرحباً`")
    
    reply_msg = await event.get_reply_message()
    spam_message = reply_msg or msg_.replace(str(counter), "").strip()
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
    try:
        count = int(event.pattern_match.group(1).split(" ")[0])
    except:
        return await eor(event, f"الاستخدام: `{hl}سبام_ميديا 50` مع الرد على ميديا")

    if not reply_msg or not reply_msg.media:
        return await eor(event, "↪️ رد على صورة، ملصق، فيديو، أو GIF لاستخدام هذا الأمر.")
    
    media = reply_msg.media
    for _ in range(count):
        await event.client.send_file(event.chat_id, media)
    await event.delete()
    await event.client.send_message(lg_id, f"#MEDIA_SPAM\n\nتم إرسال الوسائط `{count}` مرة.")
