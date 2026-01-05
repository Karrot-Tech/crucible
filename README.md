# 🧪 Crucible

**Crucible** is an advanced multi-agent psychiatric scribe system that transforms clinical conversations into structured medical documentation. It uses an autonomous event-driven agent mesh where specialized AI agents collaborate, debate, and refine clinical insights under the supervision of an intelligent orchestrator.

> *Part of the Alchemist product family — Crucible is the advanced agentic evolution of the simple scribe.*

---

## ✨ Features

### 🤖 Multi-Agent Mesh Architecture
- **9 Specialized Agents**: Safety Guardian, Risk Monitor, Clinical Analyst, Lead Diagnostician, Medical Coder, Pharmacologist, Care Planner, Scribe Architect, and Intake Coordinator
- **Central Orchestrator (Administrator)**: Manages agent coordination, resolves conflicts, and ensures safety protocols
- **Event-Driven Communication**: Agents publish and subscribe to events, enabling parallel execution and dynamic collaboration
- **Debate Mode**: Diagnosis and Medication agents can challenge each other's conclusions for improved accuracy

### 🛡️ Safety-First Design
- **Real-time Safety Monitoring**: Continuous detection of suicide/homicide risk, domestic violence, and medical emergencies
- **C-SSRS Risk Assessment**: Automatic Columbia-Suicide Severity Rating Scale evaluation when risks are detected
- **Override Protocols**: Clinical context validation can override safety flags when appropriate

### 🖥️ Interactive Workspace
- **Agent Mesh Visualization**: Real-time view of agent activity with status indicators and connection lines
- **Team Chat Panel**: Live feed of agent communications and reasoning
- **Brain View**: Click any agent to see their operational profile and prompt logic
- **Kill Switch**: Immediate network termination for safety or debugging

### 📋 Clinical Output
- **Structured SOAP Notes**: Automatic generation of psychiatric documentation
- **ICD-10-CM Mapping**: Automatic F-code diagnosis classification
- **CPT Coding**: Procedure code suggestions for billing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Bus (Pub/Sub)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │   Safety    │    │  Clinical   │    │  Diagnosis  │    │
│   │  Guardian   │◄──►│  Analyst    │◄──►│   Mapping   │    │
│   └─────────────┘    └─────────────┘    └──────┬──────┘    │
│          │                                      │           │
│          │         ┌─────────────┐              │           │
│          └────────►│ ORCHESTRATOR│◄─────────────┘           │
│                    │(Administrator)            │           │
│          ┌────────►└─────────────┘◄────────────┐           │
│          │                                      │           │
│   ┌──────┴──────┐    ┌─────────────┐    ┌──────┴──────┐    │
│   │    Risk     │    │  Medication │◄──►│  Treatment  │    │
│   │   Monitor   │    │   Manager   │    │   Planner   │    │
│   └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **Google API Key** (for Gemini LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:Karrot-Tech/crucible.git
   cd crucible
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Create .env file
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

3. **Setup Frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Run the Application**
   ```bash
   # From project root
   chmod +x start-app.sh
   ./start-app.sh
   ```

   Or run manually:
   ```bash
   # Terminal 1 - Backend
   cd backend && source venv/bin/activate && python -m uvicorn main:app --reload --port 8000
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

5. **Open in Browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

---

## 📁 Project Structure

```
crucible/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── core/           # Event bus, socket manager, logging
│   │   └── services/
│   │       ├── agents/     # Individual agent implementations
│   │       └── orchestrator.py
│   ├── main.py             # FastAPI entry point
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── workspace/  # Main workspace components
│   │   ├── hooks/          # Custom React hooks (WebSocket)
│   │   └── lib/            # Utilities and constants
│   └── package.json
├── docs/                   # Documentation
│   ├── vision.md           # Project vision
│   └── agent_architecture.md
└── start-app.sh           # Full-stack startup script
```

---

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
GOOGLE_API_KEY=your_gemini_api_key
```

---

## 🧠 Agent Roster

| Agent | Role | Priority | Description |
|-------|------|----------|-------------|
| Safety Guardian | Safety Monitor | 100 | Monitors for self-harm, violence, emergencies |
| Risk Monitor | Clinical Psychologist | 8 | Performs C-SSRS assessments |
| Clinical Analyst | Medical Scribe | 9 | Extracts symptoms, medications, conditions |
| Lead Diagnostician | Psychiatrist | 8 | Maps to ICD-10-CM F codes |
| Medical Coder | Billing Specialist | 6 | Generates CPT procedure codes |
| Pharmacologist | Psychiatrist | 5 | Reviews medication interactions |
| Care Planner | Clinical Director | 5 | Creates treatment plans |
| Scribe Architect | Documentation Specialist | 1 | Generates final SOAP notes |
| Intake Coordinator | Intake Coordinator | 10 | Session orientation and validation |

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with:
- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python API framework
- [React Flow](https://reactflow.dev/) - Agent mesh visualization
- [Google Gemini](https://ai.google.dev/) - LLM backbone
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [shadcn/ui](https://ui.shadcn.com/) - UI components

---

<p align="center">
  <strong>Crucible</strong> — Forging clinical insights under pressure 🔥
</p>
