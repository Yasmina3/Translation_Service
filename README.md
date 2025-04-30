# Translation_Service
Absolutely! Here's a **fully copy-paste ready `README.md` section**. Just paste it into your `.md` file — it’s markdown-formatted, clean, and professional:

---

```markdown
# 🚀 How to Run the Translation Microservice

This microservice listens to Kafka messages requesting title translations (EN ➝ ES), calls the Gemini API, and returns the translated title via Kafka.

---

## ✅ Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Gemini API Key (from [Google MakerSuite](https://makersuite.google.com/app))

---

## 📁 Project Structure

```
translation-service/
├── translation_worker.py         # Main service (Kafka consumer/producer)
├── gemini_api.py                 # Gemini API logic
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Kafka + Zookeeper setup
├── .venv/                        # Python virtual environment (after setup)
```

---

## 🛠️ 1. Python Environment Setup

```bash
cd translation-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Make sure `requirements.txt` contains:

```
fastapi==0.109.0
uvicorn==0.25.0
aiokafka==0.8.1
httpx==0.25.0
```

---

## 🔑 2. Export the Gemini API Key

```bash
export GEMINI_API_KEY="your_real_gemini_api_key_here"
```

---

## 🐳 3. Start Kafka and Zookeeper

```bash
docker-compose up -d
```

Verify:

```bash
docker ps
```

✅ You should see containers `kafka` and `zookeeper` running.

---

## 🧠 4. Start the Translation Service

In a new terminal:

```bash
cd translation-service
source .venv/bin/activate
export GEMINI_API_KEY="your_real_gemini_api_key_here"
python3 translation_worker.py
```

Expected log:

```
INFO:TranslationService:Subscribed to topic: translation_requests
```

---

## 🧪 5. Test the Service

### 📤 A. Send a Translation Request

```bash
docker exec -it kafka bash
kafka-console-producer --topic translation_requests --bootstrap-server localhost:9092
```

Paste:

```json
{"document_id": 101, "title_en": "Welcome to the document system"}
```

Press Enter.

---

### 📥 B. Receive the Translated Response

Still inside Kafka container:

```bash
kafka-console-consumer --topic translation_responses --from-beginning --bootstrap-server localhost:9092
```

Expected output:

```json
{"document_id": 101, "title_es": "Bienvenido al sistema de documentos"}
```

---

## 🔁 Restart Checklist (Every Session)

```bash
cd translation-service
source .venv/bin/activate
export GEMINI_API_KEY="your_real_gemini_api_key_here"
docker-compose up -d
python3 translation_worker.py
```

---

## 🧹 Troubleshooting

| Problem                           | Solution                                        |
|----------------------------------|-------------------------------------------------|
| Port 9092 already in use         | `sudo lsof -i :9092` then `sudo kill -9 <PID>`  |
| LEADER_NOT_AVAILABLE warning     | Wait 5s or send a message to create the topic   |
| Unicode characters escaped (`\u`) | Output is valid — decode or use `.strip()`     |
