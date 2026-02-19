# 🎙️ صوت البراند (Brand Voice) - Social Media Agent

## 📋 نظرة عامة

| البند | التفاصيل |
|-------|----------|
| **البراند** | LangChain Community |
| **النمط** | تقني + مجتمعي + تعليمي |
| **اللغة** | إنجليزية (أمريكية) |
| **الجمهور** | مطوري AI/LLM |

---

## 🎯 خصائص صوت البراند

### 1️⃣ النبرة (Tone)

| الخاصية | الوصف | مثال |
|---------|-------|------|
| **ودية** | ✅ "Made by the LangChain Community" | مجتمعي |
| **متحمسة** | ✅ "🚀RepoGPT: AI-Powered..." | إيموجي |
| **تعليمية** | ✅ "This is one of the most comprehensive examples..." | تفصيلي |
| **محفزة** | ✅ "Check out this video..." | دعوة للعمل |

### 2️⃣ الهيكل (Structure)

```
[إيموجي + العنوان] ← Hook (5 كلمات max)
↓
[Made by the LangChain Community] ← التوثيق
↓
[الوصف] ← المحتوى (3 جمل max)
↓
[المميزات/النقاط] ← تفاصيل (اختياري)
↓
[الرابط] ← Call to Action
```

### 3️⃣ القواعد (Rules)

| القاعدة | التفاصيل |
|---------|----------|
| **الطول** | قصير ومختصر |
| **الإيموجي** | في العنوان + CTA (اختياري) |
| **الهاشتاج** | ❌ ممنوع |
| **الزمن** | present tense ("just launched") |
| **التقنية** | متوسط - ليس بسيط ولا معقد |
| **الشخصية** | إنسانية - "posting for other humans" |

---

## 📝 أمثلة من الكود

### مثال 1: إعلان منتج
```
🎙️🤖 Podcastfy.ai

Made by the LangChain Community

An Open Source API alternative to NotebookLM's podcast product

Transforming Multimodal Content into Captivating Multilingual Audio Conversations with GenAI

https://podcastfy.ai
```

**التحليل:**
- ✅ Hook: إيموجي + اسم المنتج
- ✅ توثيق: "Made by..."
- ✅ وصف: ما يفعله
- ✅ CTA: الرابط

### مثال 2: شرح تقني
```
🧱Complex SQL Joins with LangGraph and Waii

Made by the LangChain Community

Waii is a toolkit that provides text-to-SQL and text-to-chart capabilities

This post focuses on Waii's approach to handling complex joins in databases, doing so within LangGraph

https://waii.com
```

**التحليل:**
- ✅ Hook: إيموجي + موضوع تقني
- ✅ توضيح: ما هو Waii
- ✅ التركيز: الفائدة

### مثال 3: فيديو تعليمي
```
🌐 Build agents that can interact with any website

Made by the LangChain Community

Check out this video by @DendriteSystems showing how to build an agent that can interact with websites just like a human would!

This video demonstrates a workflow that:
- Finds competitors on Product Hunt and Hacker News
- Drafts an email about new competitors
- Sends the email via Outlook

📺 Video: https://youtube.com/watch?v=...
🧠 Repo: https://github.com/...
```

**التحليل:**
- ✅ Hook: إيموجي + فائدة
- ✅ دعوة: "Check out..."
- ✅ نقاط: المميزات
- ✅ روابط متعددة

---

## 🎨 عناصر الصوت

### الكلمات المفتاحية
| النوع | الأمثلة |
|-------|---------|
| **تقنية** | AI, LLM, LangGraph, Agents |
| **إنجاز** | Comprehensive, Powerful, Open Source |
| **مجتمع** | Made by the LangChain Community |
| **إثارة** | 🚀, 🎉, 🤖, 🧠 |

### أنماط الجمل
| النمط | المثال |
|-------|--------|
| **إعلان** | "X just launched..." |
| **شرح** | "This is one of the most comprehensive examples..." |
| **دعوة** | "Check out this video..." |
| **توثيق** | "Made by the LangChain Community" |

---

## 🔄 للتخصيص (Customization)

### تغيير صوت البراند:

في الملف: `src/agents/generate-post/prompts/index.ts`

```typescript
export const POST_CONTENT_RULES = `
- Focus your post on what the content covers...
- Do not make the post over technical...
- Keep posts short, concise and engaging
- Limit the use of emojis...
- NEVER use hashtags...
- ALWAYS use present tense...
- You're acting as a human... Keep your tone casual and friendly.
`;
```

### تغيير سياق الأعمال:

```typescript
export const BUSINESS_CONTEXT = `
<business-context>
- AI applications...
- UI/UX for AI...
- New AI/LLM research...
- Agents...
</business-context>
`;
```

---

## 💡 ملخص

| العنصر | القيمة |
|--------|--------|
| **النمط** | تقني + مجتمعي + ودي |
| **الطول** | قصير (3-5 جمل) |
| **الهيكل** | Hook → Context → Body → CTA |
| **الإيموجي** | في البداية والنهاية |
| **الجمهور** | مطوري AI |
| **الهدف** | تعليم + إعلام + ترويج |

### **صوت البراند: "صديق خبير يشارك اكتشافاته بتشويق"** 🎯
