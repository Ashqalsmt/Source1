import os
import shutil
from asyncio import sleep
import random

from telethon import events

from yamenthon import zedub
from yamenthon.core.logger import logging
from ..Config import Config
from ..core.managers import edit_or_reply, edit_delete
from ..helpers import reply_id, get_user_from_event
from . import BOTLOG, BOTLOG_CHATID
plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)


async def ge(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj

zel_dev = (6669024587)


import random

from telethon import events


@zedub.zed_cmd(pattern="رفع زوجتي(?: |$)(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"🚻 ** ᯽︙  المستخدم => • ** [{tag}](tg://user?id={user.id}) \n ☑️ **᯽︙  تم رفعها مرتك  :** 👰🏼‍♀️.\n**᯽︙  يلا حبيبي امشي نخلف بيبي 👶🏻🤤** ")

@zedub.zed_cmd(pattern="رفع كلب(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه كلب 🐶  :**  \n**᯽︙  خليه خله ينبح 😂**")

@zedub.zed_cmd(pattern="رفع تاجي(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"᯽︙ المستخدم [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه تاج :**  👑🔥")

@zedub.zed_cmd(pattern="رفع قرد(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"᯽︙ المستخدم [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه قرد واعطائه موزة 🐒🍌 :** ")

@zedub.zed_cmd(pattern="رفع بكلبي(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه بكلـبك 🤍 :**  \n**᯽︙  انت حبي الابدي 😍**")
    
    

@zedub.zed_cmd(pattern="رفع مركبه(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه مطي 🐴  :**  \n**᯽︙  تعال حبي استلم  انه **")
    



@zedub.zed_cmd(pattern="رفع زوجي(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه زوجج :**  \n**᯽︙  يلا حبيبي امشي نخلف 🤤🔞**")
    

@zedub.zed_cmd(pattern="رفع زاحف(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفع المتهم زاحف اصلي :**  \n**᯽︙  ها يلزاحف شوكت تبطل سوالفك حيوان 😂🐍**")

@zedub.zed_cmd(pattern="رفع كحبة(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفع المتهم كحبة 👙 :**  \n**᯽︙  ها يلكحبة طوبز خلي انيجك/ج**")

@zedub.zed_cmd(pattern="رفع فرخه(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه فرخ الكروب :**  \n**᯽︙  لك الفرخ استر على خمستك ياهو اليجي يزورهاً 👉🏻👌🏻**")

@zedub.zed_cmd(pattern="رفع حلوه(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـها حلوه الكروب 🤤😻 :**  \n**᯽︙  تعاي يعافيتي اريد حضن دافي 😽**")

@zedub.zed_cmd(pattern="رفع هايشة(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه المتهم هايشة 🐄 :**  \n**᯽︙  ها يلهايشة خوش بيك حليب تعال احلبك 😂**")

@zedub.zed_cmd(pattern="رفع حلو(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه صاك 🤤 :**  \n**᯽︙  تعال يلحلو انطيني بوسة من رگبتك 😻🤤**")

@zedub.zed_cmd(
    pattern="مصه(?:\s|$)([\s\S]*)",
    command=("مصه", plugin_category),
)
async def permalink(mention): 
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . بلا مفتاله حقك هاذا مطور السورس يا مجنون😒  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . بلا مفتاله حقك هاذا مطور السورس يا مجنون😒  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . بلا مفتاله حقك هاذا مطور السورس يا مجنون😒  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"** ⣠⡶⠚⠛⠲⢄⡀\n⣼⠁      ⠀⠀⠀⠳⢤⣄\n⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇\n⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄\n⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄\n⠀⠀⠀⠘⣆       ⠀⠀⠀⠀⠀⠈⠓⢦⣀\n⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤\n⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧\n⠀⠀⠀⠀⠀⠀⠀    ⠓⠦⠀⠀⠀⠀**\n**🚹 ¦ تعال مصه عزيزي ** [{tag}](tg://user?id={user.id})")

@zedub.zed_cmd(pattern="سيد(?: |$)(.*)")
async def permalink(mention):
    await edit_or_reply(mention, f"سماحة السيد الاسطوره عاشق الصمت مطور سورس يمنثون @T_A_Tl")

@zedub.zed_cmd(pattern="رفع ايجة(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه ايچة 🤤  :**  \n**᯽︙  ها يلأيچة تطلعين درب بـ$25 👙**")

@zedub.zed_cmd(pattern="رفع زبال(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعـه زبال الكروب 🧹 :**  \n**᯽︙  تعال يلزبال اكنس الكروب لا أهينك 🗑😹**")

@zedub.zed_cmd(pattern="رفع كوده(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعه كواد :**  \n**᯽︙  تعال يكواد عرضك مطشر اصير حامي عرضك ؟😎**")

@zedub.zed_cmd(pattern="رفع ديوث(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ المستخدم** [{tag}](tg://user?id={user.id}) \n**᯽︙  تـم رفعه ديوث الكروب :**  \n**᯽︙  تعال يلديوث جيب اختك خلي اتمتع وياها 🔞**")

@zedub.zed_cmd(pattern="رفع مميز(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ الحلو** 「[{tag}](tg://user?id={user.id})」 \n**᯽︙  تـم رفعه مميز :** ")

@zedub.zed_cmd(pattern="رفع ادمن(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ الحلو** 「[{tag}](tg://user?id={user.id})」 \n**᯽︙  تـم رفعه ادمن :** ")

@zedub.zed_cmd(pattern="رفع منشى(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ الحلو** 「[{tag}](tg://user?id={user.id})」 \n**᯽︙  تـم رفعه منشئ :** ")

@zedub.zed_cmd(pattern="رفع مالك(?: |$)(.*)")
async def permalink(mention):
    
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"**᯽︙ الحلو** 「[{tag}](tg://user?id={user.id})」 \n**᯽︙  تـم رفعه مالك الكروب :** ")

@zedub.zed_cmd(pattern="رفع مجنب(?: |$)(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f" ** ᯽︙  المستخدم => • ** [{tag}](tg://user?id={user.id}) \n ☑️ **᯽︙  تم رفعه مجنب  :** .\n**᯽︙  كوم يلمجنب اسبح مو عيب تضرب جلغ 😹** ")

@zedub.zed_cmd(pattern="رفع وصخ(?: |$)(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"** ᯽︙  المستخدم => • ** [{tag}](tg://user?id={user.id}) \n ☑️ **᯽︙  تم رفعه وصخ الكروب 🤢  :** .\n**᯽︙  لك دكوم يلوصخ اسبح مو ريحتك كتلتنا 🤮 ** ")

@zedub.zed_cmd(pattern="زواج(?: |$)(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"᯽︙ ** لقد تم زواجك/ج من : **[{tag}](tg://user?id={user.id}) 💍\n**᯽︙  الف الف مبروك الان يمكنك اخذ راحتك ** ")

@zedub.zed_cmd(pattern="طلاك(?: |$)(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id in zel_dev:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا احـد المطـورين المساعديـن  ❏╰**")
    if user.id == 5571722913:
        return await edit_or_reply(mention, f"**╮ ❐ لك دي . . هـذا مطـور السـورس  ❏╰**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention,
        f"🚻 ** ᯽︙  المستخدم => • ** [{tag}](tg://user?id={user.id})**᯽︙  انتِ طالق طالق طالق 🙎🏻‍♂️  :** .\n**᯽︙  لقد تم طلاقها بلثلاث وفسخ زواجكما الان الكل حر طليق ** ")
