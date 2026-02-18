# 📖 Bot Commands Reference / مرجع أوامر البوت

[中文](README.md) | [English](README_EN.md) | [العربية](README_AR.md)

---

## 👤 User Commands / أوامر المستخدم

These commands are available to all registered users.
هذه الأوامر متاحة لجميع المستخدمين المسجلين.

| Command | Description | الوصف |
|---------|-------------|-------|
| `/start` | Register and get 1 free point | التسجيل والحصول على 1 نقطة مجانية |
| `/about` | View bot features and info | عرض ميزات ومعلومات البوت |
| `/help` | Show all available commands | عرض جميع الأوامر المتاحة |
| `/balance` | Check your current points | التحقق من رصيد نقاطك الحالي |
| `/qd` | Daily check-in (+1 point) | تسجيل الدخول اليومي (+1 نقطة) |
| `/invite` | Generate invite link (+2 pts/person) | إنشاء رابط دعوة (+2 نقطة/شخص) |
| `/use <code>` | Redeem a points code | استرداد كود نقاط |
| `/status` | View your verification history | عرض سجل طلبات التحقق |

---

## 🔐 Verification Commands / أوامر التحقق

Each verification costs **1 point**. Points are refunded if verification fails.
كل تحقق يكلف **1 نقطة**. تُسترد النقاط إذا فشل التحقق.

| Command | Service | Type | الخدمة |
|---------|---------|------|--------|
| `/verify <link>` | Gemini One Pro | Teacher | خصم Google AI Studio التعليمي |
| `/verify2 <link>` | ChatGPT Teacher K12 | Teacher | خصم OpenAI ChatGPT التعليمي |
| `/verify3 <link>` | Spotify Student | Student | خصم Spotify للطلاب |
| `/verify4 <link>` | Bolt.new Teacher | Teacher | خصم Bolt.new التعليمي |
| `/verify5 <link>` | YouTube Premium Student | Student | خصم YouTube Premium للطلاب |
| `/getV4Code <id>` | Bolt.new code query | — | استعلام كود Bolt.new |
| `/check <id>` | Check any verification result | — | استعلام نتيجة أي تحقق |

> **Note:** `/getV4Code` still works as an alias for `/check`.
> `/getV4Code` لا يزال يعمل كاسم بديل لـ `/check`.

### How to use verification / كيفية استخدام التحقق

1. **Get the verification link / احصل على رابط التحقق**
   - Visit the service's verification page / قم بزيارة صفحة تحقق الخدمة
   - Start the verification process / ابدأ عملية التحقق
   - Copy the full URL from the browser / انسخ الرابط الكامل من المتصفح

2. **Send the command / أرسل الأمر**
   ```
   /verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy
   ```

3. **Wait for processing / انتظر المعالجة**
   - The bot generates identity info automatically / البوت ينشئ المعلومات تلقائياً
   - Generates student/teacher ID image / ينشئ صورة بطاقة الطالب/المعلم
   - Submits to SheerID / يقدم إلى SheerID

4. **Get results / احصل على النتائج**
   - Review usually completes in minutes / المراجعة تكتمل عادةً خلال دقائق
   - On success, a redirect link is returned / عند النجاح، يتم إرجاع رابط توجيه

---

## 💰 Earning Points / كسب النقاط

| Method | Points | الطريقة | النقاط |
|--------|--------|---------|--------|
| Registration | +1 | التسجيل | +1 |
| Daily check-in `/qd` | +1 | تسجيل يومي | +1 |
| Invite friend `/invite` | +2 | دعوة صديق | +2 |
| Redeem code `/use` | Varies | استرداد كود | متنوع |

---

## 🔧 Admin Commands / أوامر المسؤول

> ⚠️ These commands are only available to the admin (configured via `ADMIN_USER_ID` in `.env`).
> هذه الأوامر متاحة فقط للمسؤول (يُحدد عبر `ADMIN_USER_ID` في `.env`).

### Points Management / إدارة النقاط

| Command | Description | الوصف |
|---------|-------------|-------|
| `/addbalance <user_id> <points>` | Add points to a user | إضافة نقاط لمستخدم |

**Examples / أمثلة:**
```
/addbalance 123456789 10      → Add 10 points to user / إضافة 10 نقاط
/addbalance 123456789 9999    → Add 9999 points (e.g. to yourself) / إضافة 9999 نقطة
```

### User Management / إدارة المستخدمين

| Command | Description | الوصف |
|---------|-------------|-------|
| `/block <user_id>` | Block a user | حظر مستخدم |
| `/white <user_id>` | Unblock a user | إلغاء حظر مستخدم |
| `/blacklist` | View blocked users list | عرض قائمة المحظورين |

**Examples / أمثلة:**
```
/block 123456789              → Block user / حظر المستخدم
/white 123456789              → Unblock user / إلغاء حظر المستخدم
```

### Redemption Codes / أكواد الاسترداد

| Command | Description | الوصف |
|---------|-------------|-------|
| `/genkey <code> <pts> [uses] [days]` | Create redemption code | إنشاء كود استرداد |
| `/listkeys` | View all codes | عرض جميع الأكواد |

**Parameters / المعاملات:**
- `code` — Code name / اسم الكود
- `pts` — Points value / قيمة النقاط
- `uses` — (Optional) Max uses, default: 1 / الحد الأقصى للاستخدام
- `days` — (Optional) Expiry in days, default: never / الصلاحية بالأيام

**Examples / أمثلة:**
```
/genkey welcome 5             → 5 pts, single use, never expires
                                5 نقاط، استخدام واحد، لا ينتهي
/genkey vip50 50 10           → 50 pts, 10 uses, never expires
                                50 نقطة، 10 استخدامات، لا ينتهي
/genkey promo 20 100 30       → 20 pts, 100 uses, expires in 30 days
                                20 نقطة، 100 استخدام، ينتهي خلال 30 يوم
```

### Broadcasting / الإرسال الجماعي

| Command | Description | الوصف |
|---------|-------------|-------|
| `/broadcast <text>` | Send message to all users | إرسال رسالة لجميع المستخدمين |

You can also reply to a message and send `/broadcast` to forward it to all users.
يمكنك أيضاً الرد على رسالة وإرسال `/broadcast` لإعادة توجيهها لجميع المستخدمين.

---

## ⚙️ Admin Quick Setup / إعداد المسؤول السريع

1. **Find your Telegram User ID / اعثر على معرف تيليجرام الخاص بك:**
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - أرسل رسالة إلى [@userinfobot](https://t.me/userinfobot)

2. **Set it in `.env` / حدده في `.env`:**
   ```env
   ADMIN_USER_ID=123456789
   ```

3. **Give yourself points / أعطِ نفسك نقاط:**
   ```
   /addbalance 123456789 9999
   ```

---

<p align="center">
  <strong>⭐ If this project is helpful, give it a Star!</strong><br>
  <strong>⭐ إذا كان المشروع مفيداً، امنحه نجمة!</strong>
</p>
