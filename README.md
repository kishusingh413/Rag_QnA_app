# Document Management and RAG-based Q&A System

This project is a **Flask-based backend** for a **Document Management and Retrieval-Augmented Generation (RAG) Q&A system**. Users can upload documents (DOCX, PDF), manage them, and ask questions based on the document content using AI-powered retrieval and embeddings.

## 🚀 Features
- **User Authentication** (Registration & Login)
- **Document Upload & Management**
- **Retrieval-Augmented Question Answering (RAG)**
- **Embedding Generation for Efficient Retrieval**
- **PostgreSQL Database Integration**
- **Asynchronous Processing for Optimization**

## 🛠️ Technologies Used
- **Backend:** Flask, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy
- **Database:** PostgreSQL
- **Embedding & Retrieval:** OpenAI API for embeddings
- **Containerization:** Docker, Docker Compose
- **Web Server:** Gunicorn
- **Authentication:** JWT-based authentication

---

## 📌 Installation & Setup

### 1️⃣ Prerequisites
- Install **Docker** and **Docker Compose**
- OpenAI API Key (for embeddings)
- PostgreSQL Database Credentials

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/kishusingh413/Rag_QnA_app.git
cd Rag_QnA_app
```

### 3️⃣ Setup Environment Variables
Create a `.env` file and configure your credentials:
```env
DATABASE_URL=postgresql://user:password@db:5432/mydatabase
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
OPENAI_API_KEY=your_openai_api_key
```

### 4️⃣ Build and Run the Containers
```sh
docker-compose up --build -d
```

### 5️⃣ Apply Database Migrations
```sh
docker exec -it backend flask db upgrade
```

---

## 🔑 API Endpoints

### 🏠 Authentication
| Method | Endpoint          | Description         |
|--------|------------------|---------------------|
| POST   | `/register`       | User Registration  |
| POST   | `/login`          | User Login         |

### 📂 Document Management
| Method | Endpoint          | Description         |
|--------|------------------|---------------------|
| POST   | `/upload`         | Upload a Document  |
| GET    | `/documents`      | List Uploaded Docs |
| DELETE | `/documents/{id}` | Delete a Document  |

### ❓ Question Answering
| Method | Endpoint   | Description                     |
|--------|-----------|---------------------------------|
| POST   | `/ask`    | Ask a question on a document   |

---

## 📜 License
This project is licensed under the MIT License.

---

## 🤝 Contributing
Feel free to open issues and pull requests to improve the system!

---

## 📧 Contact
For any inquiries, reach out to **singhkishu341@gmail.com**.

