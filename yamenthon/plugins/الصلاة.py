import requests
import json
from . import zedub
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "البحث"

@zedub.zed_cmd(
    pattern="صلاة ([\s\S]*)",
    command=("صلاة", plugin_category),
    info={
        "header": "اوقـات الصـلاة لـ عواصـم الـدول العـربيـة",
        "الاستـخـدام": "{tr}صلاة + العاصمـة",
    },
)
async def get_adzan(adzan):
    city_input = adzan.pattern_match.group(1).strip()

    # قاموس لتحديد المدن والدول الخاصة بالمدينة
    cities = {
        "صنعاء": ("Sanaa", "Yemen", "صنعـاء", "اليمـن"),
        "القاهرة": ("Cairo", "Egypt", "القاهـرة", "مصـر"),
        "بغداد": ("Baghdad", "Iraq", "بغـداد", "العـراق"),
        "دمشق": ("Damascus", "Syria", "دمشـق", "سـوريا"),
        "الدوحة": ("Doha", "Qatar", "الدوحـة", "قطـر"),
        "مسقط": ("Muscat", "Oman", "مسقـط", "سلطنـة عمـان"),
        "مكة": ("Mecca", "Saudi Arabia", "مكـه المكـرمـه", "المملكـة العربيـه السعـودية"),
        "بيروت": ("Beirut", "Lebanon", "بيـروت", "لبنـان"),
    }

    if city_input not in cities:
        await edit_delete(
            adzan,
            f"** لم يـتم العثور على هـذه المدينه {city_input}**\n**-يرجى كتابة اسم العاصمـة أو الدولـة بشكل صحيح** ",
            5,
        )
        return

    city_en, country_en, city_ar, country_ar = cities[city_input]

    url = f"https://api.aladhan.com/v1/timingsByCity?city={city_en}&country={country_en}&method=4"
    response = requests.get(url)

    if response.status_code != 200:
        await edit_delete(
            adzan,
            f"** حدث خطأ في جلب بيانات الصلاة للمدينة {city_ar} **",
            5,
        )
        return

    data = response.json()
    timings = data["data"]["timings"]
    date_gregorian = data["data"]["date"]["gregorian"]["date"]
    date_hijri = data["data"]["date"]["hijri"]["date"]

    msg = (
        f"<b>🕋╎اوقـات الصـلاة بالتـوقيت المحلـي لعواصـم الـدول</b>\n\n"
        f"<b>المـدينة     :</b> {city_ar}\n"
        f"<b>الـدولة  :</b> {country_ar}\n"
        f"<b>التـاريخ     :</b> {date_gregorian}\n"
        f"<b>الهـجري    :</b> {date_hijri}\n\n"
        f"<b>الامـساك    :</b> {timings['Imsak']}\n"
        f"<b>شـروق الشمس  :</b> {timings['Sunrise']}\n"
        f"<b>الـفجر     :</b> {timings['Fajr']}\n"
        f"<b>الضـهر    :</b> {timings['Dhuhr']}\n"
        f"<b>العـصر      :</b> {timings['Asr']}\n"
        f"<b>غـروب الشمس   :</b> {timings['Sunset']}\n"
        f"<b>المـغرب  :</b> {timings['Maghrib']}\n"
        f"<b>العشـاء     :</b> {timings['Isha']}\n"
        f"<b>منتـصف الليل :</b> {timings['Midnight']}\n\n"
        f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝙔𝘼𝙈𝙀𝙉𝙏𝙃𝙊𝙉╎@YamenThon"
    )

    await edit_or_reply(adzan, msg, parse_mode="html")
