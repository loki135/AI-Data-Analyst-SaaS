# DataLens AI — AI-Powered CSV Data Analyst

Upload a CSV → get instant charts, stats, AI summaries, and natural language Q&A powered by Google Gemini.

## Tech Stack
- **Frontend**: React + Vite + Tailwind CSS + Recharts + react-dropzone
- **Backend**: Node.js + Express + MongoDB + Mongoose + Multer
- **AI**: Google Gemini 1.5 Flash (free tier, plain fetch — no SDK)
- **Deploy**: Render (backend) + Netlify (frontend) + MongoDB Atlas (free M0)

---

## Local Setup

### 1. Clone & install

```bash
# Server
cd server
npm install

# Client
cd ../client
npm install
```

### 2. Configure environment

Copy `server/.env.example` to `server/.env` and fill in:

```
PORT=5000
MONGO_URI=your_mongodb_atlas_connection_string
JWT_SECRET=any_random_secret_string
GEMINI_API_KEY=your_gemini_api_key
```

**Get free keys:**
- Gemini API: https://aistudio.google.com → "Get API Key"
- MongoDB Atlas: https://mongodb.com/atlas → free M0 cluster (no card)

### 3. Run locally

```bash
# Terminal 1: start backend
cd server
npm run dev

# Terminal 2: start frontend
cd client
npm run dev
```

Open http://localhost:5173

---

## Deploy to Production

### Backend → Render (free)
1. Push to GitHub
2. New Web Service on Render → connect repo
3. Root directory: `server`
4. Build command: `npm install`
5. Start command: `node index.js`
6. Add environment variables (MONGO_URI, JWT_SECRET, GEMINI_API_KEY, CLIENT_URL)

### Frontend → Netlify (free)
1. `cd client && npm run build`
2. Drag the `dist/` folder to https://netlify.com/drop
3. Set environment variable or update vite.config.js proxy target to your Render URL

---

## API Routes

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | /api/auth/register | No | Register → JWT |
| POST | /api/auth/login | No | Login → JWT |
| POST | /api/upload | Yes | Upload CSV, get analysis |
| GET | /api/analysis | Yes | List user's datasets |
| GET | /api/analysis/:id | Yes | Full dataset with rows |
| DELETE | /api/analysis/:id | Yes | Delete dataset |
| POST | /api/ai/ask | Yes | Ask question about dataset |
| POST | /api/ai/suggest-chart | Yes | AI chart suggestion |

---

## Features
- Drag-and-drop CSV upload (max 10MB)
- Auto column type detection (numeric / categorical / date)
- Per-column stats: min, max, mean, null count, unique count
- AI-generated plain-English dataset summary
- Bar, line, pie charts with axis selection + AI suggestion
- Paginated data table (10 rows/page)
- Chat Q&A: ask anything about your data
- Full upload history with delete
- JWT auth (7-day tokens)
