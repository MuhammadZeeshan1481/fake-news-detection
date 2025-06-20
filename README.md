# Fake News Detection 📰🤖

A machine learning-based Fake News Detection System using BERT, FastAPI, and Streamlit. It predicts if a news headline/statement is real or fake and cross-verifies with trusted news sources.

---

##  Features

- **BERT-based Model:** Accurate fake/real news classification
- **FastAPI Backend:** Fast, modern REST API
- **Streamlit Frontend:** User-friendly web interface
- **NewsAPI Verification:** Checks matching news in trusted sources
- **SQLite Logging:** Prediction logs for analytics
- **Explainable AI (Optional):** Top influential words (attention-based)

---

##  Installation

1. **Clone the Repo**
    ```sh
    git clone https://github.com/MuhammadZeeshan1481/fake-news-detection.git
    cd fake-news-detection
    ```

2. **Create Virtual Environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Requirements**
    ```sh
    pip install -r requirements.txt
    ```

---

##  How to Run

1. **Initialize the Database (First Time Only)**
    ```sh
    python init_db.py
    ```

2. **Start the Backend (FastAPI Server)**
    ```sh
    cd backend
    uvicorn app:app --reload
    ```
    _Server will start at: http://127.0.0.1:8000_

3. **Run the Frontend (Streamlit App)**  
    Open a new terminal in the project root folder:
    ```sh
    cd frontend
    streamlit run main.py
    ```
    _App will open in your browser (usually at http://localhost:8501)_

---

##  Usage

- Enter any news headline or statement in the input box.
- Click **Check**.
- See prediction (`Real` / `Fake`), confidence, and NewsAPI verification.
- If enabled, top influential words will also display (Explainable AI).

---

##  Configuration

- **Model files:** Place BERT model and tokenizer files inside:  
  `backend/model/saved_model/`
- **API Key:** NewsAPI key is set inside `backend/app.py` (`NEWS_API_KEY = "..."`).  
  For real deployment, use `.env` file for security.

---
