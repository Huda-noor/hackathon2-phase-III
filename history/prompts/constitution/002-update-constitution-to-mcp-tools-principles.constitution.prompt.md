---
id: 002
title: Update Constitution to MCP Tools Principles
stage: constitution
date: 2026-02-07
surface: agent
model: gemini-cli
feature: none
branch: null
user: null
command: /sp.constitution
labels: []
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/tasks-template.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: MCP Tools & AI Agent Behavior for Todo Chatbot

Core principles:
- Intent accuracy: User intent must map correctly to tool calls
- Determinism: Same input should lead to same tool decision
- Transparency: Tool calls must be visible and traceable
- Safety: Agent must not perform unauthorized actions

Key standards:
- MCP tools must follow defined schemas
- Tool inputs and outputs strictly validated
- Agent behavior rules followed consistently
- Friendly confirmations after actions
- Graceful error handling

Constraints:
- Use OpenAI Agents SDK
- MCP Server via official MCP SDK
- No direct database access by agent
- Tools act as single source of truth

Success criteria:
- All MCP tools implemented and callable
- Agent correctly selects tools based on user input
- Tool outputs returned in structured format
- Errors handled without breaking conversation

## Response snapshot

I have updated the project constitution to version 2.0.0, which includes the new principles for the "MCP Tools & AI Agent Behavior for Todo Chatbot" project. The `plan` and `tasks` templates have also been updated to align with these changes.

Suggested commit message:
`docs: amend constitution to v2.0.0 (MCP Tools principles)`

## Outcome

- ✅ Impact: Major update to the project's guiding principles.
- 🧪 Tests: n/a
- 📁 Files: 
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/tasks-template.md
- 🔁 Next prompts: Potentially `/sp.specify` or `/sp.plan` to start implementing features under the new constitution.
- 🧠 Reflection: The script-based PHR creation failed, requiring a fallback to the manual, agent-native method. The process was successful but highlights a dependency on the shell environment that could be fragile.

## Evaluation notes (flywheel)

- Failure modes observed: Shell script execution failure on Windows due to node-pty binary issues.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
