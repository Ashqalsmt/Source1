

import asyncio
import os
import shutil
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import edit_delete, logging, zedub

plugin_category = "الادوات"
DEFAULTUSER = gvarstatus("ALIVE_NAME") or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)
CHANGE_TIME = int(gvarstatus("CHANGE_TIME")) if gvarstatus("CHANGE_TIME") else 60
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

normzltext = "1234567890"

autopic_path = os.path.join(os.getcwd(), "yamenthon", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "yamenthon", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "yamenthon", "photo_pfp.png")


zedfont = gvarstatus("DEFAULT_PIC") or "yamenthon/helpers/styles/ZThon.ttf"
NAUTO = gvarstatus("Z_NAUTO") or "(الاسم تلقائي|الاسم الوقتي|اسم وقتي|اسم تلقائي)"
PAUTO = (
    gvarstatus("Z_PAUTO")
    or "(البروفايل تلقائي|الصوره الوقتيه|الصورة الوقتية|صوره وقتيه|البروفايل)"
)
BAUTO = (
    gvarstatus("Z_BAUTO")
    or "(البايو تلقائي|البايو الوقتي|بايو وقتي|نبذه وقتيه|النبذه الوقتيه)"
)


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            digitalpfp = gvarstatus("DIGITAL_PIC")
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(f"{zedfont}", 35)
        drawn_text.text((140, 70), current_time, font=fnt, fill=(280, 280, 280))
        img.save(autophoto_path)
        file = await zedub.upload_file(autophoto_path)
        try:
            if i > 0:
                await zedub(
                    functions.photos.DeletePhotosRequest(
                        await zedub.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await zedub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def autoname_loop():
    while AUTONAMESTART := gvarstatus("autoname") == "true":
        time.strftime("%d-%m-%y")
        HM = time.strftime("%I:%M")
        for normal in HM:
            if normal in normzltext:
                namerzfont = gvarstatus("ZI_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
                namefont = namerzfont[normzltext.index(normal)]
                HM = HM.replace(normal, namefont)
        ZEDT = gvarstatus("CUSTOM_ALIVE_EMZED") or "⏐"
        name = f"{HM}{ZEDT}"
        LOGS.info(name)
        try:
            await zedub(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        time.strftime("%d.%m.%Y")
        HM = time.strftime("%I:%M")
        for normal in HM:
            if normal in normzltext:
                namerzfont = gvarstatus("ZI_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
                namefont = namerzfont[normzltext.index(normal)]
                HM = HM.replace(normal, namefont)
        DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @YamenThon"
        bio = f"{DEFAULTUSERBIO} ⏐ {HM}"
        LOGS.info(bio)
        try:
            await zedub(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


@zedub.zed_cmd(pattern=f"{PAUTO}$")
async def _(event):
    digitalpfp = gvarstatus("DIGITAL_PIC")
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**التـغير التـلقائـي لصورتك ممكن بالفعل 𓆰**")
    addgvar("digitalpic", True)
    await edit_delete(event, "**تـم تفـعيل التـغير التـلقائـي لصورتك 𓆰**")
    await digitalpicloop()


@zedub.zed_cmd(pattern=f"{NAUTO}$")
async def _(event):
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, "`الاسم التلقائي ممكّن بالفعل 𓆰`")
    addgvar("autoname", True)
    await edit_delete(event, "**تـم بـدأ الاسـم التـلقائـي 𓆰**")
    await autoname_loop()


@zedub.zed_cmd(pattern=f"{BAUTO}$")
async def _(event):
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "** الـنبذة التلقائيه مفعـلة 𓆰**")
    addgvar("autobio", True)
    await edit_delete(event, "** تم تفعيل الـنبذة التلقائيه بنجاح 𓆰**")
    await autobio_loop()


@zedub.zed_cmd(
    pattern="الغاء ([\s\S]*)",
    command=("الغاء", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if (
        input_str == "البروفايل تلقائي"
        or input_str == "البروفايل"
        or input_str == "البروفايل التلقائي"
        or input_str == "الصوره الوقتيه"
        or input_str == "الصورة الوقتية"
    ):
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "** تم الغاء  البروفايل التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البروفايل التلقائي 𓆰**")
    if (
        input_str == "الاسم تلقائي"
        or input_str == "الاسم"
        or input_str == "الاسم التلقائي"
        or input_str == "الاسم الوقتي"
        or input_str == "اسم الوقتي"
    ):
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم إيقاف الاسم التلقائي الآن 𓆰**")
        return await edit_delete(event, "**لم يتم تمكين الاسم التلقائي 𓆰**")
    if (
        input_str == "البايو تلقائي"
        or input_str == "البايو"
        or input_str == "البايو التلقائي"
        or input_str == "البايو الوقتي"
        or input_str == "النبذه الوقتيه"
        or input_str == "النبذة الوقتية"
        or input_str == "بايو الوقتي"
        or input_str == "نبذه الوقتي"
    ):
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = (
                gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @YamenThon"
            )
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "** تم الغاء  البايو التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البايو التلقائي 𓆰**")


@zedub.zed_cmd(
    pattern="ايقاف ([\s\S]*)",
    command=("ايقاف", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if (
        input_str == "البروفايل تلقائي"
        or input_str == "البروفايل"
        or input_str == "البروفايل التلقائي"
        or input_str == "الصوره الوقتيه"
        or input_str == "الصورة الوقتية"
    ):
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "** تم الغاء  البروفايل التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البروفايل التلقائي 𓆰**")
    if (
        input_str == "الاسم تلقائي"
        or input_str == "الاسم"
        or input_str == "الاسم التلقائي"
        or input_str == "الاسم الوقتي"
        or input_str == "اسم الوقتي"
    ):
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم إيقاف الاسم التلقائي الآن 𓆰**")
        return await edit_delete(event, "**لم يتم تمكين الاسم التلقائي 𓆰**")
    if (
        input_str == "البايو تلقائي"
        or input_str == "البايو"
        or input_str == "البايو التلقائي"
        or input_str == "البايو الوقتي"
        or input_str == "النبذه الوقتيه"
        or input_str == "النبذة الوقتية"
        or input_str == "بايو الوقتي"
        or input_str == "نبذه الوقتي"
    ):
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = (
                gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @YamenThon"
            )
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "** تم الغاء  البايو التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البايو التلقائي 𓆰**")


@zedub.zed_cmd(
    pattern="انهاء ([\s\S]*)",
    command=("انهاء", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "digitalpfp": "To stop difitalpfp",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if (
        input_str == "البروفايل تلقائي"
        or input_str == "البروفايل"
        or input_str == "البروفايل التلقائي"
        or input_str == "الصوره الوقتيه"
        or input_str == "الصورة الوقتية"
    ):
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "** تم انهاء  البروفايل التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البروفايل التلقائي 𓆰**")
    if (
        input_str == "الاسم تلقائي"
        or input_str == "الاسم"
        or input_str == "الاسم التلقائي"
        or input_str == "الاسم الوقتي"
        or input_str == "اسم الوقتي"
    ):
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "**تم إيقاف الاسم التلقائي الآن 𓆰**")
        return await edit_delete(event, "**لم يتم تمكين الاسم التلقائي 𓆰**")
    if (
        input_str == "البايو تلقائي"
        or input_str == "البايو"
        or input_str == "البايو التلقائي"
        or input_str == "البايو الوقتي"
        or input_str == "النبذه الوقتيه"
        or input_str == "النبذة الوقتية"
        or input_str == "بايو الوقتي"
        or input_str == "نبذه الوقتي"
    ):
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = (
                gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @YamenThon"
            )
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "** تم انهاء  البايو التلقائي الان 𓆰**")
        return await edit_delete(event, "** لم يتم تمكين  البايو التلقائي 𓆰**")
    END_CMDS = [
        "البروفايل تلقائي",
        "الصوره الوقتيه",
        "الاسم تلقائي",
        "الاسم الوقتي",
        "البايو تلقائي",
        "البايو الوقتي",
        "النبذه الوقتيه",
        "البروفايل",
        "الاسم",
        "البايو",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"{input_str} is invalid end command.Mention clearly what should i end.",
            parse_mode=_format.parse_pre,
        )


zedub.loop.create_task(digitalpicloop())
zedub.loop.create_task(autoname_loop())
zedub.loop.create_task(autobio_loop())
