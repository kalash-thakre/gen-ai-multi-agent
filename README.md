# Multi-Agent AI System

## Overview
This project is a multi-agent AI system designed to handle various tasks with improved efficiency and collaboration between agents. Each agent is specialized in different areas, leading to a robust and scalable system.

## Features
- Distributed task management
- Real-time collaboration between agents
- Highly modular architecture
- Easy integration with other systems

## Requirements
- Python 3.8 or higher
- Docker
- Required Python packages (listed in `requirements.txt`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kalash-thakre/gen-ai-multi-agent.git
   cd gen-ai-multi-agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- Run the application:
   ```bash
   python main.py
   ```
- Access the API via `http://localhost:8000/`

## Project Structure
```
/gen-ai-multi-agent
├── main.py            # Entry point of the application
├── agents/            # Directory for agent implementations
│   ├── agent1.py
│   ├── agent2.py
│   └── ...
├── utils/             # Utility functions
├── requirements.txt   # Python dependencies
└── Dockerfile         # Docker configuration
```

## Environment Setup
- Ensure that Docker is installed on your machine.
- Use the provided `Dockerfile` to build the Docker image:
   ```bash
   docker build -t multi-agent-ai .
   ```

## Docker Deployment
To run the application using Docker:
```bash
docker run -p 8000:8000 multi-agent-ai
```

## API Endpoints
- **GET /api/agents**: List all agents
- **POST /api/task**: Send a task to an agent
- **GET /api/status**: Get the status of the system