## Skin Cancer Detection Backend

This backend provides secure API endpoints for a skin lesion tracking system. It includes user authentication, image upload handling, PDF report storage, and an ensemble Keras inference pipeline that activates automatically when model files are placed in `backend/models/` (not included in this repository).

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
│   └── utils/                      # Logger, response templates
├── models/                         # Trained Keras model folders (see models/README.md)
│   ├── melanoma_models/
│   ├── nevus_models/
│   ├── binary_models/
│   ├── malignant_models/
│   └── benign_models/
├── routes/                         # FastAPI routers
│   ├── auth_controller.py
│   ├── detection.py
│   └── report_controller.py
├── static/                         # Static files (e.g., reset-password.html)
├── temp/                           # Temporary uploaded image storage (auto-cleaned)
├── ensemble_pipeline.py            # Standalone ensemble pipeline reference
├── .env                            # Environment variables
├── main.py                         # FastAPI application entry point
└── requirements.txt                # Python dependencies
```

---

### Tech Stack

- FastAPI
- MongoDB + Motor (async)
- TensorFlow / Keras (ensemble inference — model files not included, see `models/README.md`)
- JWT (access + refresh tokens)
- Pydantic
- SMTP email integration
- bcrypt (password hashing)

---

### Key Endpoints

| Method | Endpoint                              | Auth     | Description                        |
|--------|---------------------------------------|----------|------------------------------------|
| POST   | `/api/auth/signup`                    | No       | Register a new user                |
| POST   | `/api/auth/login`                     | No       | Login and receive tokens           |
| POST   | `/api/auth/refresh-token`             | No       | Exchange refresh token             |
| POST   | `/api/auth/request-password-reset`    | No       | Send password reset email          |
| POST   | `/api/auth/reset-password`            | No       | Reset password with token          |
| POST   | `/api/auth/update-profile`            | JWT      | Update name, surname, email        |
| POST   | `/api/auth/change-password`           | JWT      | Change password                    |
| POST   | `/api/auth/logout`                    | No       | Invalidate tokens                  |
| POST   | `/detect`                             | No       | Upload image for classification    |
| POST   | `/api/reports/upload`                 | JWT      | Save detection report              |
| GET    | `/api/reports/me`                     | JWT      | Fetch user's reports               |
| GET    | `/api/reports/pdf/{id}`               | JWT      | Download PDF report                |
| GET    | `/api/reports/image/{id}`             | JWT      | Download report image              |

---

### Setup Instructions

1. Clone the repository
2. Create and configure your `.env` file (see `.env` for required variables)
3. Start MongoDB:
   ```bash
   "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   "C:\Program Files\Python312\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
6. Open Swagger docs:
   `http://localhost:8000/docs`

---

### Environment Variables (`.env`)

| Variable                    | Default              | Description                          |
|-----------------------------|----------------------|--------------------------------------|
| `MONGODB_HOST`              | `localhost:27017`    | MongoDB host                         |
| `MONGODB_DATABASE`          | `skincancer`         | Database name                        |
| `MONGODB_USERNAME`          | —                    | MongoDB user (optional)              |
| `MONGODB_PASSWORD`          | —                    | MongoDB password (optional)          |
| `SECRET_KEY`                | `super-secret-key`   | JWT signing key                      |
| `ALGORITHM`                 | `HS256`              | JWT algorithm                        |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15`               | Access token TTL in minutes          |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7`                  | Refresh token TTL in days            |
| `SMTP_HOST`                 | `smtp.mailtrap.io`   | SMTP server host                     |
| `SMTP_PORT`                 | `587`                | SMTP server port                     |
| `SMTP_USER`                 | —                    | SMTP username                        |
| `SMTP_PASS`                 | —                    | SMTP password                        |
| `BASE_URL`                  | `http://localhost:8000` | Base URL for password reset links |

---

### Model Files

Models are not included in the repository. Place trained `.keras` files under `models/` using the following structure:

```
models/
├── melanoma_models/
│   ├── xception_finetuned.keras
│   ├── densenet_finetuned.keras
│   └── cnn_model.keras
├── nevus_models/
│   ├── xception_finetuned.keras
│   ├── densenet_finetuned.keras
│   └── cnn_finetuned.keras
├── binary_models/
│   ├── xception_finetuned.keras
│   ├── densenet_finetuned.keras
│   └── cnn_finetuned.keras
├── malignant_models/
│   ├── xception_model.keras
│   ├── densenet_finetuned.keras
│   └── cnn_finetuned.keras
└── benign_models/
    ├── xception_finetuned.keras
    ├── densenet_model.keras
    └── cnn_finetuned.keras
```

Once all 15 model files are present, the backend auto-detects them and activates real inference. See `routes/detection.py` for instructions on switching from dummy to ensemble mode.

---

### Notes

- `/detect` returns dummy output by default when model files are missing.
- The ensemble pipeline code is preserved as comments in `routes/detection.py` for easy activation.
- All user-facing endpoints are JWT-secured.
