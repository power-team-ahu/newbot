# -*- coding: utf-8 -*-
"""
Power Team Bot
- أسماء المواد كلها بالعربي ومرتبة أبجدياً.
- زر /start يرسل رسالة الترحيب المطلوبة ويعرض القوائم.
- أزرار تحكم (Inline) مع روابط مباشرة لملفات Google Drive للوصول السريع دون تأخير.
- قوائم فرعية: المواد / المختبرات / الخطة الهندسية (إن وجدت) لكل تخصّص.
- ترقيم/تقسيم تلقائي (Pagination) عند كثرة المواد لتجنب ازدحام الأزرار.
- مهيّأ على python-telegram-bot (v21+).

لتشغيله:
1) pip install python-telegram-bot==21.*
2) عدّل BOT_TOKEN أدناه.
3) python bot.py
"""

import asyncio
from typing import Dict, List, Tuple

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ضع توكن البوت هنا
BOT_TOKEN = "8447138394:AAHFEKr1hwxqlEas0h11UVeDar5a1O2j3F8"

# ---------------------------
# بيانات المواد (روابط Google Drive)
# ---------------------------

DATA: Dict[str, Dict[str, Dict[str, str]]] = {
    "المواد المشتركة": {
        "المواد": {
            "الانظمة المضمنة": "https://drive.google.com/drive/folders/16w1rVH6Mw0-qV5rTYFtiUf5bUJrYOCvX?usp=drive_link",
            "رياضيات هندسية 1": "https://drive.google.com/drive/folders/1CVTPuJbPDaKZG7cWV83VacVbvFI2M5fI?usp=drive_link",
            "اشارات و انظمة": "https://drive.google.com/drive/folders/1e1ApCeq_whrJiD8DlNoal9rljXywawOa?usp=drive_link",
            "اقتصاد هندسي": "https://drive.google.com/drive/folders/16mit6Uq7ZeojYLbZhGNrJZjq7_Ic1rVO?usp=drive_link",
            "الكترونات رقمية": "https://drive.google.com/drive/folders/1fqSq0h3acJox-5dAPsTcxQ7hsZjOeTds?usp=drive_link",
            "الكترونيات 1": "https://drive.google.com/drive/folders/1BRE5v-R_Ne1iEsTo-e7uflRn3v-uXFE1?usp=drive_link",
            "الكترونيات 2": "https://drive.google.com/drive/folders/1hc1a1ZsF5jb1R9vAS1_joFPkAT5CMGpm?usp=drive_link",
            "تحليل عددي للمهندسين": "https://drive.google.com/drive/folders/12s3eddwIl0l2XmL9-ghxPVQ-kv3oizb6?usp=drive_link",
            "تصميم دارات منطقية": "https://drive.google.com/drive/folders/1TBDQfJ9_eqown8diNdjE8CGKSjO27iYO?usp=drive_link",
            "دارات كهربائية 1": "https://drive.google.com/drive/folders/1CcyNHCm9nhXd4soPVdZgAQIx22A9HLvZ?usp=drive_link",
            "دارات كهربائية 2": "https://drive.google.com/drive/folders/1AtWqrScCDy4IktO5_ObhKs_A9zjAcaK8?usp=drive_link",
            "رياضيات هندسية 2": "https://drive.google.com/drive/folders/16gp5DpwmIMQ_YZ8oR0rxbo7iLZb7CwO3?usp=drive_link",
            "كالكولس 1": "https://drive.google.com/drive/folders/1FjpEmPVkqQ6CiRZvHD44lXqsjzZdCI8?usp=drive_link",
            "كالكولس 2": "https://drive.google.com/drive/folders/1FAnxWF0L_6Fh4YEZK03rB55fiJNMswBU?usp=drive_link",
            "لغة الاسمبلي": "https://drive.google.com/drive/folders/1jXgPhN1qLrod1m9gvC2RM8Hwon8QOvn0?usp=drive_link",
            "لغة البرمجة  ++C": "https://drive.google.com/drive/folders/17FKX_BNG4xl1vXgzO4TkN61H_trubDma?usp=drive_link",
            "مدخل هندسي": "https://drive.google.com/drive/folders/1mv-L56blvA3WFcLWjqcqptXntk9IKvyz?usp=drive_link",
            "فيزياء 1": "https://drive.google.com/drive/folders/1mVn_2RcI-KlQY7ItqEc_huZ7FetxekzF?usp=drive_link",
            "فيزياء 2": "https://drive.google.com/drive/folders/11gTuumDU0BeKnSyVAizDQ3Yg6Nw_bKKU?usp=drive_link",
        },
        "المختبرات": {
            "مختبر الاسمبلي": "https://drive.google.com/drive/folders/1nMOBq2CF7aJrkRKTDwjjn1U9Z8A9YDt1?usp=drive_link",
            "مختبر الأنظمة المضمنة": "https://drive.google.com/drive/folders/1JPV31gz3mrl88NHeYEQJQKmAd2Eh3B7X?usp=drive_link",
            "مختبر الدارات المنطقية": "https://drive.google.com/drive/folders/1-KrNw7-ghLxNUeI5mCRtsu7JEoHhuaKF?usp=drive_link",
            "مختبر الكترونيات": "https://drive.google.com/drive/folders/10C8EwOYndd1DhNq_pjoMsOV6Y6CTAn6M?usp=drive_link",
            "مختبر الكترونيات رقمية": "https://drive.google.com/drive/folders/17UaZ1c92fqO8a15ES_WKG5c-OAMscG2X?usp=drive_link",
            "مختبر تطبيقات هندسية": "https://drive.google.com/drive/folders/12hCEJP5N_2ZigA9CzP1XZl_5p7gvkzJS?usp=drive_link",
            "مختبر دارات كهربائية": "https://drive.google.com/drive/folders/1YVc1NurxA1Gn4kJFvFO4easJG47trLDh?usp=drive_link",
            "مختبر فيزياء 1": "https://drive.google.com/drive/folders/1AdKwQhqKdhBSdkxc2zKoJN_X0GIVC5Uj?usp=drive_link",
            "مختبر فيزياء 2": "https://drive.google.com/drive/folders/19wiHOVXDaXAAq60vPSfH0fWrzL2N7hOR?usp=drive_link",
        },
    },

    "هندسة الكهرباء": {
        "المواد": {
            "آلات 1": "https://drive.google.com/drive/folders/1PINq7nmoMgmp2Zgxbh0p2COjruLNeOVk?usp=drive_link",
            "آلات 2": "https://drive.google.com/drive/folders/1jUUcEVlbiVik4-hHRj4Wnw4g7JS7nHuV?usp=drive_link",
            "اتصالات تناظرية": "https://drive.google.com/drive/folders/12ULxRPTPeF4q9m0SeUbqslix1SSqjOTq?usp=drive_link",
            "اتصالات رقمية": "https://drive.google.com/drive/folders/12SKHpj56vFEFYsoHv19MZwBuHk1ZqSgf?usp=drive_link",
            "اجهزة وقياسات": "https://drive.google.com/drive/folders/1QUJA19IgCdrlyKUFEHRa2gGMqJq9lRXz?usp=drive_link",
            "الاحتمالات و العمليات العشوائية": "https://drive.google.com/drive/folders/1-PGGdRLOLDfySyksTjB0Rl5wS8XDnI_c?usp=drive_link",
            "الكترونيات الاتصالات": "https://drive.google.com/drive/folders/1-h-RcBRx1YXnibnd1n7KpB6PTGIgxPUP?usp=drive_link",
            "الكترونيات القوى": "https://drive.google.com/drive/folders/18zhwWxkFfwDFn1yBzGfth8IG0R0ANBR5?usp=drive_link",
            "أنظمة الاتصالات": "https://drive.google.com/drive/folders/1G798-2xPhroLY2Jq9L3_WCTrqiCDVzOL?usp=drive_link",
            "انظمة الحماية": "https://drive.google.com/drive/folders/1xIL4HPUuACb-eu0z32h_r8XaIOzSC1sJ?usp=drive_link",
            "انظمة القوى الكهربائية  1": "https://drive.google.com/drive/folders/1SmkgqX_0ddBa4oaeBSHOQlvJztLF7cVW?usp=drive_link",
            "انظمة القوى الكهربائية  2": "https://drive.google.com/drive/folders/1hfSkR6MOB7yKckyGmnKZ9v9Pa9mzUSLy?usp=drive_link",
            "انظمة تحكم": "https://drive.google.com/drive/folders/1wxXIpA7leuwSjnIVvyoR-BRpEF9fWGQ9?usp=drive_link",
            "انظمة نقل و توريع": "https://drive.google.com/drive/folders/1zlAri1RTRaSMdcjpwmHjzoZAZJOJwhA3?usp=drive_link",
            "شبكات الحاسوب": "https://drive.google.com/drive/folders/1_MHa1wcLJnxM8G0AGL0GmbL-W478JsUC?usp=drive_link",
            "كهرومغناطيسة 1": "https://drive.google.com/drive/folders/1q8nSPugWLnzpeUbm4VZi01D-qibfb9-i?usp=drive_link",
            "كهرومغناطيسة  2": "https://drive.google.com/drive/folders/11XdPoGrIbALeps1qgIUJfsm2I4a7cqen?usp=drive_link",
        },
        "المختبرات": {
            "مختبر آلات كهربائية": "https://drive.google.com/drive/folders/1Qyyn5Wr28qnykQ3BImgLoM9zRENKSr3E?usp=drive_link",
            "مختبر اجهزة و قياسات": "https://drive.google.com/drive/folders/1-vVXnxN_ZXJmBHOEkFaFIc2DuyTlaTXT?usp=drive_link",
            "مختبر الاتصالات": "https://drive.google.com/drive/folders/1HA1WOQIto-YgMG0VzB5jkL_3y9Hj7cM6?usp=drive_link",
            "مختبر القوى الكهربائية": "https://drive.google.com/drive/folders/1F5pVt4kmwHW2eVqTNQI2w58-l-Mlgd4N?usp=drive_link",
            "مختبر انظمة التحكم": "https://drive.google.com/drive/folders/1-wq6lVykbUtCu5AuS3h_LMeoP7ZQjiIj?usp=drive_link",
        },
        "الخطة الهندسية": {
            "الخطة الهندسية الكهربائية": "https://drive.google.com/drive/folders/1-18zMVKS9l_cPnir_owlE7Fd2HeDr6SU?usp=drive_link",
        },
    },

    "هندسة الاتصالات": {
        "المواد": {
            "اتصالات ضوئية": "https://drive.google.com/drive/folders/1B76DmtbKA1MgLhfiDzciA0rJg0Le9WRb?usp=drive_link",
            "الاتصالات الرقمية": "https://drive.google.com/drive/folders/1np7LxIO90cylT-O8krDlbUfo8P4ffd_X?usp=drive_link",
            "الكترونيات الاتصالات": "https://drive.google.com/drive/folders/19Tqs-mK9O_OcAdWQw3Nb0w9T_29_Upsx?usp=drive_link",
            "انظمة اتصالات": "https://drive.google.com/drive/folders/1vnWlDpxtLeum0McCTlr1M4Ug_jjVYlgx?usp=drive_link",
            "انظمة الاتصالات": "https://drive.google.com/drive/folders/1cwt2m3aq3WUhdb8efT6uofnsVPNyWX5e?usp=drive_link",
            "هندسة الامواج الدقيقة": "https://drive.google.com/drive/folders/1PhjRiR4r1Eo-wRk2mEfN3OgYUL9MbIgn?usp=drive_link",
            "هندسة الهوائيات": "https://drive.google.com/drive/folders/1GIpRqnkRhZ0SDbtd18XG36_c1BuBD_kp?usp=drive_link",
            "اتصالات تناظرية": "https://drive.google.com/drive/folders/12ULxRPTPeF4q9m0SeUbqslix1SSqjOTq?usp=drive_link",
            "اتصالات رقمية": "https://drive.google.com/drive/folders/12SKHpj56vFEFYsoHv19MZwBuHk1ZqSgf?usp=drive_link",
            "اجهزة وقياسات": "https://drive.google.com/drive/folders/1QUJA19IgCdrlyKUFEHRa2gGMqJq9lRXz?usp=drive_link",
            "الاحتمالات و العمليات العشوائية": "https://drive.google.com/drive/folders/1-PGGdRLOLDfySyksTjB0Rl5wS8XDnI_c?usp=drive_link",
            "الكترونيات القوى": "https://drive.google.com/drive/folders/18zhwWxkFfwDFn1yBzGfth8IG0R0ANBR5?usp=drive_link",
            "أنظمة الاتصالات": "https://drive.google.com/drive/folders/1G798-2xPhroLY2Jq9L3_WCTrqiCDVzOL?usp=drive_link",
            "انظمة الحماية": "https://drive.google.com/drive/folders/1xIL4HPUuACb-eu0z32h_r8XaIOzSC1sJ?usp=drive_link",
            "انظمة القوى الكهربائية  1": "https://drive.google.com/drive/folders/1SmkgqX_0ddBa4oaeBSHOQlvJztLF7cVW?usp=drive_link",
            "انظمة القوى الكهربائية  2": "https://drive.google.com/drive/folders/1hfSkR6MOB7yKckyGmnKZ9v9Pa9mzUSLy?usp=drive_link",
            "انظمة تحكم": "https://drive.google.com/drive/folders/1wxXIpA7leuwSjnIVvyoR-BRpEF9fWGQ9?usp=drive_link",
            "انظمة نقل و توريع": "https://drive.google.com/drive/folders/1zlAri1RTRaSMdcjpwmHjzoZAZJOJwhA3?usp=drive_link",
            "شبكات الحاسوب": "https://drive.google.com/drive/folders/1_MHa1wcLJnxM8G0AGL0GmbL-W478JsUC?usp=drive_link",
            "كهرومغناطيسة 1": "https://drive.google.com/drive/folders/1q8nSPugWLnzpeUbm4VZi01D-qibfb9-i?usp=drive_link",
            "كهرومغناطيسة  2": "https://drive.google.com/drive/folders/11XdPoGrIbALeps1qgIUJfsm2I4a7cqen?usp=drive_link",
            "معالجة الاشارات الرقمية": "https://drive.google.com/drive/folders/1TQIz73_CjdtgwzpW5Ck1Osi_l1lxU34R?usp=drive_link",
        },
        "المختبرات": {
            "مختبر اجهزة و قياسات": "https://drive.google.com/drive/folders/1-vVXnxN_ZXJmBHOEkFaFIc2DuyTlaTXT?usp=drive_link",
            "مختبر الاتصالات": "https://drive.google.com/drive/folders/1HA1WOQIto-YgMG0VzB5jkL_3y9Hj7cM6?usp=drive_link",
            "مختبر القوى الكهربائية": "https://drive.google.com/drive/folders/1F5pVt4kmwHW2eVqTNQI2w58-l-Mlgd4N?usp=drive_link",
            "مختبر انظمة التحكم": "https://drive.google.com/drive/folders/1-wq6lVykbUtCu5AuS3h_LMeoP7ZQjiIj?usp=drive_link",
            "مختبر انظمة تحكم": "https://drive.google.com/drive/folders/1rug3To79Xdit_pHjkWOls31wVyYlZamd?usp=drive_link",
            "مختبر الامواج الدقيقة": "https://drive.google.com/drive/folders/1zql-s6vlRPP11y66VxC72aP-lyltNaSv?usp=drive_link",
        },
        "الخطة الهندسية": {
            "الخطة الهندسية للاتصالات": "https://drive.google.com/drive/folders/1PnfqKcvVDFW1RbJ6yTbZafQmEa7-kst2?usp=drive_link",
        },
    },

    "هندسة الحاسوب": {
        "المواد": {
            "الشبكات العصبونية و المنطق المشوش": "https://drive.google.com/drive/folders/1V9HzzgZp9w2FGJ7htucboVCvsIWwRNPS?usp=drive_link",
            "انظمة تحكم": "https://drive.google.com/drive/folders/1wxXIpA7leuwSjnIVvyoR-BRpEF9fWGQ9?usp=drive_link",
            "الاحتمالات و العمليات العشوائية": "https://drive.google.com/drive/folders/1-PGGdRLOLDfySyksTjB0Rl5wS8XDnI_c?usp=drive_link",
            "شبكات الحاسوب": "https://drive.google.com/drive/folders/1_MHa1wcLJnxM8G0AGL0GmbL-W478JsUC?usp=drive_link",
            "اتصالات تناظرية و رقمية": "https://drive.google.com/drive/folders/15y-6_rPWDSfY3-KXG6fE1hCTt4ppJa_X?usp=drive_link",
            "الشبكات اللاسلكية": "https://drive.google.com/drive/folders/1m7X1_BERjU3vXxNGZGhgmhQvpEX3hvEY?usp=drive_link",
            "النظم الموزعة و تطبيقاتها": "https://drive.google.com/drive/folders/1G3Ne-mGxUmDcuXMj1AFPi6zdURb7W1uo?usp=drive_link",
            "أمن و حماية شبكات الحاسوب": "https://drive.google.com/drive/folders/10HDJsEiMYJg5H1hiJ3CkjIFdf6EBXlUm?usp=drive_link",
            "أنظمة نشغيل الحاسوب": "https://drive.google.com/drive/folders/1mgDIu-s7QUIvvOm7PFSgR2z887x1jBap?usp=drive_link",
            "تصميم الأنظمة الرقمية": "https://drive.google.com/drive/folders/1f49GBNxFSHCVqQ5IbefOKSjOWhB2geyv?usp=drive_link",
            "تطبيقات الهواتف المحمولة المحوسبة": "https://drive.google.com/drive/folders/1YH7lXvNZdBjIYdxIR9G0rfJzSFESutLQ?usp=drive_link",
            "تصميم و تنظيم الحاسوب": "https://drive.google.com/drive/folders/1PX-p7kx1iqW_OQj27a-hwCCzh3NzrCJ8?usp=drive_link",
            "توصيل الحاسوب و الطرفيات": "https://drive.google.com/drive/folders/1wiwMcWxAk808uTV6vd9z2rZjjCJAY6xn?usp=drive_link",
            "رياضيات متقطعة": "https://drive.google.com/drive/folders/1em5CrJQnF5TbrHrRlvWEEfKDwxiAKiW0?usp=drive_link",
            "شبكات الحاسوب المتقدمة": "https://drive.google.com/drive/folders/1M2ze9YtEGWunTih5W4_O8w9OBdouOsfy?usp=drive_link",
            "معالجة الاشارات الرقمية": "https://drive.google.com/drive/folders/1KyvEovWMNVx0m5YDnO3fyv-C6zorPnnr?usp=drive_link",
            "نمذجة و محاكاة الحاسوب": "https://drive.google.com/drive/folders/1RKzZ1rVlHe5g6Nx3ABrbZVToN2x62AHY?usp=drive_link",
            "معالجة الصوت و الصورة": "https://drive.google.com/drive/folders/1RKFZ8au5Rvogorbu118hOVgfJyBt5wwv?usp=drive_link",
            "معمارية الحاسوب": "https://drive.google.com/drive/folders/1_VLoOOCoHms-WSgJcoF2lOOMYntgtJMf?usp=drive_link",
        },
        "المختبرات": {
            "مختبر شبكات الحاسوب": "https://drive.google.com/drive/folders/1RJr264U0BuQvIWUBSpOLW4LOJi6llGie?usp=drive_link",
            "مختبر أنظمة تحكم": "https://drive.google.com/drive/folders/1rug3To79Xdit_pHjkWOls31wVyYlZamd?usp=drive_link",
            "مختبر صيانة الحاسوب": "https://drive.google.com/drive/folders/1YKsZ9evEHkDrPLSlI9maFLVUktVmNjkp?usp=drive_link",
        },
        "الخطة الهندسية": {
            "الخطة الهندسية للحاسوب": "https://drive.google.com/drive/folders/1spc3iflGpHM4Mdg3dP2aLB3vWULqoIk_?usp=drive_link",
        },
    },

    "هندسة امن الشبكات و المعلومات": {
        "المواد": {
            "البرمجة الكينونية": "https://drive.google.com/drive/folders/1LVJ8hAmjVwhCFQ87Im0jWwy_mf_c3Icb?usp=drive_link",
            "التشفير و امن المعلومات": "https://drive.google.com/drive/folders/1LnrM96VCevmMeXRQUo4STNCmMOScyMWT?usp=drive_link",
            "الخوارزميات و نراكيب البيانات": "https://drive.google.com/drive/folders/1k2_9U_FGj2YxvvCJbksyKTo4wZ_aFdQf?usp=drive_link",
            "الذكاء الاصطناعي": "https://drive.google.com/drive/folders/14gHUcSTUwG1XB5F_0ef6FNIk6m68PKtO?usp=drive_link",
            "الشبكات العصبونية و المنطق المشوش": "https://drive.google.com/drive/folders/1V9HzzgZp9w2FGJ7htucboVCvsIWwRNPS?usp=drive_link",
            "أمن البرمجيات": "https://drive.google.com/drive/folders/1ymvvPXw2_s2X5b_GRZELxix5k5Fa8oGq?usp=drive_link",
            "أمن التطبيقات و الهواتف": "https://drive.google.com/drive/folders/1osmqhj9SFCj1Wr4vSvepdylwQwch5yLY?usp=drive_link",
            "امن الحوسبة السحابية": "https://drive.google.com/drive/folders/1LJB5XpuNf7BvQ8tmNEIumb4Y5gy851dw?usp=drive_link",
            "امن الشبكات": "https://drive.google.com/drive/folders/1WF8ZWB88Irmj6LEvoquIIkFFimcAddXJ?usp=drive_link",
            "امن الشبكات اللاسلكية": "https://drive.google.com/drive/folders/1mOmvhewV6ftGTQV4pqcmQ5u7DFHvlnMN?usp=drive_link",
            "أمن الكونات المادية": "https://drive.google.com/drive/folders/1gZP2yrYP8pbNUM_kf0BnxphY1JGyp4GT?usp=drive_link",
            "امن انظمة التشغيل": "https://drive.google.com/drive/folders/14s9_7EgAG3YeRObWCRcEho_H0Zpy0tRx?usp=drive_link",
            "انترنت الاشياء": "https://drive.google.com/drive/folders/1bRDo4TT9cuD1nvi9TZwXoDu_ppzfckmw?usp=drive_link",
            "أنظمة الحماية و الدفاع": "https://drive.google.com/drive/folders/11ZUn_7JuNNDOKStzboqY4VlqE-hvtfYU?usp=drive_link",
            "أنظمة الشبكات اللاسلكية": "https://drive.google.com/drive/folders/1dKaY71SbKOxBqZSqIc66SUDhgY9PX3yI?usp=drive_link",
            "أنظمة تشغيل الحاسوب": "https://drive.google.com/drive/folders/11Jg369D7W8x-A_Ssvr3pVBYqc8Ep-lEm?usp=drive_link",
            "أنظمة قواعد البيانات": "https://drive.google.com/drive/folders/1sELRmZC3oT_e9vFUZFBwacwBKdgpEFWp?usp=drive_link",
            "برمجة الشبكات": "https://drive.google.com/drive/folders/1M4k7yaFDAEJCMZ6ST3gCb_--fR9usKaD?usp=drive_link",
            "بروتوكولات شبكات الحاسوب": "https://drive.google.com/drive/folders/1Hlp8eKifI-l6PKc7zkwRtpGGaVJwdfKy?usp=drive_link",
            "تحليل أداء الشبكات": "https://drive.google.com/drive/folders/1wzkxjHR8Go2uMkbhHFuHinjc2B8dqNEZ?usp=drive_link",
            "تراسل البيانات": "https://drive.google.com/drive/folders/1a148FlGkeHGFJ2n9exSM10H7w5KYgF_Y?usp=drive_link",
            "تشريعات الفضاء الإلكتروني": "https://drive.google.com/drive/folders/1al9hXo4mI8lcMLeQd_GQEGECqCSPZCr8?usp=drive_link",
            "تقييم أمن الأنظمة": "https://drive.google.com/drive/folders/1wMYhZ_KoP_0n0BqFxLINh3tHH1Uhg0gT?usp=drive_link",
            "رياضيات متقطعة": "https://drive.google.com/drive/folders/1em5CrJQnF5TbrHrRlvWEEfKDwxiAKiW0?usp=drive_link",
            "شبكات الحاسوب": "https://drive.google.com/drive/folders/1_MHa1wcLJnxM8G0AGL0GmbL-W478JsUC?usp=drive_link",
            "معمارية الأنظمة الأمنة": "https://drive.google.com/drive/folders/1W_8n50PtAcrl8GRxgLSEqtNutdptfB2s?usp=drive_link",
            "معمارية الحاسوب": "https://drive.google.com/drive/folders/1RO973dl77oWqRCIMg3ARvybpgMyzPJTI?usp=drive_link",
            "نمذجة و محاكاة النظم": "https://drive.google.com/drive/folders/1j3EBoMpRaPtv4NJHbJ-2qs3g0_rbbjWx?usp=drive_link",
        },
        "المختبرات": {
            "مختبر البرمجة الكينونية": "https://drive.google.com/drive/folders/1YUHf02SJM6uauGP4liTRfspfv_NFsSIG?usp=drive_link",
            "مختبر أمن البرمجيات": "https://drive.google.com/drive/folders/1DhhxihaDJltYwqMjiwPgjF6g4KKTKnXd?usp=drive_link",
            "مختبر امن الشبكات": "https://drive.google.com/drive/folders/1pJm5fA5wuvo9TRHfSnY41If8IWrAsBOL?usp=drive_link",
            "مختبر انظمة التشغبل": "https://drive.google.com/drive/folders/1u9xC89UFXEsKKwbWSivd1Y1LcNp6jvJm?usp=drive_link",
            "مختبر شبكات الحاسوب": "https://drive.google.com/drive/folders/1RJr264U0BuQvIWUBSpOLW4LOJi6llGie?usp=drive_link",
        },
        "الخطة الهندسية": {
            "الخطة الهندسية لأمن الشبكات": "https://drive.google.com/drive/folders/1xMvm4xaK83O9iooLvBBCweJIDAM3mwVx?usp=drive_link",
        },
    },
}

# ---------------------------
# ترتيب أبجدي عربي (مفتاح ترتيب)
# ---------------------------

AR_ORDER = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
AR_INDEX = {ch: i for i, ch in enumerate(AR_ORDER)}

REPLACE_MAP = str.maketrans({
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ى": "ي",
    "ة": "ه",
    "ؤ": "و",
    "ئ": "ي",
    "ـ": "",   # تطويل
})

def normalize_ar(s: str) -> str:
    s = s.strip().translate(REPLACE_MAP)
    # تجاهل "ال" في بداية الكلمة لتحسين الترتيب
    if s.startswith("ال") and len(s) > 2:
        s = s[2:]
    return s

def arabic_sort_key(s: str) -> Tuple[int, ...]:
    s_norm = normalize_ar(s)
    return tuple(AR_INDEX.get(ch, 100) for ch in s_norm)

def sorted_items(d: Dict[str, str]) -> List[Tuple[str, str]]:
    return sorted(d.items(), key=lambda kv: arabic_sort_key(kv[0]))

# ---------------------------
# مفاتيح الرد وأسماء الأقسام
# ---------------------------

CATEGORIES = list(DATA.keys())  # الرئيسية
SECTIONS_MAP = {
    "المواد": "S0",
    "المختبرات": "S1",
    "الخطة الهندسية": "S2",
}
SECTIONS_REVERSE = {v: k for k, v in SECTIONS_MAP.items()}

PAGE_SIZE = 10

def main_menu_kb() -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, cat in enumerate(CATEGORIES, start=1):
        row.append(InlineKeyboardButton(cat, callback_data=f"CAT|{i-1}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)

def section_menu_kb(cat_idx: int) -> InlineKeyboardMarkup:
    cat = CATEGORIES[cat_idx]
    available_sections = list(DATA[cat].keys())
    rows = []
    # نعرض الأقسام الموجودة فقط
    for sec in ["المواد", "المختبرات", "الخطة الهندسية"]:
        if sec in available_sections:
            rows.append([InlineKeyboardButton(sec, callback_data=f"SEC|{cat_idx}|{SECTIONS_MAP[sec]}")])
    rows.append([InlineKeyboardButton("◀️ رجوع للقائمة الرئيسية", callback_data="BACK|MAIN")])
    return InlineKeyboardMarkup(rows)

def items_menu_kb(cat_idx: int, sec_code: str, page: int = 1) -> InlineKeyboardMarkup:
    cat = CATEGORIES[cat_idx]
    sec = SECTIONS_REVERSE[sec_code]
    items = sorted_items(DATA[cat][sec])
    total = len(items)
    start = (page - 1) * PAGE_SIZE
    end = min(start + PAGE_SIZE, total)
    page_items = items[start:end]

    rows = []
    # أزرار روابط مباشرة لكل مادة (فتح سريع)
    for name, url in page_items:
        rows.append([InlineKeyboardButton(name, url=url)])

    # أزرار التنقل
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("« السابق", callback_data=f"PAGE|{cat_idx}|{sec_code}|{page-1}"))
    nav.append(InlineKeyboardButton("رجوع", callback_data=f"SEC|{cat_idx}|{sec_code}"))  # يعيد للقائمة نفسها (تحديث)
    if end < total:
        nav.append(InlineKeyboardButton("التالي »", callback_data=f"PAGE|{cat_idx}|{sec_code}|{page+1}"))
    rows.append(nav)

    # زر الرجوع لقائمة الأقسام
    rows.append([InlineKeyboardButton("◀️ رجوع للأقسام", callback_data=f"CAT|{cat_idx}")])
    rows.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="BACK|MAIN")])

    return InlineKeyboardMarkup(rows)

WELCOME_TEXT = (
    "👋 أهلاً وسهلاً بك في Power Team Bot 🚀\n"
    "بوت خاص لمساعدة طلاب الهندسة في الوصول إلى المواد والملفات بكل سهولة.\n\n"
    "📚 اختر من القوائم التالية للوصول إلى:\n"
    "• المواد المشتركة\n"
    "• هندسة الكهرباء\n"
    "• هندسة الحاسوب\n"
    "• هندسة أمن الشبكات و المعلومات\n"
    "• هندسة الاتصالات\n\n"
    "✨ نتمنى لك تجربة ممتعة ومفيدة مع البوت!"
)

# ---------------------------
# Handlers
# ---------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu_kb())
    elif update.callback_query:
        await update.callback_query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_kb())

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """دعم سريع: إذا كتب المستخدم اسم قسم رئيسي نصاً، افتح له القائمة."""
    text = (update.message.text or "").strip()
    if text in CATEGORIES:
        idx = CATEGORIES.index(text)
        await update.message.reply_text(f"اختر القسم داخل: {text}", reply_markup=section_menu_kb(idx))
    else:
        # تلميح بسيط
        await update.message.reply_text("اكتب /start ثم اختر من الأزرار 👇")

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data or ""
    try:
        if data.startswith("CAT|"):
            _, cat_idx_str = data.split("|", 1)
            cat_idx = int(cat_idx_str)
            cat_name = CATEGORIES[cat_idx]
            await query.edit_message_text(f"📂 {cat_name} — اختر:", reply_markup=section_menu_kb(cat_idx))

        elif data.startswith("SEC|"):
            _, cat_idx_str, sec_code = data.split("|", 2)
            cat_idx = int(cat_idx_str)
            cat = CATEGORIES[cat_idx]
            sec = SECTIONS_REVERSE[sec_code]
            title = f"📁 {cat} • {sec}\nاختر ما تريد فتحه مباشرةً:"
            await query.edit_message_text(title, reply_markup=items_menu_kb(cat_idx, sec_code, page=1))

        elif data.startswith("PAGE|"):
            _, cat_idx_str, sec_code, page_str = data.split("|", 3)
            cat_idx = int(cat_idx_str)
            page = int(page_str)
            cat = CATEGORIES[cat_idx]
            sec = SECTIONS_REVERSE[sec_code]
            title = f"📁 {cat} • {sec}\nاختر ما تريد فتحه مباشرةً:"
            await query.edit_message_text(title, reply_markup=items_menu_kb(cat_idx, sec_code, page=page))

        elif data == "BACK|MAIN":
            await start(update, context)

        else:
            await query.answer("أمر غير معروف", show_alert=False)

    except Exception as e:
        # في حال أي خطأ غير متوقع، لا نعلّق الرسالة — نعرض القائمة الرئيسية بسرعة
        await query.answer("حدث خطأ بسيط، تمت إعادتك للقائمة الرئيسية.", show_alert=False)
        await start(update, context)

# ---------------------------
# تطبيق وتشغيل
# ---------------------------

def build_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    return app

if __name__ == "__main__":
    application = build_app()
    print("Power Team Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
