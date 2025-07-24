## Skin Cancer Detection App (Flutter Frontend)

This is the Flutter-based mobile and web frontend for the Skin Cancer Detection system. It connects to a FastAPI backend to handle user authentication, image upload, classification, and report management.

---

### Project Structure

```
frontend/
├── android/                    # Android platform config
├── ios/                        # iOS platform config
├── assets/                     # Static assets (fonts, images, etc.)
│   ├── fonts/
│   └── images/
├── lib/                        # Main Flutter application
│   ├── app/                    # App-wide routing and navigation
│   ├── assets/                 # Asset helpers
│   ├── core/                   # Shared logic (theme, utils, constants)
│   ├── models/                 # Dart data models
│   ├── screens/                # All UI screens (feature-based)
│   │   ├── auth/               # Authentication (login/signup/reset)
│   │   ├── home/               # Home screen
│   │   ├── onboarding/         # Intro/tutorial screens
│   │   ├── profile/            # User profile
│   │   ├── reports/            # Report list and PDF viewer
│   │   ├── scan/               # Camera and result display
│   │   ├── settings/           # User preferences
│   │   ├── theme/              # Theme toggling
│   │   └── welcome/            # Landing/welcome screen
│   ├── services/               # API service layer
│   ├── widgets/                # Reusable UI components
│   └── main.dart               # App entry point
├── test/                       # Widget & unit tests
├── web/                        # Web platform files (icons, index.html)
├── .env                        # Optional: environment variables
├── pubspec.yaml                # Flutter dependencies and assets
├── README.md                   # This file
└── .gitignore, analysis_options.yaml, etc.
```

---

### Features

- User registration, login, and password reset (with backend)
- Upload lesion images for classification
- View predictions and risk levels (mock or real)
- Access previous reports and download PDFs
- Supports light and dark theme
- Mobile and web responsive design

---

### Setup Instructions

1. Install Flutter SDK → https://docs.flutter.dev/get-started/install
2. Run:

```bash
flutter pub get
flutter run
```

> To run in Chrome:

```bash
flutter run -d chrome
```

---

### API Configuration

The app connects to a FastAPI backend.

Set your base URL in `.env` or inside your API service:

```dart
const baseUrl = "http://10.0.2.2:8000"; // Android emulator
```

---

### Testing

To run tests:

```bash
flutter test
```

---

### Notes

- The `/detect` endpoint returns dummy data unless real models are added.
- Make sure the backend is running before using authentication or prediction features.
- Models and backend structure: see `../backend/README.md`
