# 🌿 OuttaDoor — Personalized Outdoor Adventure Planner

**Turn your free time into a little adventure.**

OuttaDoor is a web application that helps users discover simple outdoor activities based on their available time and preferred mood. It generates a structured adventure quest with activities, helpful tips, and safety guidance.

🌐 **Live Demo:** https://outtadoor-1.onrender.com/

## ✨ Features

- **Personalized quests:** Generate outdoor adventure ideas based on your selected preferences.
- **Three-step adventures:** Get a structured quest with three activities.
- **Mood-based planning:** Tailor suggestions to the kind of experience you're looking for.
- **Helpful tips:** Receive practical suggestions for your adventure.
- **Safety guidance:** Get reminders to help plan outdoor activities responsibly.
- **Copy quest:** Copy the generated quest for later use.
- **AI-assisted generation:** Supports local Gemma model inference through Ollama, with fallback quests when the model is unavailable.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| HTML | Webpage structure |
| CSS | Styling and responsive interface |
| JavaScript | Frontend interactions and API requests |
| Python | Backend logic |
| FastAPI | REST API |
| Pydantic | Request and response data validation |
| Ollama | Local model inference |
| Gemma 3 1B | Local language model used for quest generation |
| Render | Public frontend and backend hosting |

## 🏗️ Project Structure

```text
OuttaDoor/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── images/
├── .gitignore
└── README.md
```

*Your repository may contain additional files.*

## 🚀 Run Locally

### Prerequisites

- Python installed
- Git installed
- Ollama installed if you want to run the local Gemma model

### 1. Clone the repository

```bash
git clone https://github.com/aditric7/OuttaDoor.git
cd OuttaDoor
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
python -m uvicorn main:app --reload
```

The local API should be available at:

- API: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs

### 4. Run the frontend

Open `frontend/index.html` using VS Code Live Server or another local static web server.

The deployed frontend is configured to communicate with the public backend. For local development, make sure the frontend API URL matches the backend environment you're running.

### 5. Optional: Run Gemma locally

Install Ollama and download the model:

```bash
ollama pull gemma3:1b
```

Start Ollama and keep it running while using the local backend. If Ollama is unavailable, the backend may return predefined fallback quests instead.

## 🌍 Deployment

OuttaDoor is deployed on Render using separate frontend and backend services.

- **Frontend:** https://outtadoor-1.onrender.com/
- **Backend:** https://outtadoor.onrender.com/
- **API documentation:** https://outtadoor.onrender.com/docs

The backend exposes these main endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check backend status |
| POST | `/generate-quest` | Request a generated quest |

Free hosting may sleep after inactivity, so the first request after a quiet period can take longer.

## 🤖 AI and Limitations

OuttaDoor supports local inference using Gemma 3 1B through Ollama. The deployed backend does not automatically have access to the Ollama instance running on a developer's laptop.

When the model is unavailable, the application can use predefined fallback quests. Therefore, not every quest returned by the deployed version is necessarily AI-generated.

Generated suggestions may not always be accurate about real-world locations, activity duration, or conditions. Verify location details, check local conditions, and use your own judgment before heading outdoors.

## 🔒 Privacy and Security

- Never commit API keys, passwords, or private environment files to GitHub.
- Keep private credentials in server-side environment variables.
- Do not put secret keys in frontend JavaScript.
- Check local conditions and choose activities appropriate to your situation.

## 🔮 Future Improvements

- More personalized quest recommendations
- Better validation of activity duration and location details
- Additional user preferences
- Improved error handling and loading feedback
- More robust deployment monitoring

## 👩‍💻 Author

Created as a personal software project to explore web development, API integration, and AI-assisted activity planning.

## 📄 License

No license has been specified yet. Add a license file if you decide to make the project available for reuse under specific terms.
