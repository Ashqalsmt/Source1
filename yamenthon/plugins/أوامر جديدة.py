import contextlib
import asyncio
from asyncio import sleep

from telethon.errors import (
    ChatAdminRequiredError,
    FloodWaitError,
    MessageNotModifiedError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBanned,
    ChannelParticipantsKicked,
    ChatBannedRights,
)
from telethon.utils import get_display_name
from telethon import events
from telethon.errors import UserNotParticipantError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import GetParticipantRequest

from yamenthon import zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import readable_time
from ..helpers.utils import reply_id
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


spam_chats = []
chr = Config.COMMAND_HAND_LER


async def ban_user(chat_id, i, rights):
    try:
        await zedub(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@zedub.zed_cmd(pattern=r"غادر(.*)")
async def leavme(leave):
    await leave.edit("**「❖╎جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@zedub.zed_cmd(pattern=r"اطردني(.*)")
async def kickme(leave):
    await leave.edit("**「❖╎جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@zedub.zed_cmd(pattern="بوتي$")
async def _(event):
    TG_BOT_USERNAME = Config.TG_BOT_USERNAME
    await event.reply(f"**「❖╎البـوت المسـاعد الخـاص بك هـو** \n {TG_BOT_USERNAME}")

@zedub.zed_cmd(pattern="حالتي ?(.*)")
async def rep(event):
    await event.edit("**- جـارِ التحقـق انتظـر قليـلاً . . .**")
    async with bot.conversation("@SpamBot") as tiba:
        try:
            dontTag = tiba.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await tiba.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(tiba.chat_id)
        except YouBlockedUserError:
            await zedub(unblock("SpamBot"))
            dontTag = tiba.wait_event(
                events.NewMessage(incoming=True, from_users=178220800))
            await tiba.send_message("/start")
            dontTag = await dontTag
            await bot.send_read_acknowledge(tiba.chat_id)
        await event.edit(f"**「❖╎حالة حسابـك حاليـاً هـي :**\n\n~ {dontTag.message.message}")    


@zedub.on(events.NewMessage(pattern="منصب؟"))
async def _(event):
    user = await event.get_sender()
    me = await event.client.get_me()
    zed_dev = 5571722913
    if user.id == zed_dev and user.id == me.id:
        return
    if user.id == zed_dev:
        await event.reply("**يب منصب حبي 🙈♥ .**")

@zedub.on(events.NewMessage(pattern="السلام عليكم"))
async def _(event):
    user = await event.get_sender()
    me = await event.client.get_me()
    zed_dev = 5571722913
    if user.id == zed_dev and user.id == me.id:
        return
    if user.id == zed_dev:
        await event.reply("**وعليكم السلام اهلين بمطور السورس💖🌹**")
        
@zedub.on(events.NewMessage(pattern="منو عمك"))
async def _(event):
    user = await event.get_sender()
    me = await event.client.get_me()
    zed_dev = 5571722913
    if user.id == zed_dev and user.id == me.id:
        return
    if user.id == zed_dev:
        await event.reply("**- انت عمي و تاج راسي @T_A_Tl**")

@zedub.on(admin_cmd(pattern="انشاء بريد(?: |$)(.*)"))
async def _(zedub):
    chat = "@TempMailBot"
    geez = await zedub.edit("**جاري انشاء بريد ...**")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(                incoming=True,                from_users=220112646            )            )            
            await conv.send_message("/start")
            await asyncio.sleep(1)
            await conv.send_message("/create")
            response = await response
            iqthonbot = ((response).reply_markup.rows[2].buttons[0].url)
            await iqthon.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await geez.edit("**قم بفتح الحظر عن : @TempMailBot للأستمرار بانشاء البريدات**")
            return
        await iqthon.edit(f"بريدك الخاص هوه : ~ `{response.message.message}`\n[انقر هنا للتحقق من رسائل بريدك]({iqthonbot})")

@zedub.zed_cmd(
    pattern="تفليش بالطرد$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    repevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await repevent.edit(
        f"**「❖╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedub.zed_cmd(
    pattern="للكل طرد$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    repevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await repevent.edit(
        f"**「❖╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedub.zed_cmd(
    pattern="تفليش$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    if event.text[1:].startswith("تفليش بالبوت"):
        return
    if event.text[1:].startswith("تفليش بالطرد"):
        return
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    repevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await repevent.edit(
        f"**「❖╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedub.zed_cmd(
    pattern="تصفير$",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "**- ليس لديك صلاحيات لأستخدام هذا الامر هنا**"
        )
    repevent = await edit_or_reply(event, "**- جـارِ . . .**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await repevent.edit(
        f"**「❖╎تم حظـر {success} عضو من {total} .. بنجـاح✓**"
    )


@zedub.zed_cmd(pattern="تفليش بالبوت$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedub(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedub.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"حظر @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"حظر {idofuser}"
        await zedub.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedub.zed_cmd(pattern="حظر_الكل$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedub(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedub.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"حظر @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"حظر {idofuser}"
        await zedub.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedub.zed_cmd(pattern="كتم_الكل$", groups_only=True)
async def banavot(event):
    chat_id = event.chat_id
    is_admin = False
    try:
        await zedub(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        pass
    spam_chats.append(chat_id)
    async for usr in zedub.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        username = usr.username
        usrtxt = f"كتم @{username}"
        if str(username) == "None":
            idofuser = usr.id
            usrtxt = f"كتم {idofuser}"
        await zedub.send_message(chat_id, usrtxt)
        await asyncio.sleep(0.5)
        await event.delete()
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@zedub.zed_cmd(pattern="الغاء التفليش", groups_only=True)
async def unbanbot(event):
    if not event.chat_id in spam_chats:
        return await event.edit("**- لاتوجـد عمليـة تفليـش هنـا لـ إيقافـها ؟!**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.edit("**「❖╎تم إيقـاف عمليـة التفليـش .. بنجـاح✓**")


@zedub.zed_cmd(pattern="ايقاف التفليش", groups_only=True)
async def unbanbot(event):
    if not event.chat_id in spam_chats:
        return await event.edit("**- لاتوجـد عمليـة تفليـش هنـا لـ إيقافـها ؟!**")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.edit("**「❖╎تم إيقـاف عمليـة التفليـش .. بنجـاح✓**")
