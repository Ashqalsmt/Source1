import asyncio
from yamenthon import zedub
from telethon import events, TelegramClient
from telethon.tl.custom import Button
from telethon.sessions import StringSession
from ..Config import Config

plugin_category = "البوتات"

async def interact_with_botfather_step_by_step(client, steps):
    try:
        async with client.conversation('BotFather', timeout=30) as conv:
            responses = []
            for step in steps:
                await conv.send_message(step['command'])
                response = await conv.get_response()
                responses.append(response.text)
            return responses
    except asyncio.TimeoutError:
        return "انتهت المهلة أثناء انتظار الرد من بوت فاذر"
    except Exception as e:
        return f"حدث خطأ أثناء التفاعل مع بوت فاذر: {str(e)}"

@zedub.on(events.NewMessage(pattern=r'\.صنع بوت (.*)'))
async def create_bot(event):
    try:
        input_str = event.pattern_match.group(1)
        if ' ' not in input_str:
            await event.respond("⎉╎يجب كتابة اسم البوت ويوزره مع المسافة بينهم!\nمثال: `.صنع بوت MyBot mybot`")
            return
            
        name, username = input_str.split(' ', 1)
        if username.startswith('@'):
            username = username[1:]
        
        async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
            # خطوات إنشاء البوت بشكل تسلسلي
            steps = [
                {'command': '/newbot'},
                {'command': name},
                {'command': username}
            ]
            
            results = await interact_with_botfather_step_by_step(client, steps)
            
            if not results or len(results) < 3:
                await event.respond("⎉╎❌ فشل في إنشاء البوت. لم يتم الحصول على ردود كافية من بوت فاذر")
                return
                
            final_response = results[-1]
            
            if "Done!" in final_response or "تم!" in final_response or "token" in final_response.lower():
                # الحصول على التوكن
                token_steps = [
    {'command': '/token'},  
    {'command': f'@{username}'}
]
token_results = await interact_with_botfather_step_by_step(client, token_steps)
                
                if not token_results:
                    await event.respond(f"⎉╎✅ تم إنشاء البوت: @{username} ولكن لم يتم الحصول على التوكن")
                    return
                    
                token_response = token_results[0]
                
                if "Use this token" in token_response or "استخدم هذا الرمز" in token_response:
                    token = token_response.split('\n')[-1].strip()
                    await event.respond(
                        f"⎉╎✅ تم إنشاء البوت بنجاح!\n\n"
                        f"⎉╎اليوزر: @{username}\n"
                        f"⎉╎التوكن: `{token}`\n\n"
                        f"⎉╎يمكنك التحكم فيه باستخدام الأمر:\n`.تعديل @{username}`",
                        parse_mode='md'
                    )
                else:
                    await event.respond(f"⎉╎✅ تم إنشاء البوت: @{username} ولكن لم يتم الحصول على التوكن.\nالرد: {token_response}")
            else:
                await event.respond(f"⎉╎❌ فشل في إنشاء البوت. قد يكون اليوزر محجوزاً.\n\nالرد من بوت فاذر:\n{final_response}")
                
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ غير متوقع: {str(e)}")

# باقي الكود يبقى كما هو بدون تغيير ...

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
                    await event.respond(f"⎉╎✅ تم تغيير اسم البوت {username} إلى: {new_name}")
                else:
                    await event.respond(f"⎉╎❌ فشل في تغيير الاسم.\nالرد: {result if result else 'لا يوجد رد'}")
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
                    await event.respond(f"⎉╎✅ تم تغيير وصف البوت {username}")
                else:
                    await event.respond(f"⎉╎❌ فشل في تغيير الوصف.\nالرد: {result if result else 'لا يوجد رد'}")
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")

@zedub.on(events.CallbackQuery(data=b"change_pic"))
async def change_pic_handler(event):
    try:
        async with event.client.conversation(event.sender_id) as conv:
            await conv.send_message("⎉╎أرسل لي الصورة الجديدة للبوت (كصورة وليس كملف):")
            pic_response = await conv.get_response()
            
            original_msg = await event.get_message()
            username = original_msg.text.split()[-1]
            
            if pic_response.photo or pic_response.document.mime_type.startswith('image/'):
                async with TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH) as client:
                    await client.send_file(
                        'BotFather',
                        pic_response.media,
                        caption=f"/setuserpic {username}"
                    )
                    await asyncio.sleep(5)
                    await event.respond(f"⎉╎✅ تم استلام الصورة ومعالجتها للبوت {username}")
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
            f"⎉╎هل أنت متأكد من حذف البوت {username}؟ لا يمكن التراجع عن هذا الإجراء!",
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
                await event.respond(f"⎉╎✅ تم حذف البوت {username} بنجاح")
            else:
                await event.respond(f"⎉╎❌ فشل في حذف البوت.\nالرد: {result if result else 'لا يوجد رد'}")
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
                    parse_mode='md'
                )
            else:
                await event.respond(f"⎉╎❌ لم يتم الحصول على التوكن.\nالرد: {token_msg if token_msg else 'لا يوجد رد'}")
    except Exception as e:
        await event.respond(f"⎉╎❌ حدث خطأ: {str(e)}")
