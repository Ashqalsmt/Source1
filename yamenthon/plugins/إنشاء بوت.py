import asyncio
from yamenthon import zedub
from telethon import events, TelegramClient
from telethon.tl.custom import Button
from telethon.sessions import StringSession
from ..Config import Config

plugin_category = "البوتات"

async def interact_with_botfather(client, command, wait_for=None, timeout=30):
    try:
        # إرسال الأمر إلى BotFather
        await client.send_message('BotFather', command)
        
        if not wait_for:
            return None
            
        # انتظار الرد من BotFather
        response = await client.wait_for(
            events.NewMessage(from_users='BotFather'),
            timeout=timeout
        )
        
        return response.text
        
    except asyncio.TimeoutError:
        return "انتهت المهلة أثناء انتظار الرد من بوت فاذر"
    except Exception as e:
        return f"حدث خطأ أثناء التفاعل مع بوت فاذر: {str(e)}"

@zedub.on(events.NewMessage(pattern=r'\.صنع بوت (.*)'))
async def create_bot(event):
    try:
        input_str = event.pattern_match.group(1)
        if ' ' not in input_str:
            await event.respond(
                "⎉╎يجب كتابة اسم البوت ويوزره مع المسافة بينهم!\n"
                "مثال: `.صنع بوت MyBot mybot`",
                parse_mode='markdown'
            )
            return
            
        name, username = input_str.split(' ', 1)
        if not username.startswith('@'):
            username = f"@{username}"
        
        async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
            # التأكد من تسجيل الدخول
            if not await client.is_user_authorized():
                await event.respond(
                    "⎉╎❌ يجب تسجيل الدخول أولاً!\n"
                    "استخدم الأمر `.تسجيل` لإنشاء جلسة",
                    parse_mode='markdown'
                )
                return
            
            # إنشاء البوت
            result = await interact_with_botfather(
                client,
                f"/newbot\n{name}\n{username}",
                wait_for=True
            )
            
            if not result:
                await event.respond("⎉╎❌ لم يتم الحصول على رد من بوت فاذر")
                return
                
            if "Done!" in result or "تم!" in result or "Choose a name" in result:
                # انتظر 3 ثوان قبل طلب التوكن
                await asyncio.sleep(3)
                
                # الحصول على التوكن
                token_msg = await interact_with_botfather(
                    client,
                    f"/token {username}",
                    wait_for=True
                )
                
                if not token_msg:
                    await event.respond(
                        f"⎉╎✅ تم إنشاء البوت: {username}\n"
                        "ولكن لم يتم الحصول على التوكن"
                    )
                    return
                    
                if "Use this token" in token_msg or "استخدم هذا الرمز" in token_msg:
                    token = token_msg.split('\n')[-1].strip()
                    await event.respond(
                        f"⎉╎✅ تم إنشاء البوت بنجاح!\n\n"
                        f"⎉╎اليوزر: {username}\n"
                        f"⎉╎التوكن: `{token}`\n\n"
                        f"⎉╎يمكنك التحكم فيه باستخدام الأمر:\n`.تعديل {username}`",
                        parse_mode='markdown'
                    )
                else:
                    await event.respond(
                        f"⎉╎✅ تم إنشاء البوت: {username}\n"
                        f"ولكن لم يتم الحصول على التوكن.\nالرد: {token_msg}"
                    )
            else:
                await event.respond(
                    f"⎉╎❌ فشل في إنشاء البوت. قد يكون اليوزر محجوزاً.\n\n"
                    f"الرد من بوت فاذر:\n{result}"
                )
                
    except Exception as e:
        await event.respond(
            f"⎉╎❌ حدث خطأ غير متوقع:\n"
            f"{type(e).__name__}: {str(e)}"
        )

@zedub.on(events.NewMessage(pattern=r'\.تعديل (@?\w+)'))
async def manage_bot(event):
    try:
        username = event.pattern_match.group(1)
        if not username.startswith('@'):
            username = f"@{username}"
        
        buttons = [
            [Button.inline("تغيير اسم البوت", b"change_name")],
            [Button.inline("تغيير وصف البوت", b"change_desc")],
            [Button.inline("تغيير صورة البوت", b"change_pic")],
            [Button.inline("حذف البوت", b"delete_bot")],
            [Button.inline("الحصول على التوكن", b"get_token")],
        ]
        
        await event.respond(
            f"⎉╎اختر ما تريد فعله مع البوت {username}:",
            buttons=buttons
        )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"change_name"))
async def change_name_handler(event):
    try:
        async with event.client.conversation(event.sender_id) as conv:
            await conv.send_message("⎉╎أرسل لي الاسم الجديد للبوت:")
            name_response = await conv.get_response()
            new_name = name_response.text
            
            original_msg = await event.get_message()
            username = original_msg.text.split()[-1]
            
            async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
                result = await interact_with_botfather(
                    client,
                    f"/setname {username}\n{new_name}",
                    wait_for=True
                )
                
                if result and ("Done!" in result or "تم!" in result):
                    await event.respond(
                        f"⎉╎✅ تم تغيير اسم البوت {username} إلى: {new_name}"
                    )
                else:
                    await event.respond(
                        f"⎉╎❌ فشل في تغيير الاسم.\n"
                        f"الرد: {result if result else 'لا يوجد رد'}"
                    )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"change_desc"))
async def change_desc_handler(event):
    try:
        async with event.client.conversation(event.sender_id) as conv:
            await conv.send_message("⎉╎أرسل لي الوصف الجديد للبوت:")
            desc_response = await conv.get_response()
            new_desc = desc_response.text
            
            original_msg = await event.get_message()
            username = original_msg.text.split()[-1]
            
            async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
                result = await interact_with_botfather(
                    client,
                    f"/setdescription {username}\n{new_desc}",
                    wait_for=True
                )
                
                if result and ("Done!" in result or "تم!" in result):
                    await event.respond(
                        f"⎉╎✅ تم تغيير وصف البوت {username}"
                    )
                else:
                    await event.respond(
                        f"⎉╎❌ فشل في تغيير الوصف.\n"
                        f"الرد: {result if result else 'لا يوجد رد'}"
                    )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"change_pic"))
async def change_pic_handler(event):
    try:
        async with event.client.conversation(event.sender_id) as conv:
            await conv.send_message(
                "⎉╎أرسل لي الصورة الجديدة للبوت (كصورة وليس كملف):"
            )
            pic_response = await conv.get_response()
            
            original_msg = await event.get_message()
            username = original_msg.text.split()[-1]
            
            if (pic_response.photo or 
                (hasattr(pic_response, 'document') and 
                 pic_response.document.mime_type.startswith('image/'))):
                
                async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
                    await client.send_file(
                        'BotFather',
                        pic_response.media,
                        caption=f"/setuserpic {username}"
                    )
                    await asyncio.sleep(5)
                    await event.respond(
                        f"⎉╎✅ تم استلام الصورة ومعالجتها للبوت {username}"
                    )
            else:
                await event.respond("⎉╎❌ لم يتم إرسال صورة صالحة!")
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"delete_bot"))
async def delete_bot_handler(event):
    try:
        original_msg = await event.get_message()
        username = original_msg.text.split()[-1]
        
        confirm_buttons = [
            [Button.inline("✅ نعم، احذف البوت", b"confirm_delete")],
            [Button.inline("❌ إلغاء", b"cancel_delete")]
        ]
        
        await event.respond(
            f"⎉╎هل أنت متأكد من حذف البوت {username}؟\n"
            "لا يمكن التراجع عن هذا الإجراء!",
            buttons=confirm_buttons
        )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"confirm_delete"))
async def confirm_delete_handler(event):
    try:
        original_msg = await event.get_message()
        username = original_msg.text.split()[-2]
        
        async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
            result = await interact_with_botfather(
                client,
                f"/deletebot {username}",
                wait_for=True
            )
            
            if result and ("Done!" in result or "تم!" in result):
                await event.respond(
                    f"⎉╎✅ تم حذف البوت {username} بنجاح"
                )
            else:
                await event.respond(
                    f"⎉╎❌ فشل في حذف البوت.\n"
                    f"الرد: {result if result else 'لا يوجد رد'}"
                )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"cancel_delete"))
async def cancel_delete_handler(event):
    try:
        await event.respond("⎉╎تم إلغاء عملية الحذف")
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"get_token"))
async def get_token_handler(event):
    try:
        original_msg = await event.get_message()
        username = original_msg.text.split()[-1]
        
        async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
            token_msg = await interact_with_botfather(
                client,
                f"/token {username}",
                wait_for=True
            )
            
            if token_msg and ("Use this token" in token_msg or "استخدم هذا الرمز" in token_msg):
                token = token_msg.split('\n')[-1].strip()
                await event.respond(
                    f"⎉╎✅ توكن البوت {username}:\n\n`{token}`",
                    parse_mode='markdown'
                )
            else:
                await event.respond(
                    f"⎉╎❌ لم يتم الحصول على التوكن.\n"
                    f"الرد: {token_msg if token_msg else 'لا يوجد رد'}"
                )
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")
