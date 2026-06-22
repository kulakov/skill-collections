---
name: agent-sdk-project
aliases:
  - l-d-agent-sdk
description: "Скаффолд нового проекта на Claude Agent SDK. Используй когда пользователь говорит 'создай агента', 'agent SDK проект', 'scaffold agent', 'новый AI-агент', 'agent-first architecture', 'MCP tools проект'. Паттерн: AI-агент как ядро, инструменты через MCP, WebSocket стриминг. НЕ используй для: запуска в Docker (docker-sandbox), локальной модели (l-d-local), создания субагента-рыцаря (l-k-subagent), MCP-сервера (mcp-builder)."
---

# Agent SDK Project Scaffold

Build a new project using the **agent-first architecture** pattern. The AI agent is the core — it decides what to do, which tools to call, and how to respond. Your code provides tools, not orchestration.

## Architecture Pattern: Agent-First

### Core Principle
**Code defines capabilities (tools). Agent decides behavior (orchestration).**

Instead of:
```
User -> Handler -> if/else logic -> Service A -> Service B -> Format -> Reply
```

You build:
```
User -> Agent (Claude SDK) -> [Agent chooses tools] -> Tools execute -> Agent responds
```

### Key Difference from Rule-Based
| Aspect | Rule-Based (traditional) | Agent-First |
|--------|------------------------|-------------|
| Orchestration | Your code (handlers, state machines) | Claude Agent |
| Adding features | New handler + routing + state | New tool function + whitelist |
| Natural language | Parsed into commands | Native input |
| State management | Manual (session maps, flags) | Agent context (multi-turn) |
| New scenarios | Code changes | System prompt changes |

---

## Stack

**Backend:** Python + FastAPI (recommended) or Node.js + Express
**Frontend:** React 19 + Vite + Tailwind + shadcn/ui
**AI:** Claude Agent SDK (subscription auth via Claude Code CLI)
**Realtime:** WebSocket for streaming agent responses
**Storage:** JSON files (prototype) or SQLite/PostgreSQL (production)
**Image gen:** Google Gemini (optional, for visual rewards)

---

## File Structure

```
project-name/
├── backend/
│   ├── agent.py          # Agent setup, system prompt, session management
│   ├── tools.py          # MCP tool definitions (declarative)
│   ├── server.py         # FastAPI + WebSocket endpoints
│   ├── store.py          # Data persistence (JSON/DB)
│   ├── settings_store.py # User-configurable settings
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/   # UI components
│   │   ├── hooks/        # useWebSocket, useAgent
│   │   └── lib/          # API client
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## Implementation Guide

### Step 1: Define Tools (tools.py)

Tools are **declarative descriptions** of capabilities. The agent decides when to use them.

```python
from claude_sdk import tool, create_sdk_mcp_server

@tool(
    "create_item",
    "Create a new item with given name and properties",
    {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Item name"},
            "category": {"type": "string", "description": "Category"},
        },
        "required": ["name"]
    }
)
async def create_item(args):
    item = store.create(args["name"], args.get("category"))
    return {"content": [{"type": "text", "text": f"Created: {item['name']} (id: {item['id']})"}]}

@tool(
    "list_items",
    "List all items with their status and stats",
    {"type": "object", "properties": {}}
)
async def list_items(args):
    items = store.get_all()
    text = "\n".join(f"- {i['name']} ({i['status']})" for i in items)
    return {"content": [{"type": "text", "text": text or "No items yet."}]}

# Register all tools as MCP server
ALL_TOOLS = [create_item, list_items]  # add more here
server = create_sdk_mcp_server(
    name="my-project",
    version="1.0.0",
    tools=ALL_TOOLS,
)
```

**Rule:** Each tool = one atomic operation. Agent combines them.

### Step 2: Configure Agent (agent.py)

```python
from claude_sdk import ClaudeSDKClient, create_agent_options

SYSTEM_PROMPT = """You are a helpful assistant that manages {domain}.

Available tools:
- create_item: Create new items
- list_items: Show all items
- complete_item: Mark item as done
- get_stats: Show aggregate statistics

Rules:
- Be concise (1-2 sentences per response)
- After completing an action, confirm what you did
- If user intent is ambiguous, ask for clarification
- {custom_behavior_rules}
"""

def create_options(settings):
    return create_agent_options(
        system_prompt=SYSTEM_PROMPT.format(
            domain=settings.get("domain", "tasks"),
            custom_behavior_rules=settings.get("personal_prompt", ""),
        ),
        mcp_servers=[tools.server],
        allowed_tools=["create_item", "list_items", "complete_item", "get_stats", "Read"],
        permission_mode="bypassPermissions",
        max_turns=10,
        max_buffer_tokens=50_000_000,
    )

# One-shot query (stateless)
async def run_agent_turn(prompt, settings):
    options = create_options(settings)
    client = ClaudeSDKClient(options)
    messages = await client.query(prompt)
    return messages

# Multi-turn session (stateful)
class AgentSession:
    def __init__(self, settings):
        self.client = ClaudeSDKClient(create_options(settings))

    async def send(self, message):
        return await self.client.query(message)

    async def close(self):
        await self.client.close()
```

### Step 3: WebSocket Server (server.py)

```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], ...)

# REST endpoints for direct CRUD (bypass agent)
@app.get("/api/items")
async def get_items():
    return store.get_all()

@app.post("/api/items")
async def create_item(data: ItemCreate):
    return store.create(data.name, data.category)

# WebSocket for agent chat (streaming)
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    session = AgentSession(settings_store.load())
    try:
        while True:
            data = await ws.receive_json()
            messages = await session.send(data["message"])
            for msg in messages:
                if msg.type == "text":
                    await ws.send_json({"type": "text", "text": msg.text})
                elif msg.type == "tool_use":
                    await ws.send_json({"type": "tool_use", "name": msg.name, "input": msg.input})
    except WebSocketDisconnect:
        await session.close()
```

### Step 4: Frontend WebSocket Hook

```typescript
function useAgent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = () => {
    const ws = new WebSocket("ws://localhost:8000/ws/chat");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "text") {
        setMessages(prev => [...prev, { role: "assistant", content: data.text }]);
      } else if (data.type === "tool_use") {
        // Show tool call indicator in UI
      } else if (data.type === "image") {
        // Show generated image
      }
    };
    wsRef.current = ws;
  };

  const send = (message: string) => {
    wsRef.current?.send(JSON.stringify({ message }));
    setMessages(prev => [...prev, { role: "user", content: message }]);
  };

  return { messages, send, connect };
}
```

---

## Design Principles

### 1. Tools are Atomic
Each tool does ONE thing. Agent composes them.
- Good: `create_item`, `complete_item`, `get_stats`
- Bad: `create_and_complete_if_simple_item`

### 2. System Prompt = Behavior Config
Change agent behavior by editing the system prompt, not code.
- Strictness levels → prompt rules
- Personality → prompt tone
- Custom workflows → prompt instructions

### 3. Settings-Driven Adaptation
User preferences stored in settings.json, injected into system prompt at runtime.
- No code changes for behavioral tweaks
- A/B test different prompts easily

### 4. Dual Access: Agent + REST
- Agent chat for natural language (flexible, exploratory)
- REST API for direct operations (fast, deterministic, for UI buttons)
- Both hit the same store

### 5. Streaming Always
- WebSocket for real-time agent responses
- User sees agent "thinking" (tool calls visible)
- Reduces perceived latency

### 6. Filesystem Monitoring for Side Effects
- Snapshot state before agent turn
- After turn, diff for new files (images, exports)
- Send side effects to frontend

---

## Adding New Capabilities

To add a new feature:

1. Write a tool function in `tools.py`
2. Add to `ALL_TOOLS` list
3. Add tool name to `allowed_tools` in agent options
4. (Optional) Update system prompt with usage rules
5. Done. Agent will use it when relevant.

No new handlers, no routing, no state machine changes.

---

## When to Use This Pattern

**Good fit:**
- Chat-based interfaces (natural language primary)
- Exploratory workflows (user doesn't know exact path)
- Prototype-to-product (add tools iteratively)
- Multimodal (text + images + files)

**Bad fit:**
- High-frequency operations (agent latency 5-15s per turn)
- Strict deterministic flows (payment processing, auth)
- Background schedulers (no user prompt to trigger agent)
- Budget-sensitive (every interaction = full Claude API call)

**Hybrid approach:** Use agent-first for chat/exploration, rule-based for schedulers/buttons/critical paths.

---

## Reference Implementation
Gleb Kalinin's Visual Habit Tracker: https://github.com/glebis/claude-sdk-visual-habit-tracker

Key files to study:
- `backend/agent.py` — Agent setup with configurable strictness
- `backend/tools.py` — MCP tool definitions with `@tool` decorator
- `backend/server.py` — FastAPI + WebSocket streaming
- `backend/image_generator.py` — Gemini multimodal integration
