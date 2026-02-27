# BEA-LAB.io — Architektur-Dokumentation

> **⚠️ DEPRECATED — NICHT MEHR AKTUELL**
>
> Dieses Dokument beschreibt eine **geplante** Architektur (Next.js, Supabase, TypeScript)
> die **nie umgesetzt** wurde. Die tatsächliche Implementierung verwendet Vanilla JS + FastAPI.
>
> **SSOT:** `data/beatrix/architecture.yaml`
>
> Dieses Dokument wird nur als historische Referenz aufbewahrt.

> **Version:** 1.0 (Draft)
> **Datum:** 2026-01-26
> **Status:** ~~Review Pending~~ DEPRECATED (2026-02-14)
> **Domain:** www.bea-lab.io

---

## 1. Vision & Ziele

### Was ist BEA Lab?

**BEA Lab** (Behavioral Economics Application Laboratory) ist eine interaktive Web-Plattform, die das Evidence-Based Framework (EBF) für Mitarbeitende und später Kunden zugänglich macht.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   "Das EBF Framework — aber als interaktives Web-Erlebnis"              │
│                                                                         │
│   Statt: CLAUDE.md lesen + Claude Code CLI nutzen                       │
│   Neu:   bea-lab.io öffnen + geführte Workflows durchlaufen             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ziele

| Ziel | Beschreibung | Messung |
|------|--------------|---------|
| **Demokratisierung** | Jeder bei FehrAdvice kann EBF nutzen, nicht nur Power-User | Adoption Rate |
| **Standardisierung** | Einheitliche Qualität bei allen Analysen | Compliance Score |
| **Effizienz** | Schnellere Time-to-Insight | Durchschnittliche Session-Zeit |
| **Wissensspeicher** | Sessions werden gespeichert und wiederverwendbar | Knowledge Base Größe |

### Zielgruppen (Phasen)

| Phase | Zielgruppe | Zugang |
|-------|------------|--------|
| **Phase 1** | FehrAdvice Mitarbeitende | Login mit Firmen-Email |
| **Phase 2** | Ausgewählte Kunden | Einladungs-Link |
| **Phase 3** | Öffentlich | Freemium oder Subscription |

---

## 2. Tech-Stack

### Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FRONTEND                                                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Next.js 14 (App Router)     │ React-basiertes Full-Stack Framework     │
│  TypeScript                  │ Typsicherheit, bessere DX                │
│  Tailwind CSS                │ Utility-first CSS, schnelles Styling     │
│  shadcn/ui                   │ Accessible UI-Komponenten (Radix-based)  │
│  Framer Motion               │ Animationen für bessere UX               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  BACKEND                                                                │
├─────────────────────────────────────────────────────────────────────────┤
│  Next.js API Routes          │ Serverless Functions (kein separater BE) │
│  Anthropic SDK               │ Claude API Integration                   │
│  Vercel AI SDK               │ Streaming, Tool Use, Chat Helpers        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  DATENBANK & AUTH                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Supabase                    │ PostgreSQL + Auth + Realtime + Storage   │
│  NextAuth.js                 │ Auth-Abstraktion (optional: direkt Supa) │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  HOSTING & DEPLOYMENT                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Vercel                      │ Automatisches Deployment, Edge Network   │
│  GitHub                      │ Source Code, CI/CD via Vercel            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Warum diese Choices?

| Technologie | Begründung | Alternativen (verworfen) |
|-------------|------------|--------------------------|
| **Next.js** | Full-Stack in einem, Server Components, API Routes, Vercel-optimiert | Remix, SvelteKit, separate FE+BE |
| **Supabase** | PostgreSQL + Auth + Realtime in einem, generous Free Tier, Open Source | Firebase, PlanetScale, Auth0 |
| **Vercel** | Nahtlose Next.js Integration, Preview Deployments, Edge Functions | Netlify, Railway, AWS |
| **shadcn/ui** | Copy-paste Komponenten (kein Lock-in), Radix-based (accessible) | Material UI, Chakra, Ant Design |
| **Tailwind** | Schnelles Prototyping, keine CSS-Datei-Verwaltung | CSS Modules, Styled Components |

---

## 3. System-Architektur

### High-Level Architektur

```
                                    ┌─────────────────────┐
                                    │   www.bea-lab.io    │
                                    │   (Vercel Edge)     │
                                    └──────────┬──────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
         ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
         │  Next.js App     │      │  API Routes      │      │  Static Assets   │
         │  (React SSR)     │      │  (/api/*)        │      │  (CDN)           │
         └────────┬─────────┘      └────────┬─────────┘      └──────────────────┘
                  │                         │
                  │                         ├─────────────────────┐
                  │                         │                     │
                  ▼                         ▼                     ▼
         ┌──────────────────┐      ┌──────────────────┐  ┌──────────────────┐
         │  Supabase        │      │  Anthropic API   │  │  EBF Context     │
         │  (PostgreSQL)    │      │  (Claude)        │  │  (YAML/JSON)     │
         │  - Users         │      │                  │  │  - BCM2          │
         │  - Sessions      │      │                  │  │  - Theories      │
         │  - Messages      │      │                  │  │  - Cases         │
         └──────────────────┘      └──────────────────┘  └──────────────────┘
```

### Request Flow: Chat Message

```
┌─────────────────────────────────────────────────────────────────────────┐
│  USER SENDS MESSAGE                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. User tippt: "Wie hoch ist Loss Aversion in der Schweiz?"            │
│     │                                                                   │
│     ▼                                                                   │
│  2. Frontend sendet POST /api/chat                                      │
│     {                                                                   │
│       "message": "Wie hoch ist Loss Aversion...",                       │
│       "sessionId": "sess_abc123",                                       │
│       "mode": "STANDARD"                                                │
│     }                                                                   │
│     │                                                                   │
│     ▼                                                                   │
│  3. API Route:                                                          │
│     a) Auth prüfen (Supabase JWT)                                       │
│     b) Session laden (bisherige Messages)                               │
│     c) EBF Context laden (CLAUDE.md + BCM2)                             │
│     d) System Prompt bauen                                              │
│     │                                                                   │
│     ▼                                                                   │
│  4. Anthropic API Call (Streaming):                                     │
│     {                                                                   │
│       "model": "claude-opus-4-5-20251101",                              │
│       "system": "[EBF SYSTEM PROMPT]",                                  │
│       "messages": [history + new message]                               │
│     }                                                                   │
│     │                                                                   │
│     ▼                                                                   │
│  5. Stream Response zurück an Frontend                                  │
│     │                                                                   │
│     ▼                                                                   │
│  6. Frontend zeigt Antwort (live streaming)                             │
│     │                                                                   │
│     ▼                                                                   │
│  7. Nach Completion: Message in Supabase speichern                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Datenmodell

### Supabase Schema

```sql
-- Users (managed by Supabase Auth)
-- Automatisch erstellt, erweitert durch:

CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT NOT NULL,
  full_name TEXT,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'viewer')),
  organization TEXT DEFAULT 'FehrAdvice',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sessions (Konversationen)
CREATE TABLE public.sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) NOT NULL,
  title TEXT,                                    -- Auto-generiert aus erster Frage
  mode TEXT DEFAULT 'STANDARD' CHECK (mode IN ('SCHNELL', 'STANDARD', 'TIEF')),
  workflow TEXT,                                 -- 'chat', 'model-builder', 'intervention', etc.
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
  metadata JSONB DEFAULT '{}',                   -- Workflow-spezifische Daten
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages
CREATE TABLE public.messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES public.sessions(id) ON DELETE CASCADE NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',                   -- Token count, model, etc.
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON public.sessions(user_id);
CREATE INDEX idx_sessions_created_at ON public.sessions(created_at DESC);
CREATE INDEX idx_messages_session_id ON public.messages(session_id);
CREATE INDEX idx_messages_created_at ON public.messages(created_at);

-- Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Policies: Users can only see their own data
CREATE POLICY "Users can view own profile" ON public.profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can view own sessions" ON public.sessions
  FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view messages in own sessions" ON public.messages
  FOR ALL USING (
    session_id IN (
      SELECT id FROM public.sessions WHERE user_id = auth.uid()
    )
  );
```

### Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│  profiles        │       │  sessions        │       │  messages        │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │──┐    │ id (PK)          │──┐    │ id (PK)          │
│ email            │  │    │ user_id (FK)     │◄─┘    │ session_id (FK)  │◄─┘
│ full_name        │  │    │ title            │       │ role             │
│ role             │  └───►│ mode             │       │ content          │
│ organization     │       │ workflow         │       │ metadata         │
│ created_at       │       │ status           │       │ created_at       │
│ updated_at       │       │ metadata         │       └──────────────────┘
└──────────────────┘       │ created_at       │
                           │ updated_at       │
                           └──────────────────┘
```

---

## 5. API Design

### Endpoints

| Method | Endpoint | Beschreibung | Auth |
|--------|----------|--------------|------|
| `POST` | `/api/auth/[...nextauth]` | Auth Callbacks | - |
| `GET` | `/api/sessions` | Liste aller Sessions des Users | ✓ |
| `POST` | `/api/sessions` | Neue Session erstellen | ✓ |
| `GET` | `/api/sessions/[id]` | Session Details + Messages | ✓ |
| `DELETE` | `/api/sessions/[id]` | Session löschen | ✓ |
| `POST` | `/api/chat` | Chat Message senden (Streaming) | ✓ |
| `GET` | `/api/context/[type]` | EBF Context laden (BCM2, etc.) | ✓ |

### Chat Endpoint (Kern-API)

```typescript
// POST /api/chat

// Request
interface ChatRequest {
  sessionId: string;
  message: string;
  mode?: 'SCHNELL' | 'STANDARD' | 'TIEF';
  workflow?: 'chat' | 'model-builder' | 'intervention' | 'context-analyzer';
}

// Response (Streaming)
// Server-Sent Events (SSE) Format:
// data: {"type": "text", "content": "Die Loss Aversion..."}
// data: {"type": "text", "content": " in der Schweiz..."}
// data: {"type": "done", "messageId": "msg_xyz"}
```

### Example: Chat API Route

```typescript
// app/api/chat/route.ts

import { anthropic } from '@/lib/claude';
import { createClient } from '@/lib/supabase/server';
import { getEBFSystemPrompt } from '@/lib/ebf-context';
import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const supabase = createClient();

  // 1. Auth Check
  const { data: { user }, error: authError } = await supabase.auth.getUser();
  if (authError || !user) {
    return new Response('Unauthorized', { status: 401 });
  }

  // 2. Parse Request
  const { sessionId, message, mode = 'STANDARD' } = await req.json();

  // 3. Load Session History
  const { data: messages } = await supabase
    .from('messages')
    .select('role, content')
    .eq('session_id', sessionId)
    .order('created_at', { ascending: true });

  // 4. Build System Prompt with EBF Context
  const systemPrompt = await getEBFSystemPrompt(mode);

  // 5. Call Claude (Streaming)
  const stream = await anthropic.messages.stream({
    model: 'claude-opus-4-5-20251101',
    max_tokens: 4096,
    system: systemPrompt,
    messages: [
      ...(messages || []).map(m => ({ role: m.role, content: m.content })),
      { role: 'user', content: message }
    ]
  });

  // 6. Return Streaming Response
  return new Response(stream.toReadableStream(), {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

---

## 6. EBF Integration

### Wie bekommt Claude den EBF-Kontext?

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBF CONTEXT INJECTION                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SYSTEM PROMPT besteht aus:                                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. CLAUDE.md (Core Instructions)                                │   │
│  │     - 10C Framework                                              │   │
│  │     - EBF Workflow (Schritte 0-9)                                │   │
│  │     - Modus-Definitionen (SCHNELL/STANDARD/TIEF)                 │   │
│  │     - Kontext-First Regeln                                       │   │
│  │     - Exclusion Principles                                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              +                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  2. BCM2 Context (dynamisch geladen je nach Frage)               │   │
│  │     - CH/AT/DE Faktoren (404 pro Land)                           │   │
│  │     - Relevante Dimensionen                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              +                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  3. Theory Catalog (bei Modell-Fragen)                           │   │
│  │     - 134 Theorien mit EBF-Restriktionen                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              +                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  4. Workflow-spezifischer Kontext                                │   │
│  │     - Model Builder: /design-model Skill                         │   │
│  │     - Intervention: /design-intervention Skill                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Context Loading Strategy

```typescript
// lib/ebf-context.ts

import claudeMd from '@/data/CLAUDE.md';
import theoryCatalog from '@/data/theory-catalog.yaml';
import bcm2Swiss from '@/data/context/ch/BCM2_04_KON_socio_cultural.yaml';

export async function getEBFSystemPrompt(
  mode: 'SCHNELL' | 'STANDARD' | 'TIEF',
  workflow?: string
): Promise<string> {

  // Base: CLAUDE.md (gekürzt für Token-Effizienz)
  const baseContext = getCondensedClaudeMd(mode);

  // Mode-spezifische Instruktionen
  const modeInstructions = getModeInstructions(mode);

  // Workflow-spezifischer Kontext
  const workflowContext = workflow
    ? getWorkflowContext(workflow)
    : '';

  return `
${baseContext}

## Aktueller Modus: ${mode}
${modeInstructions}

${workflowContext}

## Session-Kontext
- Plattform: BEA Lab (bea-lab.io)
- User: FehrAdvice Mitarbeiter
- Sprache: Deutsch bevorzugt
`;
}

function getCondensedClaudeMd(mode: string): string {
  // SCHNELL: Nur essenzielle Regeln (~2000 Tokens)
  // STANDARD: Vollständige Regeln (~8000 Tokens)
  // TIEF: Alles + erweiterte Datenbanken (~15000 Tokens)

  if (mode === 'SCHNELL') {
    return `
# EBF Quick Reference

## 10C CORE Fragen
WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE, HIERARCHY, EIT

## Workflow
1. Kontext → 2. Modell → 3. Parameter → 4. Antwort

## Kontext-First Regel
IMMER zuerst Kontext analysieren: MACRO → MESO → MICRO
`;
  }

  // STANDARD und TIEF: Vollständiger CLAUDE.md
  return claudeMd;
}
```

### Token Budget Management

| Modus | System Prompt | User Context | Response | Total Budget |
|-------|---------------|--------------|----------|--------------|
| SCHNELL | ~2,000 | ~1,000 | ~2,000 | ~5,000 |
| STANDARD | ~8,000 | ~4,000 | ~4,000 | ~16,000 |
| TIEF | ~15,000 | ~10,000 | ~8,000 | ~33,000 |

---

## 7. UI/UX Konzept

### Screens

#### 1. Landing Page (`/`)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  🧠 BEA LAB                                        [Login]      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│                                                                         │
│              ╔═══════════════════════════════════════╗                  │
│              ║                                       ║                  │
│              ║   Behavioral Economics                ║                  │
│              ║   Application Laboratory              ║                  │
│              ║                                       ║                  │
│              ║   Das EBF Framework —                 ║                  │
│              ║   interaktiv und intelligent.         ║                  │
│              ║                                       ║                  │
│              ║        [ Jetzt starten → ]            ║                  │
│              ║                                       ║                  │
│              ╚═══════════════════════════════════════╝                  │
│                                                                         │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  🎯 Analyze     │  │  🔬 Model       │  │  💡 Design      │         │
│  │  Context        │  │  Builder        │  │  Interventions  │         │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2. Dashboard (`/dashboard`)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  🧠 BEA LAB          [Dashboard]  [Settings]  [Maria S. ▾]     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Willkommen zurück, Maria!                                      │   │
│  │                                                                  │   │
│  │  [ + Neue Analyse starten ]                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  📁 Letzte Sessions                                              │   │
│  │  ─────────────────────────────────────────────────────────────  │   │
│  │  │ Loss Aversion Schweiz Energie      │ STANDARD │ vor 2h    │  │   │
│  │  │ Intervention Design BFE Heizung    │ TIEF     │ gestern   │  │   │
│  │  │ Kontext-Analyse PORR Sicherheit    │ SCHNELL  │ 3. Jan    │  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌───────────────────────┐  ┌───────────────────────┐                  │
│  │  📊 Statistiken       │  │  🎯 Quick Actions     │                  │
│  │  ──────────────────   │  │  ──────────────────   │                  │
│  │  Sessions: 24         │  │  → Model Builder      │                  │
│  │  Diesen Monat: 8      │  │  → Context Analyzer   │                  │
│  │  Ø Dauer: 18 min      │  │  → Case Explorer      │                  │
│  └───────────────────────┘  └───────────────────────┘                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3. Chat Interface (`/chat/[sessionId]`)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  🧠 BEA LAB    │ Session: Loss Aversion CH    │ STANDARD ▾     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ 👤 User                                                  │    │   │
│  │  │ Wie hoch ist Loss Aversion in der Schweiz für           │    │   │
│  │  │ Energie-Entscheidungen?                                  │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ 🤖 BEA Lab                                               │    │   │
│  │  │                                                          │    │   │
│  │  │ ┌─────────────────────────────────────────────────────┐ │    │   │
│  │  │ │ 🔍 KONTEXT                                          │ │    │   │
│  │  │ │ MACRO: Schweiz (λ_CH = 2.1)                         │ │    │   │
│  │  │ │ MESO: Energie-Sektor (λ × 1.2)                      │ │    │   │
│  │  │ │ MICRO: Heizungsersatz (High Stakes)                 │ │    │   │
│  │  │ └─────────────────────────────────────────────────────┘ │    │   │
│  │  │                                                          │    │   │
│  │  │ Basierend auf BCM2 und der Literatur...                 │    │   │
│  │  │ λ_final = 2.1 × 1.2 × 1.3 = **3.28**                    │    │   │
│  │  │                                                          │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  [ Nachricht eingeben...                              ] [Send]  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 4. Mode Selector (Modal)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│         ╔═══════════════════════════════════════════════════╗           │
│         ║  Welcher Modus?                                   ║           │
│         ║                                                   ║           │
│         ║  ┌─────────────────────────────────────────────┐  ║           │
│         ║  │  ⚡ SCHNELL                                  │  ║           │
│         ║  │  10 min, keine Rückfragen                   │  ║           │
│         ║  └─────────────────────────────────────────────┘  ║           │
│         ║                                                   ║           │
│         ║  ┌─────────────────────────────────────────────┐  ║           │
│         ║  │  🎯 STANDARD                    [EMPFOHLEN] │  ║           │
│         ║  │  45 min, Feedback pro Schritt               │  ║           │
│         ║  └─────────────────────────────────────────────┘  ║           │
│         ║                                                   ║           │
│         ║  ┌─────────────────────────────────────────────┐  ║           │
│         ║  │  🔬 TIEF                                     │  ║           │
│         ║  │  2+ Std, Monte Carlo, Alternativen          │  ║           │
│         ║  └─────────────────────────────────────────────┘  ║           │
│         ║                                                   ║           │
│         ╚═══════════════════════════════════════════════════╝           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Design System

| Element | Spezifikation |
|---------|---------------|
| **Primärfarbe** | `#2563eb` (Blau) — Vertrauen, Professionalität |
| **Sekundärfarbe** | `#10b981` (Grün) — Erfolg, Wachstum |
| **Akzent** | `#f59e0b` (Amber) — Aufmerksamkeit |
| **Hintergrund** | `#fafafa` (Light) / `#0a0a0a` (Dark) |
| **Font** | Inter (UI), JetBrains Mono (Code) |
| **Border Radius** | `0.5rem` (8px) |
| **Shadows** | Subtle, consistent elevation system |

---

## 8. Security & Auth

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AUTHENTICATION FLOW (Supabase Auth)                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Phase 1: Email/Password (MVP)                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  1. User gibt Email + Password ein                                      │
│  2. Supabase Auth verifiziert                                           │
│  3. JWT Token wird gesetzt (httpOnly Cookie)                            │
│  4. Alle API Requests nutzen diesen Token                               │
│                                                                         │
│  Phase 2: SSO (Optional, später)                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  - Microsoft Azure AD (FehrAdvice Office 365)                           │
│  - Google Workspace                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Security Measures

| Bereich | Maßnahme |
|---------|----------|
| **Auth** | Supabase Auth mit Row Level Security (RLS) |
| **API** | Rate Limiting (10 req/min für Chat) |
| **Secrets** | Environment Variables (Vercel) |
| **Data** | Verschlüsselung at rest (Supabase) |
| **HTTPS** | Automatisch via Vercel |
| **CORS** | Nur bea-lab.io erlaubt |

### Environment Variables

```bash
# .env.local (NICHT committen!)

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...  # Nur Server-side!

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# App
NEXT_PUBLIC_APP_URL=https://bea-lab.io
```

---

## 9. Deployment

### Vercel Setup

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DEPLOYMENT PIPELINE                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  GitHub Repository                                                      │
│  (FehrAdvice-Partners-AG/bea-lab)                                       │
│         │                                                               │
│         │ Push to main                                                  │
│         ▼                                                               │
│  ┌─────────────────────┐                                                │
│  │  Vercel Build       │                                                │
│  │  - npm install      │                                                │
│  │  - npm run build    │                                                │
│  │  - Type Check       │                                                │
│  └──────────┬──────────┘                                                │
│             │                                                           │
│             │ Success                                                   │
│             ▼                                                           │
│  ┌─────────────────────┐                                                │
│  │  Production         │  ──►  https://bea-lab.io                       │
│  └─────────────────────┘                                                │
│                                                                         │
│  Preview Deployments:                                                   │
│  - Jeder PR bekommt eigene URL                                          │
│  - https://bea-lab-git-feature-xxx.vercel.app                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Domain Setup

```
1. Vercel Dashboard → Project Settings → Domains
2. Add Domain: bea-lab.io
3. DNS bei Domain-Registrar:
   - A Record: 76.76.21.21
   - CNAME: cname.vercel-dns.com (für www)
4. SSL: Automatisch via Vercel
```

---

## 10. Phasen-Plan

### Phase 1: MVP (Wochen 1-3)

| Woche | Deliverables |
|-------|--------------|
| **W1** | Projekt Setup, Auth, Basis-UI |
| **W2** | Chat Interface, Claude Integration |
| **W3** | Session-Speicherung, Polish, Deploy |

**MVP Features:**
- [x] Landing Page
- [x] Login/Logout (Email/Password)
- [x] Dashboard (Session-Liste)
- [x] Chat Interface mit Modus-Wahl
- [x] Claude + EBF Context Integration
- [x] Session-Speicherung
- [x] Responsive Design

### Phase 2: Workflows (Wochen 4-6)

| Feature | Beschreibung |
|---------|--------------|
| Model Builder | Geführter 10C Wizard |
| Context Analyzer | MACRO→MESO→MICRO Flow |
| Report Export | Markdown, PDF Download |

### Phase 3: Advanced (Wochen 7-10)

| Feature | Beschreibung |
|---------|--------------|
| Intervention Designer | 20-Field Schema Wizard |
| Case Explorer | Registry Browser |
| Parameter Finder | BCM2 Suche |
| Team Features | Shared Sessions |

### Phase 4: Polish & Scale (Wochen 11-12)

| Feature | Beschreibung |
|---------|--------------|
| SSO | Microsoft AD Integration |
| Analytics | Usage Tracking |
| Admin Panel | User Management |
| Performance | Caching, Optimierung |

---

## 11. Kosten-Schätzung

### Fixkosten (Monthly)

| Service | Free Tier | Pro Tier | Notes |
|---------|-----------|----------|-------|
| **Vercel** | $0 | $20/user | Free reicht für Start |
| **Supabase** | $0 | $25 | Free: 500MB DB, 50K Auth |
| **Domain** | - | ~$15/Jahr | Bereits registriert |

### Variable Kosten (Claude API)

| Modus | Tokens/Session | Cost/Session | 100 Sessions/Monat |
|-------|----------------|--------------|-------------------|
| SCHNELL | ~5,000 | ~$0.08 | ~$8 |
| STANDARD | ~16,000 | ~$0.25 | ~$25 |
| TIEF | ~33,000 | ~$0.50 | ~$50 |

**Geschätzte Monatskosten (Start):**
- 10 User, 50 Sessions/Monat: **~$15-30**
- Free Tiers von Vercel + Supabase reichen

**Bei Skalierung:**
- 50 User, 500 Sessions/Monat: **~$150-300**
- Vercel Pro + Supabase Pro: +$45/Monat

---

## 12. Offene Fragen

| # | Frage | Optionen | Empfehlung |
|---|-------|----------|------------|
| 1 | Soll CLAUDE.md 1:1 übernommen werden oder gekürzt? | 1:1 / Gekürzt / Dynamisch | Dynamisch je nach Modus |
| 2 | Wie sollen Sessions benannt werden? | Auto / User-Input | Auto-generiert aus Frage |
| 3 | Soll es Dark Mode geben? | Ja / Nein / Later | Ja (von Anfang an) |
| 4 | Wie wird Rate Limiting kommuniziert? | Modal / Toast / Inline | Toast Notification |
| 5 | Welche Analytics? | None / Simple / Full | Simple (Vercel Analytics) |

---

## 13. Nächste Schritte

Nach Approval dieser Architektur:

1. **Repo erstellen:** `FehrAdvice-Partners-AG/bea-lab`
2. **Projekt initialisieren:** Next.js + TypeScript + Tailwind
3. **Supabase Setup:** Projekt erstellen, Schema deployen
4. **Vercel Connect:** Repo verbinden, Domain konfigurieren
5. **MVP bauen:** Landing → Auth → Dashboard → Chat

---

## Appendix A: Projekt-Struktur (Detail)

```
bea-lab/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── chat/[sessionId]/page.tsx
│   │   ├── settings/page.tsx
│   │   └── layout.tsx
│   ├── api/
│   │   ├── auth/
│   │   │   └── [...supabase]/route.ts
│   │   ├── chat/route.ts
│   │   ├── sessions/
│   │   │   ├── route.ts
│   │   │   └── [id]/route.ts
│   │   └── context/[type]/route.ts
│   ├── page.tsx                    # Landing
│   ├── layout.tsx                  # Root Layout
│   └── globals.css
├── components/
│   ├── ui/                         # shadcn components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── chat/
│   │   ├── ChatInterface.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── ContextBox.tsx
│   │   └── ModeSelector.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── shared/
│       ├── Logo.tsx
│       └── LoadingSpinner.tsx
├── lib/
│   ├── supabase/
│   │   ├── client.ts
│   │   ├── server.ts
│   │   └── middleware.ts
│   ├── claude.ts                   # Anthropic Client
│   ├── ebf-context.ts              # EBF System Prompt Builder
│   └── utils.ts
├── data/
│   ├── CLAUDE.md                   # Symlink oder Copy
│   ├── theory-catalog.yaml
│   ├── case-registry.yaml
│   └── context/
│       └── ch/
│           └── BCM2_*.yaml
├── types/
│   ├── database.ts                 # Supabase Types
│   └── ebf.ts                      # EBF Types
├── public/
│   ├── logo.svg
│   └── favicon.ico
├── .env.local                      # Secrets (git-ignored)
├── .env.example                    # Template
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── README.md
```

---

## Appendix UNMAPPED_B: EBF System Prompt Template

```typescript
// lib/ebf-context.ts

export const EBF_SYSTEM_PROMPT_TEMPLATE = `
# BEA Lab — EBF Assistant

Du bist der BEA Lab Assistant, basierend auf dem Evidence-Based Framework (EBF)
von FehrAdvice & Partners AG und Prof. Ernst Fehr.

## Deine Rolle
- Du führst User durch EBF-Analysen
- Du wendest IMMER den EBF Workflow an (Kontext → Modell → Parameter → Antwort)
- Du zeigst Kontext-Boxen bevor du antwortest
- Du verwendest die BCM2 Datenbank für Parameter

## Aktueller Modus: {MODE}
{MODE_INSTRUCTIONS}

## EBF Workflow (verkürzt)
1. KONTEXT: MACRO → MESO → MICRO → INDIVIDUAL → META
2. MODELL: 10C Fragen (WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE, HIERARCHY, EIT)
3. PARAMETER: LLMMC Prior + BCM2 Daten
4. ANTWORT: Mit Kontext-Box und Quellenangaben

## Kontext-Box Format
Zeige bei JEDER Antwort zuerst:

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│  🔍 KONTEXT                                                 │
├─────────────────────────────────────────────────────────────┤
│  THEMA: [...]                                               │
│  DIMENSIONEN: [Ψ_I, Ψ_S, Ψ_K, etc.]                        │
│  PARAMETER: [λ = X.XX, β = X.XX, etc.]                      │
│  QUELLEN: [BCM2, Papers, etc.]                              │
└─────────────────────────────────────────────────────────────┘
\`\`\`

## Verfügbare Daten
- BCM2: {BCM2_SUMMARY}
- Theorien: {THEORY_COUNT} Modelle
- Cases: {CASE_COUNT} dokumentierte Fälle

## Kommunikationsstil
- Professionell aber zugänglich
- Deutsch als Hauptsprache
- Strukturierte Antworten mit Boxen und Tabellen
- Immer evidenz-basiert mit Quellenangaben
`;
```

---

*Dokument erstellt: 2026-01-26*
*Nächster Schritt: Review → Repo erstellen*
