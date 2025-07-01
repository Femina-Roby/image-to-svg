Image to SVG Converter · Powered by AI
Turn bitmap images (like PNG/JPG) into high-quality SVG vector graphics using Hugging Face’s StarVector model—all inside a beautifully responsive React app with a FastAPI backend.

Features
- GraphQL API built with FastAPI + Ariadne
- Live SVG preview after uploading
- Downloadable SVG output
- Dockerized frontend + backend with docker-compose
- AI-powered vectorization via StarVector (Hugging Face)

Tech Stack
| Frontend | Backend | AI | DevOps | 
| React + Apollo | FastAPI + Ariadne | StarVector | Docker + Compose | 



Getting Started
1. Clone the repo
git clone https://github.com/Femina-Roby/image-to-svg.git
cd image-to-svg


2. Add your Hugging Face API key
In backend/.env:
HF_API_KEY=your_huggingface_key_here


Never commit this key—.env is in .gitignore.


3. Run Locally with Docker Compose
docker-compose up --build


- Backend: http://localhost:8000/graphql
- Frontend: http://localhost:3000

Demo
Try uploading a logo or sketch. The app will:
- Send the image to the backend
- Vectorize via Hugging Face’s StarVector API
- Return a clean, scalable SVG preview
- Let you download it with one click

Development Notes
- You can swap in svgtrace or other local converters as fallback
- Uses GraphQL Upload scalar for file input
- Backend supports both async & thread-pooled calls

Contributing
Feel free to fork, improve, and open pull requests! Suggestions for better vectorization logic or UI polish are always welcome.

