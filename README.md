# SynapseHR

Hey there! Welcome to the SynapseHR repository. 

This project is an AI-powered HR Management System (HRMS) that heavily relies on an agentic architecture rather than just hardcoding a million different workflows. The goal is to let the user talk to an AI hr assistant that can dynamically orchestrate tasks, check who is allowed to do what (RBAC), and push modular UI cards straight to the dashboard. 

### What's Inside?

We split the codebase into two main halves under the `Code/` folder:

- **Frontend (`/frontend`)**: Built with React and Vite. It serves as a simple interface with a sidebar for generated UI cards and a chat panel on the right. Notice that there's barely any business logic here — the backend dictates exactly what UI component should render on the screen by sending a JSON `"ui_type"` via Progressive Disclosure. 
- **Backend (`/backend`)**: This is the core engine, written in FastAPI. It handles the API requests, runs intent parsing against the LLM, connects to our Postgres DB, and acts as the gatekeeper for role permissions. 

### Getting Started

There are a few different ways to run the project depending on whether you want to use Docker or run it directly on your Windows machine.

1. **Configure Environment variables**:
   First, make sure to add your Groq API key into the `.env` file within the `Code/` directory.

2. **How to Run (Windows)**:
   We've included three handy batch scripts right in the root folder so you don't have to memorize any terminal commands! 

   * **`First time setup.bat`**: Run this if you are booting the project natively for the very first time. It automatically installs all the Python (`pip`) and React (`npm`) dependencies and then launches the servers.
   * **`run_direct.bat`**: Your daily driver. Once you've run the setup script at least once, use this! It skips the slow dependency installation steps and triggers a split-second boot of both the frontend and backend servers.
   * **`run_docker.bat`**: If you have Docker Desktop installed, use this. It safely brings down any old containers and builds a fresh, completely isolated container stack for you.

Whichever script you choose, wait a few seconds and it will automatically pop open your default browser to access the React frontend at `http://localhost:5173`. 

### The Architecture & Skills

We handle tasks by routing them into "Skills" (found in `backend/app/skills/`). Each skill (like `leave.request` or `payroll.query`) represents a discrete action piece. If an employee asks for a complicated workflow, the `agent_controller.py` chains these skills together, enforces roles, executes the DB updates, and returns an audit trail.

Hope that helps you navigate things! Let me know if you run into any port mapping issues.
