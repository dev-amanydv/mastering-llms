# Prompt Caching

> Reduce latency and cost by reusing previously processed context across LLM calls.

---

## What is Prompt Caching?

Every time you send a message to an LLM, the model has to **process every single token** in your prompt — system instructions, context, documents, conversation history — before it can generate a response. For long prompts, this is expensive and slow.

**Prompt caching** lets you tell the provider: *"this part of the prompt isn't changing — process it once, cache it, and reuse it on subsequent calls."*

The cached portion is stored server-side (typically for 5 minutes, extendable with each use). On cache hits, you skip the full processing of that context, which means:

- ⚡ **Lower latency** — up to 80% faster time-to-first-token
- 💰 **Lower cost** — cached input tokens are billed at a fraction of normal input price
- 🔁 **Same output quality** — the model behaves identically; caching is purely an infrastructure optimization

---

## How it Works

```
Without caching                     With caching
─────────────────────               ─────────────────────────────
Request 1:                          Request 1:
  [System prompt]      ──────────►  [System prompt]  ◄── write cache
  [Long document]                   [Long document]
  [User question]                   [User question]
                                           │
Request 2:                          Request 2:
  [System prompt]      ──────────►  [System prompt]  ◄── cache HIT ✓
  [Long document]                   [Long document]       (skip processing)
  [New question]                    [New question]
```

On the second request, the large static context (system prompt + document) is served from cache. Only the new user question needs to be freshly processed.

---

## When Should You Use It?

Prompt caching is most valuable when you have a **large, stable block of text** that you're sending repeatedly:

| Use Case | Cacheable Content |
|---|---|
| Document Q&A | The full document (PDF, book, codebase) |
| Customer support bot | Long system prompt with product rules |
| RAG pipeline | Retrieved chunks that don't change per query |
| Multi-turn chat | Growing conversation history |
| Code assistant | Entire codebase as context |
| Few-shot prompting | Large bank of examples |

The rule of thumb: **if it doesn't change between calls, cache it.**

---

## Provider Support

| Provider | Support | Cache Duration | Cost (cached) |
|---|---|---|---|
| Anthropic (Claude) | ✅ Native | 5 min (resets on use) | ~10% of normal input cost |
| OpenAI | ✅ Automatic | 5–10 min | ~50% of normal input cost |
| Google (Gemini) | ✅ Explicit API | 1 hour+ | Varies |
| Groq | ❌ Not yet | — | — |

---

## Anthropic — Explicit Cache Control

Anthropic requires you to **explicitly mark** what to cache using `cache_control`.

### Basic Example — Caching a System Prompt

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": """You are an expert Python tutor. Your job is to help 
            students understand Python concepts clearly and concisely.
            Always provide working code examples. Explain line by line 
            when the student asks. Be encouraging and patient.""",
            "cache_control": {"type": "ephemeral"}  # 👈 mark for caching
        }
    ],
    messages=[
        {"role": "user", "content": "What is a list comprehension?"}
    ]
)

print(response.content[0].text)
```

### Document Q&A — Caching a Large Document

This is the most impactful use case. Load a document once, ask many questions:

```python
import anthropic

client = anthropic.Anthropic()

# Load a large document (e.g. hamlet.txt, a codebase, a PDF's text)
with open("hamlet.txt", "r") as f:
    hamlet_text = f.read()

def ask_about_document(question: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a literary analyst. Answer questions about the text provided.",
            },
            {
                "type": "text",
                "text": hamlet_text,
                "cache_control": {"type": "ephemeral"}  # 👈 cache the whole document
            }
        ],
        messages=[
            {"role": "user", "content": question}
        ]
    )
    
    # Check cache usage in response metadata
    usage = response.usage
    print(f"Input tokens:          {usage.input_tokens}")
    print(f"Cache write tokens:    {getattr(usage, 'cache_creation_input_tokens', 0)}")
    print(f"Cache read tokens:     {getattr(usage, 'cache_read_input_tokens', 0)}")
    
    return response.content[0].text


# First call: writes the cache (slightly higher cost, full latency)
print("Q1:", ask_about_document("Who is Ophelia?"))

# Second call: reads from cache (lower cost, much faster)
print("Q2:", ask_about_document("What happens to Ophelia in the end?"))

# Third call: still hitting cache
print("Q3:", ask_about_document("What is the significance of 'To be or not to be'?"))
```

**Output on second/third calls:**
```
Input tokens:          42
Cache write tokens:    0
Cache read tokens:     32768    ← entire document served from cache
```

### Multi-turn Conversation with Cached History

```python
import anthropic

client = anthropic.Anthropic()

conversation_history = []

def chat(user_message: str) -> str:
    # Add new user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Mark all messages except the last as cacheable
    messages_with_cache = []
    for i, msg in enumerate(conversation_history):
        if i == len(conversation_history) - 2:  # second to last
            messages_with_cache.append({
                **msg,
                "content": [
                    {
                        "type": "text",
                        "text": msg["content"] if isinstance(msg["content"], str) else msg["content"],
                        "cache_control": {"type": "ephemeral"}  # 👈 cache growing history
                    }
                ]
            })
        else:
            messages_with_cache.append(msg)
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=messages_with_cache
    )
    
    assistant_reply = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })
    
    return assistant_reply

# Each turn caches the history so only the latest message is freshly processed
print(chat("Hi! I'm learning about machine learning."))
print(chat("Can you explain gradient descent?"))
print(chat("What's the difference between batch and stochastic gradient descent?"))
```

---

## OpenAI — Automatic Caching

OpenAI caches automatically — no code changes needed. The first 1024+ tokens of identical prompts are cached server-side and reused if the same prefix is sent within ~10 minutes.

```python
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a senior software engineer specializing in Python backend development.
[...imagine 2000 tokens of detailed instructions, style guides, and examples here...]
"""

def ask(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # automatically cached by OpenAI
            {"role": "user", "content": question}
        ]
    )
    
    # Check if cache was used
    usage = response.usage
    if hasattr(usage, 'prompt_tokens_details'):
        cached = usage.prompt_tokens_details.cached_tokens
        print(f"Cached tokens used: {cached}")
    
    return response.choices[0].message.content


# OpenAI will cache SYSTEM_PROMPT automatically after the first call
print(ask("How do I handle database connections in FastAPI?"))
print(ask("What's the best way to structure async routes?"))
```

> **Note:** OpenAI's caching is prefix-based. The cached portion must be at the **beginning** of the prompt and be at least 1024 tokens long. Moving the system prompt or changing anything before the cached block will cause a cache miss.

---

## Using LiteLLM (Provider-Agnostic)

[LiteLLM](https://github.com/BerriAI/litellm) provides a unified interface so you can use prompt caching across providers with a consistent API:

```python
from litellm import completion

# Works with Claude, OpenAI, Gemini, and more
response = completion(
    model="anthropic/claude-opus-4-5",
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are a helpful assistant with deep knowledge of LLMs.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        },
        {
            "role": "user",
            "content": "Explain the transformer architecture."
        }
    ]
)

print(response.choices[0].message.content)
```

---

## Measuring Cache Performance

Track your cache efficiency to verify you're getting the expected savings:

```python
import anthropic
import time

client = anthropic.Anthropic()

def timed_request(question: str, document: str, label: str):
    start = time.time()
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system=[
            {"type": "text", "text": "Answer questions about the document."},
            {"type": "text", "text": document, "cache_control": {"type": "ephemeral"}}
        ],
        messages=[{"role": "user", "content": question}]
    )
    
    elapsed = time.time() - start
    usage = response.usage
    
    cache_writes = getattr(usage, 'cache_creation_input_tokens', 0)
    cache_reads  = getattr(usage, 'cache_read_input_tokens', 0)
    
    print(f"\n[{label}]")
    print(f"  Time:         {elapsed:.2f}s")
    print(f"  Input tokens: {usage.input_tokens}")
    print(f"  Cache writes: {cache_writes}  {'(first call — writing cache)' if cache_writes else ''}")
    print(f"  Cache reads:  {cache_reads}   {'(cache HIT ✓)' if cache_reads else ''}")
    print(f"  Answer:       {response.content[0].text[:80]}...")


with open("hamlet.txt") as f:
    doc = f.read()

timed_request("Who is Hamlet?",           doc, "Call 1 — cache MISS")
timed_request("What is the ghost?",       doc, "Call 2 — cache HIT")
timed_request("What happens at the end?", doc, "Call 3 — cache HIT")
```

**Sample output:**
```
[Call 1 — cache MISS]
  Time:         3.42s
  Input tokens: 32810
  Cache writes: 32768  (first call — writing cache)
  Cache reads:  0

[Call 2 — cache HIT]
  Time:         0.81s   ← 4x faster
  Input tokens: 42
  Cache writes: 0
  Cache reads:  32768   (cache HIT ✓)

[Call 3 — cache HIT]
  Time:         0.79s
  Input tokens: 45
  Cache writes: 0
  Cache reads:  32768   (cache HIT ✓)
```

---

## Common Pitfalls

**Cache miss on every call** — The cached block must be byte-for-byte identical. Even a single character change (e.g. injecting a timestamp or user ID into the system prompt) breaks the cache. Keep dynamic content in the user message, not the cached block.

**Minimum token threshold** — Anthropic requires at least **1024 tokens** to be eligible for caching. Caching a short 50-word system prompt does nothing.

**Cache expiry** — The default TTL is 5 minutes. If your use case involves long gaps between calls, you won't get a cache hit. Cache is refreshed each time it's hit, so active conversations naturally stay warm.

**Wrong placement** — Always put the cache marker on the **largest, most stable block**. Caching a 20-token system prompt while passing a 10,000-token document uncached is backwards.

---

## Key Takeaways

- Prompt caching is one of the easiest wins in LLM engineering — minimal code change, significant cost and latency reduction.
- Anthropic requires explicit `cache_control` markers. OpenAI does it automatically.
- The pattern is always: **large static content goes in the cache, dynamic content goes in the user message**.
- Always monitor `cache_read_input_tokens` to confirm your cache is actually being hit.
- Rotate your cache boundary as conversations grow to keep the largest possible prefix cached.

---

## References

- [Anthropic Prompt Caching Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [OpenAI Prompt Caching Docs](https://platform.openai.com/docs/guides/prompt-caching)
- [LiteLLM Caching Docs](https://docs.litellm.ai/docs/caching/prompt_caching)
- [Ed Donner's llm_engineering course](https://github.com/ed-donner/llm_engineering)