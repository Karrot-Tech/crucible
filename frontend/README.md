# Crucible Frontend

The interactive workspace UI for the Crucible agent mesh system.

## Tech Stack
- **Next.js 15** (App Router)
- **React 19**
- **Tailwind CSS**
- **shadcn/ui** components
- **React Flow** for agent mesh visualization

## Setup

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Key Components

| Component | Description |
|-----------|-------------|
| `Workspace.tsx` | Main layout with agent mesh, chat, and controls |
| `AgentFlow.tsx` | React Flow visualization of agent network |
| `AgentCardNode.tsx` | Individual agent node in the mesh |
| `AgentDetailView.tsx` | Modal showing agent details ("Brain View") |
| `TeamChatPanel.tsx` | Real-time agent communication feed |
| `SessionSetupDialog.tsx` | Session initialization form |
| `OutputView.tsx` | SOAP note output display |

## Environment

Expects backend running at `http://localhost:8000`
