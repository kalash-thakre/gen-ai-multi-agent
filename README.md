# Gen AI Multi-Agent

## Overview
This project is a comprehensive multi-agent system designed to tackle various tasks using artificial intelligence. It leverages multiple agents to process requests intelligently, utilizing shared tools and databases.

## Features
- Multi-agent architecture
- Task automation through various agents
- Integration with APIs for enhanced functionalities
- Easy setup and deployment

## Project Structure
```
.vscode/
  └── settings.json  # Visual Studio Code settings folder

multi_agent_system/
  ├── __init__.py      # Initializer for multi_agent_system
  ├── agent.py         # Contains the base agent implementation
  ├── llm.py           # Includes logic for language models
  ├── mcp_registry.py  # Manages the registration of different agents
  └── database/
      └── db.py       # Database connection and queries
  └── sub_agents/
      ├── calendar_agent.py  # Handles calendar functionalities
      ├── notes_agent.py     # Manages notes
      └── task_agent.py      # Manages tasks
  └── tools/
      ├── calendar_tools.py  # Tools related to calendar operations
      ├── notes_tools.py     # Tools for note processing
      └── task_tools.py      # Tools for task management

static/
  ├── index.html     # Main HTML file
  ├── main.py        # Main entry point for the application
  ├── requirements.txt # Needed packages for the application
  ├── Dockerfile     # Docker configuration file
  ├── .env.save      # Example environment variables
  └── .gitignore     # Specifies files to be ignored by git
```

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/kalash-thakre/gen-ai-multi-agent.git
   cd gen-ai-multi-agent
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide
To run the application, use the following command:
```bash
python main.py
```

## Environment Setup
Ensure that you have Python 3.6 or higher installed. You may also set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Docker Deployment
To build and run the Docker container, use:
```bash
docker build -t gen-ai-multi-agent .
docker run -p 5000:5000 gen-ai-multi-agent
```
## Video 
https://drive.google.com/file/d/1FTtTcpu9LupIm1XgCe3-qwuL8JICEfCH/view?usp=sharing


## Snapshot
<img width="3199" height="1926" alt="image" src="https://github.com/user-attachments/assets/e67bfddb-c134-4b97-abfe-b3056a25edca" />

## API Endpoints
- **GET /api/tasks**: Retrieves all tasks.
- **POST /api/tasks**: Creates a new task.
- **GET /api/notes**: Retrieves all notes.
- **POST /api/notes**: Creates a new note.
- **GET /api/calendar**: Retrieves calendar events.
- **POST /api/calendar**: Creates a new calendar event.
