# SynapseHR: AI-Powered Autonomous HRMS

SynapseHR is a modern, autonomous HR Management System designed to orchestrate complex HR workflows through natural language. It features a hierarchical multi-role dashboard, real-time conversational oversight, and a unified skill-registry architecture.

## 🛠️ Technical Stack & Architecture

### **Frontend (The Experience Layer)**
- **React (Vite)**: Chosen for its blazing-fast HMR and component-based architecture. Used for the entire reactive UI.
- **Framer Motion**: Powering all premium micro-animations (Hover/Tap/Transitions). Used for tactile button feedback and card entry effects.
- **Lucide React**: A clean, consistent icon set used throughout the sidebar and action buttons for high-end aesthetics.
- **Tailwind CSS & Vanilla CSS**: Utilizing a curated design system with custom variables (`--primary`, `--success`, etc.) for glassmorphic and premium dark/light modes.
- **Recharts**: For high-performance, responsive analytics and reporting visualizations.

### **Backend (The Core Logic)**
- **FastAPI (Python)**: An asynchronous, high-performance web framework. Used for all API endpoints, intent parsing orchestration, and skill execution.
- **SQLAlchemy (ORM)**: For robust, type-safe database interactions and relational mapping between Users, Tickets, and Chat History.
- **Pydantic**: Critical for data validation and schema enforcement between the AI orchestrator and the frontend.
- **SQLite (Development)**: A lightweight, serverless SQL database used for rapid prototyping and reliable data persistence.

### **AI & Orchestration (The Brain)**
- **Custom Agent Controller**: A proprietary logic layer that coordinates multi-step plans. It "decides" which skills to invoke based on user intent.
- **LLM-Driven Intent Parser**: Uses advanced LLMs to translate natural language into actionable JSON plans.
- **Skill-Based Registry**: A modular architecture where every HR function (Leave Request, Payroll Query, Admin) is a self-contained "Skill" class.

---

## 🔄 System Workflow

The SynapseHR workflow is designed to be autonomous and role-aware:

### 1. **Authentication & Initialization**
- **Trigger**: User logs into the platform with their role (Employee, Manager, or Admin).
- **Action**: The system automatically triggers the `Show my workspace` command.
- **Logic**: The **RBAC (Role-Based Access Control)** filter determines which modules to load based on the user's hierarchy.

### 2. **Conversational Intent Parsing**
- **Trigger**: User types a message (e.g., "Mithun wants sick leave for tomorrow").
- **Action**: The **Intent Parser** analyzes the message context, role, and history.
- **Extraction**: It identifies the **Skill** (`ticket.manage`), the **Action** (`create`), and **Entities** (`date="2026-04-04"`, `reason="Sick Leave"`).

### 3. **Hierarchical Execution**
- **Trigger**: The **Agent Controller** receives the plan.
- **Action**: It iterates through the plan and executes each skill.
- **Oversight Check**: For every action, the system verifies `can_invoke` and `can_manage_user` to ensure no role-boundary violations occur.
- **Persistence**: Every message and result is saved to the `chat_messages` table for permanent record-keeping.

### 4. **Dynamic UI Generation**
- **Trigger**: The skill execution completes successfully.
- **Action**: The backend returns a **Unified UI Object** (e.g., `TICKET_CARD`).
- **Rendering**: The frontend's `ChatInterface` and `Dashboard` dynamically render the appropriate component (Form, Table, or Card) with interactive buttons.

### 5. **Tactile Interaction**
- **Trigger**: User interacts with a generated card (e.g., Manager clicks "Approve").
- **Action**: A direct `ACTION:` trigger is sent back to the backend, completing the loop with high-performance execution.

---

## 🔒 Security & RBAC Hierarchy

| Role | Access Level | Conversational Oversight |
| :--- | :--- | :--- |
| **Admin** | Full System Access | Can review Employee chats, create users, view all reports. |
| **Manager** | Operational Oversight | Can review Employee chats within their scope, approve/deny tickets. |
| **Employee** | Personal Operations | Can only view their own history, raise tickets, and query their payroll. |

---

Developed with ❤️ for Advanced Agentic Coding.
