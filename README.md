# 🩺 CareFusion-AI  
### Clinical-Grade Medical Assistant powered by RAG + LLMs

CareFusion-AI is an intelligent medical assistant that leverages **Retrieval-Augmented Generation (RAG)** to deliver fast, accurate, and evidence-based responses. It integrates **Groq LLMs**, **Pinecone Vector Database**, and a sleek **Flask-based ECG-themed UI** for a seamless clinical experience.

---

## ✨ Features

- 🧠 Context-aware medical responses using RAG
- ⚡ Ultra-fast inference with Groq LLMs
- 📚 Semantic search with Pinecone Vector DB
- 💬 Conversational chatbot interface
- 🩺 ECG-style modern UI design
- ☁️ Fully deployable using AWS + Docker + CI/CD

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kanaparthi89/CareFusion-AI.git
cd CareFusion-AI

2️⃣ Create Conda Environment
conda create -n CareFusion python=3.10 -y
conda activate CareFusion
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Add API Keys

Create a .env file in the root directory:

PINECONE_API_KEY="your_pinecone_api_key"
GROQ_API_KEY="your_groq_api_key"
5️⃣ Build Vector Index (Embeddings → Pinecone)
python store_index.py

This step will:

Load medical PDF documents
Split text into chunks
Generate embeddings using HuggingFace
Store vectors in Pinecone
6️⃣ Run the Flask App
python app.py

Open in browser:

http://localhost:8080/

You will see the ECG-style medical chatbot interface.

🧠 Tech Stack
🔬 AI / RAG
Groq LLaMA-3
LangChain
HuggingFace MiniLM Embeddings
Pinecone Vector Database
⚙️ Backend
Python
Flask
🎨 Frontend
HTML5
CSS3 (ECG Pulse UI)
Bootstrap
jQuery
☁️ DevOps & Cloud
Docker
GitHub Actions
AWS EC2
AWS ECR
☁️ AWS CI/CD Deployment

This project includes a complete CI/CD pipeline using GitHub Actions and a self-hosted EC2 runner.

1️⃣ AWS Setup
Login to AWS Console
Create IAM User
Required Permissions:
AmazonEC2FullAccess
AmazonEC2ContainerRegistryFullAccess
2️⃣ Create ECR Repository

Example:

<account-id>.dkr.ecr.us-east-1.amazonaws.com/carefusion-ai
3️⃣ Launch EC2 Instance (Ubuntu)
4️⃣ Install Docker on EC2
sudo apt-get update -y
sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker ubuntu
newgrp docker
5️⃣ Configure Self-Hosted Runner

Go to:

GitHub → Repository → Settings → Actions → Runners
Add new self-hosted runner (Ubuntu)
Run the provided commands on EC2
6️⃣ Add GitHub Secrets
Secret Name	Purpose
AWS_ACCESS_KEY_ID	IAM access key
AWS_SECRET_ACCESS_KEY	IAM secret key
AWS_DEFAULT_REGION	e.g. us-east-1
ECR_REPO	ECR repository URI
PINECONE_API_KEY	Vector DB access
GROQ_API_KEY	LLM inference access
🐳 Docker Support

Build and run the container:

docker build -t carefusion-ai .
docker run -p 8080:8080 carefusion-ai
📌 Future Enhancements
🧾 EHR Integration
🗣️ Voice-based interaction
📊 Medical analytics dashboard
🔐 HIPAA-compliant security layer
⚠️ Disclaimer

This project is for research purposes only.
It is not a substitute for professional medical advice, diagnosis, or treatment.

👨‍💻 Author

Rajasekhar Kanaparthi

GitHub: https://github.com/Kanaparthi89
LinkedIn: https://linkedin.com/in/rajasekharkanaparthi