# AI Agent Assessment – Groq API Integration

## Overview

This project showcases communication between a Frontend Agent and a Backend Agent in a simple AI-powered workflow.

The user submits a task through the frontend, the backend asks follow-up questions for clarification, and finally generates AI-based content using the Groq API.

---

## Tech Stack

### Frontend

* React
* Axios

### Backend

* FastAPI
* Groq API

---

## Features

* Frontend and Backend agent communication
* Multi-step conversational workflow
* AI-generated responses using Groq
* Interactive chat-style UI
* FastAPI-based backend server

---

## Setup Instructions

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend server runs on:

```txt
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend application runs on:

```txt
http://localhost:5173
```
