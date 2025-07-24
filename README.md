# 🧠 Skin Cancer Detection App

An AI-powered Flutter application that helps users detect early signs of skin cancer using deep learning models. This app allows image classification, diagnosis reports, PDF exports, and personalized skincare tips — all in one mobile experience.

---

## 📱 Screenshots

### 👋 Onboarding Flow

<img src="screenshots/Screenshot_1.png" width="250"/> <img src="screenshots/Screenshot_2.png" width="250"/> <img src="screenshots/Screenshot_3.png" width="250"/>  
<img src="screenshots/Screenshot_4.png" width="250"/> <img src="screenshots/Screenshot_5.png" width="250"/> <img src="screenshots/Screenshot_6.png" width="250"/>

---

### 🔐 Authentication

<img src="screenshots/Screenshot_7.png" width="270"/>

---

### 🧪 Prediction Result

<img src="screenshots/Screenshot_9.jpg" width="270"/>

---

### 📊 Saved Reports

<img src="screenshots/Screenshot_11.jpg" width="270"/>
<img src="screenshots/Screenshot_8.jpg" width="270"/>

---

### 🏠 Home Page

<img src="screenshots/Screenshot_10.jpg" width="270"/>

---

## 🧩 Tech Stack

- **Frontend:** Flutter (Dart)
- **Backend:** FastAPI (Python)
- **Modeling:** Keras (TensorFlow), YOLO (for mask handling)
- **Database:** MongoDB (via Motor)
- **Authentication:** JWT, Google Sign-In
- **Extras:** PDF generation, Email verification, Docker support

---

## 📂 Folder Structure (Frontend)

```
lib/
├── app/              # Routing
├── assets/           # Fonts and images
├── core/             # Theme & utilities
├── models/           # Dart models
├── screens/          # UI screens by feature
├── services/         # API interaction
├── widgets/          # Reusable components
└── main.dart         # App entry
```

---

## 🧠 Model Overview (Backend)

> Ensemble-based image classification pipeline using:

- Melanoma detection (3 models)
- Nevus classification
- Benign vs Malignant
- Subtype diagnosis (AKIEC, BCC, etc.)

Models are stored under:

```
/models/
├── melanoma_models/
├── nevus_models/
├── binary_models/
├── malignant_models/
└── benign_models/
```

---

## 🧪 Model Training

The deep learning models used in this project were trained using the following repository:

🔗 **[Model Training Repository](https://github.com/erenisci/skin-cancer-detection)**

---

## 🚀 Getting Started

### Backend (FastAPI)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Flutter)

```bash
cd frontend
flutter pub get
flutter run
```

---

## 📦 API

- `POST /auth/login`
- `POST /auth/signup`
- `POST /detect` → returns diagnosis
- `POST /report` → save report
- `GET /report/me` → user’s history

---

## 📌 Features

- [x] AI-driven image classification
- [x] PDF report generation
- [x] Email + Google login
- [x] Onboarding, tips, dashboard
- [x] MongoDB storage

---

## 👥 Contributors

- [@erenisci](https://github.com/erenisci)
- [@zscengiz](https://github.com/zscengiz)
- [@MeldaErylmz](https://github.com/MeldaErylmz)

---

## 🧠 Disclaimer

All medical advice in this app is for **educational purposes only**.  
For any diagnosis or treatment, consult a certified medical professional.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
