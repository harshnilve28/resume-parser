#  AI-Powered Resume Parsing System

> A cloud-native, fully automated resume parsing pipeline built on Microsoft Azure — featuring Docker, N8N, OpenAI, Flask, Supabase, and Jenkins CI/CD.

---

## 🌟 Overview

This system automatically parses resume PDFs uploaded by users through an N8N chat interface. The resume is analyzed by **OpenAI**, converted to structured JSON, stored via a **Flask API** into **Supabase (PostgreSQL)** — all running on **3 Azure VMs** with full **Jenkins CI/CD automation**.

### Flow

```
User → N8N Chat Upload
        ↓
  OpenAI (Resume Parsing)
        ↓
   Structured JSON
        ↓
  Flask API (VM2 :5000)
        ↓
  Supabase / PostgreSQL (VM1)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Azure Virtual Network                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │     VM1      │  │     VM2      │  │       VM3        │  │
│  │  DB Server   │  │   Backend    │  │   Automation     │  │
│  │              │  │              │  │                  │  │
│  │     Supabase │  │     Flask    │  │      N8N         │  │
│  │  (Postgres)  │  │  API :5000   │  │  :5678           │  │
│  │              │  │              │  │     Azure OpenAI │  │
│  │  🐳 Docker   │  │  🐳 Docker  │  │  🐳 Docker       │  │
│  │              │  │     Jenkins  │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│   Private IP Only    Private IP Only   Public IP (N8N UI)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Cloud | Microsoft Azure |
| Automation | N8N |
| AI / LLM | OpenAI |
| Backend | Python Flask |
| Database | Supabase (PostgreSQL) |
| Containerization | Docker & Docker Compose |
| CI/CD | Jenkins |
| Testing | Pytest + Pylint |
| Registry | Docker Hub / Azure Container Registry |

---

## ☁️ Infrastructure Setup

### Azure Virtual Network (VNet)

All 3 VMs are deployed inside a single VNet with **static private IPs** for secure internal communication. Only VM3 (N8N) has a public IP exposed.

### VM Configuration

| VM | Role | Private IP | Public IP | Exposed Port |
|---|---|---|---|---|
| VM1 | Database Server (Supabase) | 10.0.0.4 | ❌ None | Internal only |
| VM2 | Backend Server (Flask + Jenkins) | 10.0.0.5 | ❌ None | Internal :5000 |
| VM3 | Automation Server (N8N) | 10.0.0.6 | ✅ Yes | :5678 |

### NSG Rules

- SSH (port 22): Key-based auth only, password login disabled
- Port 5678: Open to public (N8N UI)
- Port 5000: Internal VNet only (Flask API)
- Supabase ports: Internal VNet only

---

## 📸 Screenshots

### 1. Azure Virtual Network
<!-- Add your VNet screenshot here -->
![Azure VNet](./screenshots/vnet.png)

---

### 2. Virtual Machines
<!-- Add your VMs overview screenshot here -->
![Azure VMs](./screenshots/vms.png)

---

### 3. N8N Workflow
<!-- Add your N8N workflow screenshot here -->
![N8N Workflow](./screenshots/n8n.png)

---

### 4. Jenkins CI/CD Pipeline
<!-- Add your Jenkins pipeline screenshot here -->
![Jenkins Pipeline](./screenshots/jenkins.png)

---

### 5. Supabase Database
<!-- Add your Supabase/DB screenshot here -->
![Supabase DB](./screenshots/database.png)

---

### 6. Flask API Response
<!-- Add your API response screenshot here -->
![Flask API](./screenshots/flask_api.png)

---

### 7. Docker Containers Running
<!-- Add your docker ps screenshot here -->
![Docker Containers](./screenshots/docker.png)

---

## 🗄️ Database Design

### `candidates`
| Column | Type |
|---|---|
| id | UUID (PK) |
| full_name | text |
| summary | text |
| years_experience | float |
| created_at | timestamp |

### `contacts`
| Column | Type |
|---|---|
| id | UUID |
| candidate_id | FK → candidates |
| email | text |
| phone | text |
| linkedin_url | text |
| github_url | text |

### `skills`
| Column | Type |
|---|---|
| id | UUID |
| candidate_id | FK → candidates |
| skill_name | text |
| category | text (technical/soft/tool) |

### `education`
| Column | Type |
|---|---|
| id | UUID |
| candidate_id | FK → candidates |
| degree | text |
| institution | text |
| start_year | int |
| end_year | int |

### `work_experience`
| Column | Type |
|---|---|
| id | UUID |
| candidate_id | FK → candidates |
| company | text |
| role | text |
| start_date | date |
| end_date | date |
| description | text |

---

## 📡 API Reference

### `POST /api/v1/candidate`

Accepts structured JSON parsed by Azure OpenAI and inserts into all Supabase tables.

**Request Body:**
```json
{
  "candidate": {
    "full_name": "John Doe",
    "summary": "Experienced software engineer...",
    "years_experience": 5.0
  },
  "contacts": {
    "email": "john@example.com",
    "phone": "+91-9999999999",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe"
  },
  "skills": [
    { "skill_name": "Python", "category": "technical" },
    { "skill_name": "Docker", "category": "tool" }
  ],
  "education": [
    {
      "degree": "B.Tech Computer Science",
      "institution": "IIT Bombay",
      "start_year": 2018,
      "end_year": 2022
    }
  ],
  "experience": [
    {
      "company": "Acme Corp",
      "role": "Backend Engineer",
      "start_date": "2022-07-01",
      "end_date": "2024-01-01",
      "description": "Built scalable microservices..."
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "candidate_id": "uuid-here",
  "message": "Resume data inserted successfully"
}
```

---

## 🔄 CI/CD Pipeline

Jenkins pipeline defined in `Jenkinsfile`:

```
Checkout → Install Dependencies → Pylint (≥8.0) → Pytest (all pass)
    → Build Docker Image → Push to Registry → Deploy to Azure VM
```

### Quality Gates
- ✅ Pylint score must be **≥ 8.0**
- ✅ All Pytest unit tests must **pass**
- ✅ Coverage report generated on every run

---

## 🔐 Environment Variables

Create a `.env` file (never commit this):

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Supabase / PostgreSQL
SUPABASE_URL=http://10.0.0.4:8000
SUPABASE_KEY=your_supabase_anon_key
DATABASE_URL=postgresql://postgres:password@10.0.0.4:5432/postgres

# Flask
FLASK_ENV=production
FLASK_PORT=5000
```

---

## 🐳 Running Locally

### VM1 – Supabase
```bash
cd vm1-database/
docker-compose up -d
```

### VM2 – Flask API
```bash
cd vm2-backend/
docker-compose up -d
```

### VM3 – N8N
```bash
cd vm3-automation/
docker-compose up -d
# Access N8N at http://<VM3-PUBLIC-IP>:5678
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html

# Run Pylint
pylint app/ --fail-under=8
```

### Test Coverage Includes:
- JSON schema validation
- Data segregation logic
- Database insertion logic

---

## 📁 Project Structure

```
resume-parsing-system/
│
├── vm1-database/
│   └── docker-compose.yml          # Supabase setup
│
├── vm2-backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py               # Flask API routes
│   │   ├── models.py               # DB models
│   │   ├── validator.py            # Input validation
│   │   └── db.py                   # Supabase client
│   ├── tests/
│   │   ├── test_validation.py
│   │   ├── test_segregation.py
│   │   └── test_db.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│
├── vm3-automation/
│   ├── docker-compose.yml          # N8N setup
│   └── n8n-workflow.json           # Exported N8N workflow
│
├── screenshots/
│   ├── vnet.png
│   ├── vms.png
│   ├── n8n.png
│   ├── jenkins.png
│   └── database.png
│   └── Jenkinsfile
│
├── .env.example
└── README.md
```
