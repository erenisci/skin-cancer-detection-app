## Skin Cancer Detection App (Flutter Frontend)

This is the Flutter-based mobile frontend for the Skin Cancer Detection system. It connects to a FastAPI backend to handle user authentication, image upload, classification result display, and report management.

---

### Project Structure

```
frontend/
├── android/                    # Android platform config
├── ios/                        # iOS platform config
├── assets/                     # Images used across the app
│   └── images/
├── lib/                        # Main Flutter application
│   ├── app/                    # App-wide routing (go_router)
│   ├── assets/                 # Fonts
│   │   └── fonts/
│   ├── core/                   # Shared logic (theme, utils, constants)
│   ├── models/                 # Dart data models
│   ├── screens/                # All UI screens (feature-based)
│   │   ├── auth/               # Login, signup, forgot/reset password
│   │   ├── home/               # Home screen with UV index and tips
│   │   ├── onboarding/         # Intro/tutorial screens
│   │   ├── profile/            # User profile and editing
│   │   ├── reports/            # Report list and PDF download
│   │   ├── scan/               # Camera capture, gallery picker, detection result
│   │   ├── settings/           # Theme and preferences
│   │   └── welcome/            # Landing/welcome screen
│   ├── services/               # API service layer (api_service.dart, api_endpoints.dart)
│   ├── widgets/                # Reusable UI components
│   └── main.dart               # App entry point
├── test/                       # Widget and unit tests
├── web/                        # Web platform files
├── .env                        # Environment variables (API_URL)
├── pubspec.yaml                # Flutter dependencies and asset declarations
└── analysis_options.yaml       # Linter configuration
```

---

### Features

- User registration, login, and password reset
- Camera and gallery image capture with crop overlay
- Skin lesion classification result display (real inference when backend models are loaded, dummy mode otherwise)
- Detailed diagnosis result with confidence, risk level, and advice
- PDF report generation and sharing
- View and download past reports
- Light and dark theme support

---

### Setup Instructions

1. Install Flutter SDK → https://docs.flutter.dev/get-started/install
2. Configure `.env` with your backend URL:
   ```
   API_URL=http://<your-local-ip>:8000
   ```
3. Install dependencies and run:
   ```bash
   flutter pub get
   flutter run
   ```

To run in Chrome:
```bash
flutter run -d chrome
```

To build a debug APK:
```bash
flutter build apk --debug
```

---

### API Configuration

The app reads the backend URL from `.env` via `flutter_dotenv`:

```
API_URL=http://192.168.1.33:8000
```

If running on an Android emulator, use:
```
API_URL=http://10.0.2.2:8000
```

The phone and computer must be on the same Wi-Fi network when using a physical device.

---

### Testing

```bash
flutter test
```

To run static analysis:
```bash
flutter analyze
```

---

### Notes

- `/detect` returns dummy data unless real models are loaded in the backend.
- Make sure MongoDB and the FastAPI backend are running before launching the app.
- See `../backend/README.md` for backend setup and model integration details.
