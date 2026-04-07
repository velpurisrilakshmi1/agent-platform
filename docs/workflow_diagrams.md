# Agent Platform - Visual Workflow Guide

Simple visual diagrams explaining how the platform works.

---

## The Big Picture

```mermaid
flowchart LR
    You["🧑 You"] -->|Submit Job| API["📥 API"]
    API -->|Process| Platform["⚙️ Platform"]
    Platform -->|Return| Result["✅ Result"]
```

**In plain English:** You send a request → The platform processes it → You get a result back.

---

## Complete Workflow

```mermaid
flowchart TD
    subgraph Step1["📥 STEP 1: Submit"]
        A["You send a question<br/>'What is Python?'"]
    end

    subgraph Step2["📋 STEP 2: Plan"]
        B["Orchestrator creates<br/>a to-do list"]
        B1["Task 1: Get info"]
        B2["Task 2: Process"]
        B3["Task 3: Validate"]
        B --> B1 --> B2 --> B3
    end

    subgraph Step3["🔧 STEP 3: Execute"]
        C["Worker runs<br/>each task"]
    end

    subgraph Step4["✅ STEP 4: Return"]
        D["You get your<br/>answer back!"]
    end

    A --> B
    B3 --> C
    C --> D
```

---

## What Happens Inside

```mermaid
sequenceDiagram
    participant You
    participant API
    participant Orchestrator
    participant Worker
    participant MCP as MCP Server
    participant RAI as RAI Validator

    You->>API: Submit job (your question)
    API->>Orchestrator: Create a plan
    Orchestrator->>API: Here's 3 tasks to do
    
    API->>Worker: Execute the tasks
    
    Worker->>MCP: Task 1: Get context
    MCP->>Worker: Here's helpful info
    
    Worker->>Worker: Task 2: Process the query
    
    Worker->>RAI: Task 3: Is this safe?
    RAI->>Worker: Yes, it's valid!
    
    Worker->>API: All done! Here's the result
    API->>You: Here's your answer!
```

---

## The Three Tasks Explained

```mermaid
flowchart LR
    subgraph Task1["🔍 Task 1: Fetch Context"]
        T1["Ask MCP Server<br/>for helpful info"]
    end

    subgraph Task2["⚙️ Task 2: Process"]
        T2["Use the info to<br/>create an answer"]
    end

    subgraph Task3["🛡️ Task 3: Validate"]
        T3["Check if answer<br/>is safe to return"]
    end

    Task1 --> Task2 --> Task3
```

**Task 1 - Fetch Context:** "Hey MCP, what do you know about this topic?"

**Task 2 - Process:** "Let me combine the question with the context to make an answer"

**Task 3 - Validate:** "Is this answer safe? No passwords or bad stuff?"

---

## Job Status Flow

```mermaid
stateDiagram-v2
    [*] --> pending: Job Created
    pending --> running: Processing Starts
    running --> completed: All Tasks Pass ✅
    running --> failed: Something Went Wrong ❌
    completed --> [*]
    failed --> [*]
```

**pending:** Job is waiting to start  
**running:** Platform is working on it  
**completed:** Success! Here's your result  
**failed:** Oops, something broke  

---

## Component Overview

```mermaid
flowchart TB
    subgraph Frontend["🌐 How You Interact"]
        API["API Endpoints<br/>/jobs"]
    end

    subgraph Brain["🧠 The Brains"]
        Proc["Job Processor<br/>(Coordinator)"]
        Orch["Orchestrator<br/>(Planner)"]
        Work["Worker<br/>(Doer)"]
    end

    subgraph Helpers["🔧 Helper Services"]
        MCP["MCP Server<br/>(Info Provider)"]
        RAI["RAI Service<br/>(Safety Checker)"]
    end

    subgraph Memory["💾 Storage"]
        Jobs["Job Store"]
        Tasks["Task Store"]
    end

    API --> Proc
    Proc --> Orch
    Proc --> Work
    Work --> MCP
    Work --> RAI
    Proc --> Jobs
    Proc --> Tasks
```

---

## Real Example Walkthrough

```mermaid
flowchart TD
    subgraph Input
        Q["Your Question:<br/>'What is Python?'"]
    end

    subgraph Processing
        J["Job Created<br/>ID: abc-123"]
        P["Plan: 3 tasks"]
        
        T1["Task 1 Output:<br/>'Python is a programming<br/>language...'"]
        T2["Task 2 Output:<br/>'Processed result for:<br/>What is Python?'"]
        T3["Task 3 Output:<br/>'Validated: true'"]
    end

    subgraph Output
        R["Final Result:<br/>✅ Validated answer<br/>ready to return!"]
    end

    Q --> J --> P
    P --> T1 --> T2 --> T3 --> R
```

---

## Error Handling

```mermaid
flowchart TD
    Start["Start Processing"] --> Check{"Task<br/>Successful?"}
    
    Check -->|Yes| Next["Continue to<br/>Next Task"]
    Check -->|No| Fail["Mark Job<br/>as Failed"]
    
    Next --> More{"More<br/>Tasks?"}
    More -->|Yes| Check
    More -->|No| Success["Mark Job<br/>as Completed ✅"]
    
    Fail --> Error["Return Error<br/>Message ❌"]
    Success --> Return["Return<br/>Result"]
```

---

## Data Flow

```mermaid
flowchart LR
    subgraph You Send
        Input["{'query': 'What is Python?'}"]
    end

    subgraph Platform Creates
        Job["Job Object"]
        Tasks["3 Task Objects"]
    end

    subgraph You Receive
        Output["{'validated': true,<br/>'final_output': '...'}"]
    end

    Input --> Job --> Tasks --> Output
```

---

## Summary: The 4 Simple Steps

```mermaid
flowchart LR
    A["1️⃣ SUBMIT<br/>Send your question"] --> B["2️⃣ PLAN<br/>Create task list"]
    B --> C["3️⃣ EXECUTE<br/>Run each task"]
    C --> D["4️⃣ RETURN<br/>Get your answer"]
    
    style A fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
```

That's it! The platform takes your question, plans how to handle it, does the work, and gives you a safe, validated answer.

---

## Try It Yourself!

```bash
# Send this to the API
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"data": {"query": "What is Python?"}}'
```

Watch the magic happen! 🎉
