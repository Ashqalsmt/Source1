#الملف تم تحديثه وتعديله بالكامل بحيث يكون يعمل بشكل أفضل 
#الملف تحديث وتعديل الاسطوره عاشق الصمت 
#بطل الخماط وذكر المصدر وصير مطور 
#ملف اوقـات الصـلاة تخمطها هههههههههههه🤣

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
    "عدن": ("Aden", "Yemen", "عـدن", "اليمـن"),
    "القاهرة": ("Cairo", "Egypt", "القاهـرة", "مصـر"),
    "الإسكندرية": ("Alexandria", "Egypt", "الإسكندريـة", "مصـر"),
    "بغداد": ("Baghdad", "Iraq", "بغـداد", "العـراق"),
    "الموصل": ("Mosul", "Iraq", "الموصـل", "العـراق"),
    "دمشق": ("Damascus", "Syria", "دمشـق", "سـوريا"),
    "حلب": ("Aleppo", "Syria", "حلـب", "سـوريا"),
    "الرياض": ("Riyadh", "Saudi Arabia", "الريـاض", "السعوديـة"),
    "مكة": ("Makkah", "Saudi Arabia", "مكـه المكرّمة", "السعوديـة"),
    "المدينة": ("Madinah", "Saudi Arabia", "المدينـة المنـورة", "السعوديـة"),
    "جدة": ("Jeddah", "Saudi Arabia", "جـدة", "السعوديـة"),
    "دبي": ("Dubai", "UAE", "دبـي", "الإمـارات"),
    "أبوظبي": ("Abu Dhabi", "UAE", "أبو ظبـي", "الإمـارات"),
    "الشارقة": ("Sharjah", "UAE", "الشارقـة", "الإمـارات"),
    "عجمان": ("Ajman", "UAE", "عجـمان", "الإمـارات"),
    "رأس الخيمة": ("Ras Al Khaimah", "UAE", "رأس الخيـمة", "الإمـارات"),
    "أم القيوين": ("Umm Al Quwain", "UAE", "أم القيويـن", "الإمـارات"),
    "مسقط": ("Muscat", "Oman", "مسقـط", "سلطنة عمـان"),
    "الدوحة": ("Doha", "Qatar", "الدوحـة", "قطـر"),
    "المنامة": ("Manama", "Bahrain", "المنـامة", "البحريـن"),
    "بيروت": ("Beirut", "Lebanon", "بيـروت", "لبنـان"),
    "الخرطوم": ("Khartoum", "Sudan", "الخـرطوم", "السـودان"),
    "الرباط": ("Rabat", "Morocco", "الربـاط", "المغـرب"),
    "تونس": ("Tunis", "Tunisia", "تـونس", "تـونس"),
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
