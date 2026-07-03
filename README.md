# BuddyLearnAI

> An AI-powered personalized learning platform that transforms course materials into interactive study experiences.

BuddyLearnAI helps students study smarter by allowing them to upload lecture notes, textbooks, slides, and past examination papers. The platform uses Artificial Intelligence to generate quizzes, flashcards, structured study guides, personalized recommendations, and exam insights based on the student's own learning materials.

---

# 🌟 Features

## 📚 Smart Document Processing
- Upload PDF lecture notes
- Upload PowerPoint presentations
- Upload Word documents
- Upload scanned notes (OCR support)
- Organize materials by course

---

## 🧠 AI Study Guide Generator

Transform lengthy lecture notes into:

- Chapter summaries
- Key concepts
- Important definitions
- Formulas
- Examples
- Common mistakes
- Exam tips

---

## ❓ AI Quiz Generator

Generate quizzes from uploaded materials.

Supported question types:

- Multiple Choice Questions (MCQs)
- True/False
- Fill in the blanks
- Short answer
- Essay questions

Difficulty levels:

- Easy
- Medium
- Hard
- Mixed

---

## 🗂 Flashcard Generator

Automatically create study flashcards.

Example:

**Front**

> What is Dynamic Programming?

**Back**

> A programming technique that solves complex problems by breaking them into overlapping subproblems and storing intermediate results.

---

## 💬 AI Study Assistant

Students can ask questions about their uploaded materials.

Examples:

- Explain Chapter 4.
- Summarize this lecture.
- What is recursion?
- Give me examples of AVL Trees.
- Compare TCP and UDP.

Responses are generated using the student's own learning materials rather than generic internet information.

---

## 📊 Past Examination Analysis

Upload previous examination papers and let AI discover patterns such as:

- Frequently tested topics
- Chapters with the highest exam weight
- Question trends
- Difficulty distribution
- Topic frequency over multiple years

Example:

| Topic | Frequency |
|--------|-----------|
| Graph Algorithms | 34% |
| Trees | 26% |
| Searching | 15% |
| Sorting | 13% |
| Hash Tables | 12% |

---

## 🎯 Personalized Learning Recommendations

The platform combines:

- Quiz performance
- Past exam trends
- Uploaded materials
- Student progress

to recommend:

- Topics to review
- Chapters to prioritize
- Practice quizzes
- Weak concepts
- Daily study plans

---

## 📈 Progress Dashboard

Track learning with:

- Quiz scores
- Study streaks
- Topics mastered
- Weak areas
- Learning history
- Exam readiness score

---

# 🏗 System Architecture

```text
                        Client
                          │
                          ▼
                     FastAPI Server
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
 Authentication      Database           AI Engine
       │                  │                  │
       ▼                  ▼                  ▼
 PostgreSQL         File Storage      OpenAI API
                          │
                          ▼
                 Document Processing
                          │
          OCR → Extraction → Chunking
                          │
                          ▼
                    Vector Database
                          │
                          ▼
                      RAG Pipeline
                          │
     ┌──────────┬──────────┬──────────┬─────────┐
     ▼          ▼          ▼          ▼
 Study Guide  Quiz     Flashcards   AI Tutor
                          │
                          ▼
                 Exam Pattern Analyzer
                          │
                          ▼
                Recommendation Engine
```

---

# 🛠 Technology Stack

## Backend

- FastAPI
- Python 3.13+
- SQLAlchemy
- Alembic
- Pydantic

## Database

- PostgreSQL

## AI

- OpenAI API
- Retrieval-Augmented Generation (RAG)

## Vector Database

- Qdrant

## File Processing

- PyMuPDF
- pdfplumber
- Tesseract OCR (for scanned documents)

## Background Tasks

- Celery
- Redis

## Storage

- MinIO (Development)
- AWS S3 (Production)

---

# 📂 Project Structure

```text
learning-buddy/

│── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   ├── prompts/
│   ├── repositories/
│   ├── utils/
│   └── main.py
│
│── uploads/
│── vector_store/
│── tests/
│── requirements.txt
│── docker-compose.yml
│── README.md
```

---

# 🚀 Planned AI Pipeline

```text
Student Uploads Material
          │
          ▼
 Store Document
          │
          ▼
 Extract Text
          │
          ▼
 Clean Text
          │
          ▼
 Split into Chunks
          │
          ▼
 Generate Embeddings
          │
          ▼
 Store in Vector Database
          │
          ▼
 User Requests AI Feature
          │
          ▼
 Retrieve Relevant Context
          │
          ▼
 Generate AI Response
          │
          ▼
 Return Structured Output
```

---

# 🎯 Project Goals

Our mission is to build an intelligent learning companion that helps students:

- Study more efficiently
- Understand concepts faster
- Practice with personalized quizzes
- Focus on high-impact topics
- Improve exam performance
- Receive actionable learning recommendations

Rather than replacing traditional studying, AI Learning Buddy enhances it by adapting to each student's materials, performance, and learning needs.

---

# 🔮 Future Roadmap

- AI-generated mind maps
- Voice explanations
- Spaced repetition scheduling
- Collaborative study groups
- Lecturer dashboard
- Assignment feedback
- Mobile application
- Multi-language support
- Offline mode
- LMS integrations (Moodle, Canvas, Blackboard)

---

# 🤝 Contributing

Contributions are welcome!

Whether you're fixing bugs, improving documentation, designing new features, or enhancing AI prompts, your support is appreciated.

Please open an issue before submitting major changes.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Chuong Tiutiu Nyang**

Building AI-powered educational tools to make learning more personalized, engaging, and effective.