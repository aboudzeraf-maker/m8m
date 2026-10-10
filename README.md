# m8m

m8m هو منصة مجانية ومفتوحة المصدر لأتمتة الأعمال والـ workflows، مستوحاة من فكرة n8n، لكنها مصممة للتشغيل الذاتي والتوسع المرن.

**مدعومة بـ Vercel AI SDK** للتعامل مع نماذج AI المختلفة (Claude, GPT, Gemini, إلخ).

## الهدف

- بناء منصة أتمتة تدعم إنشاء sier عمل (Workflows)
- دعم عقد Node/Step لكل عملية
- إنشاء واجهة إدارة تفاعلية
- التنفيذ عبر API
- تشغيلها محلياً أو عبر Docker
- توفير قاعدة أساسية جاهزة للتطوير
- **التكامل مع Vercel AI SDK لقدرات AI متقدمة**

## المميزات الأساسية

- نظام مستخدمين: تسجيل/تسجيل دخول
- إدارة workflows
- أنواع عقدة ووظائف جاهزة:
  - `set_variable`: تعيين متغير
  - `condition`: شرط منطقي
  - `http_request`: طلب HTTP
  - `webhook`: استقبال webhook
  - `ai_task`: **مهمة AI (جديد - بـ Vercel AI)**
  - `text_extraction`: استخراج نصوص
- محرك تنفيذ بسيط للـ workflows
- لوحة تحكم تعرض الإحصائيات
- واجهة Frontend Next.js
- Backend FastAPI
- قاعدة بيانات SQLite محلية
- إعداد Docker Compose جاهز
- **تكامل Vercel AI SDK في Backend و Frontend**

## البنية

```
m8m/
├── backend/              # خادم FastAPI + Vercel AI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── security.py
│   │   ├── services/
│   │   │   ├── engine.py
│   │   │   └── ai_service.py        # (جديد)
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── workflows.py
│   │       └── ai.py               # (جديد)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # تطبيق Next.js + Vercel AI
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   ├── globals.css
│   │   └── workflows/              # (جديد)
│   ├── lib/
│   │   ├── api.ts
│   │   └── ai-client.ts           # (جديد)
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## التشغيل السريع

### 1) نسخ المشروع

```bash
git clone https://github.com/aboudzeraf-maker/m8m.git
cd m8m
```

### 2) إعداد المتغيرات

```bash
cp .env.example .env
```

**تعديل `.env` وإضافة مفاتيح API الخاصة بك:**

```env
# Vercel AI - اختر أحد الخيارات
OPENAI_API_KEY=sk-...
# أو
ANTHROPIC_API_KEY=sk-ant-...
# أو
GOOGLE_API_KEY=...
```

### 3) التشغيل عبر Docker

```bash
docker compose up --build
```

هذا سيشغل:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

### 4) التشغيل يدويًا

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # أو .venv\Scripts\activate على Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## سجل API

### التوثيق

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### أمثلة سريعة

#### تسجيل مستخدم

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"123456"}'
```

#### تسجيل الدخول

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"123456"}'
```

#### إنشاء workflow

```bash
curl -X POST http://localhost:8000/api/workflows \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"AI Content Generator",
    "description":"Generate content with AI",
    "nodes":[
      {
        "id":"n1",
        "type":"set_variable",
        "name":"Set Topic",
        "position":{"x":100,"y":100},
        "config":{"key":"topic","value":"Technology trends 2024"}
      },
      {
        "id":"n2",
        "type":"ai_task",
        "name":"Generate Blog Post",
        "position":{"x":300,"y":100},
        "config":{
          "prompt":"Write a blog post about {{topic}}",
          "model":"gpt-4",
          "temperature":0.7
        }
      }
    ],
    "trigger":{"type":"manual"}
  }'
```

#### تنفيذ مهمة AI

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message":"اكتب وصفاً قصيراً لمنصة m8m",
    "model":"gpt-4"
  }'
```

## الصورة المستقبلية

المشروع الحالي هو نسخة MVP عملية وموجهة للتطوير، مع التركيز على:

- نظام أساسي جيد للـ workflows
- مصطلحات وAPI واضحة
- واجهة قابلة للاستخدام
- **تكامل كامل مع Vercel AI SDK**
- قاعدة قوية يمكن بناء ميزات إضافية عليها مثل:
  - Webhooks و Scheduling
  - SMTP / Email Nodes
  - Database Nodes
  - Slack / Telegram / Discord
  - OAuth Providers
  - Queues and Workers
  - Self-hosting Dashboard
  - RBAC and Team Accounts
  - **أدوات AI متقدمة (Vision, Audio, Document Processing)**

## ملاحظات

هذا المشروع يهدف إلى أن يكون نقطة انطلاق مجانية وقابلة للتوسع، وليس نسخة كاملة من n8n. لكنه يقدم هيكلاً عملياً يمكن تطويره إلى سوق خاص.

## الترخيص

MIT
