## Models Directory

This directory holds the trained Keras models used for ensemble predictions in the skin lesion classification pipeline.

### Folder Structure

Organize your models into the following subdirectories:

- `melanoma_models/`: Binary models trained to detect melanoma.
- `nevus_models/`: Binary models trained to detect nevus.
- `binary_models/`: Binary models for general benign vs malignant classification.
- `malignant_models/`: Multi-class models for malignant subtypes (AKIEC, BCC).
- `benign_models/`: Multi-class models for benign subtypes (BKL, DF, VASC).

Each folder should contain `.keras` model files compatible with `tf.keras.models.load_model()`.

### Naming Convention

Ensure model files are clearly named, for example:

- `xception_finetuned.keras`
- `densenet_finetuned.keras`
- `cnn_finetuned.keras`

- `xception_model.keras`
- `densenet_model.keras`
- `cnn_model.keras`

### Note

This folder is currently empty. Once trained models are placed in the appropriate subdirectories, the `ensemble_pipeline.py` will be able to perform actual predictions.

---

> This file exists to ensure the directory is tracked by version control (Git).
