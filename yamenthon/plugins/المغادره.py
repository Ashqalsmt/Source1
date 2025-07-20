from telethon.tl.types import Channel, Chat, ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from ..core.managers import edit_or_reply
from .. import zedub

@zedub.zed_cmd(pattern="مغادره القنوات$")
async def leave_channels(event):
    reply = await edit_or_reply(event, "✧ جارٍ مغادرة القنوات التي لا تملكها أو تديرها ...")
    count = 0
    me = await event.client.get_me()
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and not entity.megagroup:
            try:
                participant = await event.client(GetParticipantRequest(entity.id, me.id))
                if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
                    continue  # تخطى القناة إن كنت مالك أو مشرف
                await event.client(LeaveChannelRequest(entity.id))
                count += 1
            except Exception:
                continue
    await reply.edit(f"**✧ تم مغادرة `{count}` قناة (غير التي تملكها أو تديرها)** ✅")

@zedub.zed_cmd(pattern="مغادره المجموعات$")
async def leave_groups(event):
    reply = await edit_or_reply(event, "**✧ جارٍ مغادرة المجموعات التي لا تملكها أو تديرها ...**")
    count = 0
    me = await event.client.get_me()
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if (isinstance(entity, Channel) and entity.megagroup) or isinstance(entity, Chat):
            try:
                participant = await event.client(GetParticipantRequest(entity.id, me.id))
                if isinstance(participant.participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
                    continue  # لا تغادر إن كنت المالك أو مشرف
                await event.client(LeaveChannelRequest(entity.id))
                count += 1
            except Exception:
                continue
    await reply.edit(f"**✧ تم مغادرة `{count}` مجموعة (غير التي تملكها أو تديرها) ✅**")
