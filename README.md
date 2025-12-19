# ConnectHub -> AI-Powered Networking MatchMaker

## Project Overview
An AI-driven networking assistant designed to help attendees at conferences, workshops, and seminars connect more easily. The system collects participant details such as name, email, interests and people they are looking to connect with, and then groups individuals based on shared interests and a user query.

## Implementation
The backend is fully implemented using Google ADK, with an AI agent that processes user profiles and a user defined query in order to generate meaningful connection groups. This is tested and functional via terminal.

The frontend is being developed using Streamlit, where users will submit their information, and admins will manage queries and view generated networking groups. Ongoing work includes integrating the Streamlit UI with the AI backend, and preparing the application fot deployment and real-world event usage.

Tech Stack: Python, Google ADK, Streamlit, AI Agents.

## Results
[▶️ Watch the demo video](https://drive.google.com/file/d/1qoAl-iEO0ZcfuLDSe0huf6sWEo4BqUJq/view?usp=sharing)
<img width="1285" height="432" alt="image" src="https://github.com/user-attachments/assets/40453f98-d873-488c-b9f6-7118554a16be" />

### Streamlit UI
<img width="1866" height="958" alt="image" src="https://github.com/user-attachments/assets/ed20c44b-51ef-4f2a-bd92-5330118e0913" />
<img width="1919" height="851" alt="image" src="https://github.com/user-attachments/assets/9c7fea85-0d8f-43c7-bb3c-eff45c4f12c3" />
<img width="1903" height="858" alt="image" src="https://github.com/user-attachments/assets/0a078c30-82df-476f-8ff3-a7f36ce32b9e" />
<img width="1918" height="864" alt="image" src="https://github.com/user-attachments/assets/e901faf4-87da-4ca5-8679-541733f40690" />

## Steps to implement backend

### Prerequisites
1) Python 3.10 or higher
2) Google API Key (free from Google AI Studio)

### Step 1: Set Up Virtual Environment
```python
python -m venv myvenv
.\myvenv\Scripts\Activate # On windows
```

### Step 3: Install Google ADK
```python
pip install google-adk
```

### Step 4: Create Your Agent
```python
adk create my_agent
```

When prompted:

1) Choose model: gemini-2.5-flash (option 1)
2) Choose backend: Google AI (option 1)
3) Enter your Google API Key

This creates:

```text
my_agent/
├── __init__.py
├── agent.py
└── .env        # Contains your API key
```

### Step 5: Create Student Data
Create a file students.csv in the project root:
```text
id,name,email,interests,looking_to_connect_with
1,Alice Johnson,alice@example.com,"AI, Machine Learning, Python","Backend developers, Data scientists"
2,Bob Smith,bob@example.com,"Web Development, React, TypeScript","Frontend developers, UI designers"
3,Carol Williams,carol@example.com,"Data Science, Machine Learning, Statistics","AI enthusiasts, Researchers"
4,David Brown,david@example.com,"Backend Development, Python, FastAPI","AI enthusiasts, Full-stack developers"
5,Eve Davis,eve@example.com,"UI/UX Design, Figma, User Research","Frontend developers, Product managers"
6,Frank Miller,frank@example.com,"DevOps, Cloud, Kubernetes","Backend developers, Security experts"
7,Grace Lee,grace@example.com,"AI, NLP, Deep Learning","Data scientists, Researchers"
8,Henry Wilson,henry@example.com,"Full-stack Development, React, Node.js","Backend developers, UI designers"
9,Ivy Chen,ivy@example.com,"Product Management, Agile, Strategy","UI designers, Full-stack developers"
10,Jack Taylor,jack@example.com,"Security, Cryptography, Ethical Hacking","DevOps engineers, Backend developers"
11,Mannahil Miftah,m10shaikh@gmail.com,"AI agents, Machine Learning, Computer Vision",AI Engineers
12,Muhammad Rayyan,rayyan123@gmail.com,"Machine Learning, Data Science",Data Scientist
13,Ayesha Khan,ayesha123@gmail.com,"Computer Vision, Visual AI, AR/VR","Computer Vision Engineer, AI Engineer"
14,Ali Raza,ali12r@gmail.com,"Web Development, Data Science","Data Scientist, Web Developers"
```

### Step 6: Update the Agent file
Replace the contents of my_agent/agent.py with:

```python
import csv
import os
from google.adk.agents import Agent
from pydantic import BaseModel

# Path to the students CSV file
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "students.csv")


def load_students_data() -> str:
    """Load all students from CSV and format as text."""
    students = []
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    
    data = "WORKSHOP ATTENDEES:\n\n"
    for s in students:
        data += f"- {s['name']} ({s['email']})\n"
        data += f"  Interests: {s['interests']}\n"
        data += f"  Looking to connect with: {s['looking_to_connect_with']}\n\n"
    return data


# Pydantic models for structured output
class StudentGroup(BaseModel):
    group: list[str]
    description: str


class GroupsResponse(BaseModel):
    groups: list[StudentGroup]


# Load student data
STUDENT_DATA = load_students_data()

# Create the ADK agent
root_agent = Agent(
    model='gemini-2.0-flash',
    name='workshop_matchmaker',
    description='Groups workshop attendees based on shared interests.',
    instruction=f'''You are a workshop matchmaker. Group students into teams 
based on their shared interests.

RULES:
- Create MULTIPLE groups
- Each group should have MAXIMUM 3 people
- Group people with similar interests together
- Every attendee should be in at least one group

Here is the data of all workshop attendees:

{STUDENT_DATA}

Create meaningful groups and explain why each group should connect.''',
    output_schema=GroupsResponse,
)
```

### Step 7: Test with CLI
```python
adk run my_agent
```
Type a message like:
```text
Create groups based on similar interets.
```

## Project Structure
```text
ConnectHub-Google ADK-MatchMaker/
├── my_agent/
│   ├── __init__.py      # Module init
│   ├── agent.py         # ADK agent definition
│   └── .env             # API key (GOOGLE_API_KEY=...)
├── students.csv         # Workshop attendee data
└── README.md            # This file
```
