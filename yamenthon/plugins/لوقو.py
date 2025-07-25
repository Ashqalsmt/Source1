

import os
import random
import string
try: 
    import arabic_reshaper
except ModuleNotFoundError:
    os.system("pip3 install arabic_reshaper")
    import arabic_reshaper
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos
from telethon import events

from yamenthon import zedub

from yamenthon.core.logger import logging
from ..core.managers import edit_delete, edit_or_reply as eor
from ..helpers import reply_id, get_user_from_event
from ..sql_helper.globals import addgvar, gvarstatus
from . import *

LOGS = logging.getLogger(__name__)
PICS_STR = []



async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)



@zedub.zed_cmd(pattern=r"لوكو ?(.*)")
async def lg1(userevent):
    event = await eor(userevent, "**- جـارِ صنـع لـوكـو انكـلش بحقـوقك ...**")
    me = await userevent.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    if gvarstatus("ZED_FONTS") is None: 
        zed_font = await get_font_file(userevent.client, "@T_Taiz")
    else:
        zed_font = gvarstatus("ZED_FONTS")
    if userevent.reply_to_msg_id:
        rply = await userevent.get_reply_message()
        logo_ = await rply.download_media()
    else: #YamenThon
        async for i in bot.iter_messages(
            "@Z_44_Z", filter=InputMessagesFilterPhotos
        ):
            PICS_STR.append(i)
        pic = random.choice(PICS_STR)
        logo_ = await pic.download_media()
    text = userevent.pattern_match.group(1)
    if not text:
        await eor(event, "- الامـر + نص او الامـر + نص بالـرد ع صـورة ...")
        return
    arabic_text = "".join(
        char for char in text if char.isalpha() and char not in string.ascii_letters
    )
    if arabic_text: #YamenThon
        await eor(event, "**- الرجاء إدخال نص باللغـة الانجليـزية فقـط.**\n`.لوكو` + **نص انكـلش**\n`.لوقو` + **نص عـربـي**")
        return
    if len(text) <= 8:
        font_size_ = 150
        strik = 10
    elif len(text) >= 9:
        font_size_ = 50
        strik = 5
    else:
        font_size_ = 130
        strik = 20
    img = Image.open(logo_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(zed_font, font_size_)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
    )
    w_ = (image_width - w) / 2
    h_ = (image_height - h) / 2
    draw.text(
        (w_, h_), text, font=font, fill="white", stroke_width=strik, stroke_fill="black"
    )
    file_name = "Andencento .png"
    img.save(file_name, "png")
    await bot.send_file(
        userevent.chat_id,
        file_name,
        caption=f"**- تم صنـع لـوجـو انكـلش .. بنجـاح 🎆☑️\n- حقـوق :** {my_mention} .\n\n**- بواسطـة : @YamenThon**",
    )
    await event.delete()
    try:
        os.remove(file_name)
        os.remove(zed_font)
        os.remove(logo_)
    except BaseException:
        pass



#YamenThon
@zedub.zed_cmd(pattern=r"لوقو ?(.*)")
async def lg1(userevent):
    event = await eor(userevent, "**- جـارِ صنـع لـوقـو عـربـي بحقـوقك ...**")
    me = await userevent.client.get_me()
    my_first = me.first_name
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    if gvarstatus("ZED_FONTS") is None: #YamenThon
        zed_font = await get_font_file(userevent.client, "@S_SSQ")
    else: 
        zed_font = gvarstatus("ZED_FONTS")
    if userevent.reply_to_msg_id:
        rply = await userevent.get_reply_message()
        logo_ = await userevent.client.download_media(rply)
    else: 
        async for i in bot.iter_messages(
            "@Z_44_Z", filter=InputMessagesFilterPhotos
        ):
            PICS_STR.append(i)
        pic = random.choice(PICS_STR)
        logo_ = await pic.download_media()
    text = userevent.pattern_match.group(1)
    if not text:
        await eor(event, "- الامـر + نص او الامـر + نص بالـرد ع صـورة ...")
        return
    arabic_text = "".join(
        char for char in text if char.isalpha() and char not in string.ascii_letters
    )
    if not arabic_text: #YamenThon
        await eor(event, "**- الرجاء إدخال نص باللغـة العربيـة فقـط.**\n`.لوقو` + **نص عـربـي**\n`.لوكو` + **نص انكـلش**")
        return
    if len(text) <= 8:
        font_size_ = 150
        strik = 10
    elif len(text) >= 9:
        font_size_ = 50
        strik = 5
    else:
        font_size_ = 130
        strik = 20
    img = Image.open(logo_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(zed_font, font_size_)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
    )
    w_ = (image_width - w) / 2
    h_ = (image_height - h) / 2
    draw.text(
        (w_, h_), text, font=font, fill="white", stroke_width=strik, stroke_fill="black"
    )
    file_name = "Andencento .png"
    img.save(file_name, "png")
    await bot.send_file(
        userevent.chat_id,
        file_name,
        caption=f"**- تم صنـع لـوجـو عـربـي .. بنجـاح 🎆☑️\n- حقـوق :** {my_mention} .\n\n**- بواسطـة : @YamenThon**",
    )
    await event.delete()
    try:
        os.remove(file_name)
        os.remove(zed_font)
        os.remove(logo_)
    except BaseException:
        pass
