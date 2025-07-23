## Skin Cancer Detection Backend

This backend application provides secure API endpoints for a skin lesion classification system. It includes user authentication, lesion analysis via ensemble Keras models, and report storage using MongoDB.

---

### Project Structure

```
backend/
├── config/                         # Environment configuration loading
│   └── config.py
├── detection/                      # Image preprocessing & mask conversion tools
│   ├── data/
│   └── processing/
├── internal/                       # Application logic and helpers
│   ├── database/                   # MongoDB access logic
│   ├── email/                      # SMTP mailer and verification code storage
│   ├── exception/                  # Custom exception handling
│   ├── models/                     # Pydantic request/response models
│   ├── tokens/                     # JWT token creation and validation
│   └── utils/                      # Password hashing, logger, response templates
├── models/                         # Trained Keras model folders (used in ensemble_pipeline.py)
│   └── README.md                   # Instructions for model file structure
├── routes/                         # FastAPI routers for all HTTP endpoints
│   ├── auth_controller.py
│   ├── detection.py
│   └── report_controller.py
├── static/                         # Frontend assets (e.g., reset-password.html)
├── temp/                           # Temporary uploaded image storage
├── .env                            # Environment variables
├── Dockerfile                      # (Optional) Docker container setup
├── main.py                         # FastAPI application entry point
└── requirements.txt                # Python dependencies
```

---

### Tech Stack

- FastAPI
- MongoDB + Motor
- Keras (TensorFlow backend)
- JWT (access/refresh tokens)
- Pydantic
- SMTP email integration
- Pillow (image processing)
- bcrypt (password hashing)

---

### Key Endpoints

- POST /api/auth/signup
- POST /api/auth/login
- POST /detect
- POST /api/reports/upload
- GET /api/reports/me
- POST /api/auth/refresh-token
- POST /api/auth/request-password-reset
- POST /api/auth/reset-password

---

### Setup Instructions

1. Clone the repo
2. Set up your `.env` file
3. Install dependencies:  
   `pip install -r requirements.txt`
4. Run the server:  
   `uvicorn main:app --reload`
5. Open docs:  
   `http://localhost:8000/docs`

---

### Model Files

Models are not included by default. You must train and place them under `models/` in folders such as:

- `melanoma_models/`: Binary models trained to detect melanoma.
- `nevus_models/`: Binary models trained to detect nevus.
- `binary_models/`: Binary models for general benign vs malignant classification.
- `malignant_models/`: Multi-class models for malignant subtypes (AKIEC, BCC).
- `benign_models/`: Multi-class models for benign subtypes (BKL, DF, VASC).

Refer to `models/README.md` for full details.

---

### Notes

- `/detect` currently returns mock output unless models are added.
- `detection.py` supports full model-based classification.
- JWT-secured access for all user endpoints.
