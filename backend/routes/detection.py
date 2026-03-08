import os
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

# --- Ensemble pipeline imports (uncomment when model files are ready) ---
# import asyncio
# import numpy as np
# from tensorflow.keras import backend as K
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# --- End ensemble pipeline imports ---

router = APIRouter()

IMG_SIZE = 224
MODEL_DIR = "models"

_REQUIRED_MODELS = [
    "melanoma_models/xception_finetuned.keras",
    "melanoma_models/densenet_finetuned.keras",
    "melanoma_models/cnn_model.keras",
    "nevus_models/xception_finetuned.keras",
    "nevus_models/densenet_finetuned.keras",
    "nevus_models/cnn_finetuned.keras",
    "binary_models/xception_finetuned.keras",
    "binary_models/densenet_finetuned.keras",
    "binary_models/cnn_finetuned.keras",
    "malignant_models/xception_model.keras",
    "malignant_models/densenet_finetuned.keras",
    "malignant_models/cnn_finetuned.keras",
    "benign_models/xception_finetuned.keras",
    "benign_models/densenet_model.keras",
    "benign_models/cnn_finetuned.keras",
]

MODELS_AVAILABLE = all(
    os.path.exists(os.path.join(MODEL_DIR, m)) for m in _REQUIRED_MODELS
)

# --- Ensemble pipeline functions ---
# To enable real inference: place model files under backend/models/,
# uncomment the functions below, and swap the dummy block in the endpoint.
#
# def load_and_preprocess_image(img_path):
#     img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0) / 255.0
#     return img_array
#
#
# def predict_binary_ensemble(img_tensor, model_paths, weights):
#     preds = []
#     for path in model_paths:
#         K.clear_session()
#         model = load_model(path)
#         preds.append(model.predict(img_tensor, verbose=0)[0][0])
#         del model
#     return np.average(preds, weights=weights)
#
#
# def classify_image(image_path):
#     img_tensor = load_and_preprocess_image(image_path)
#
#     melanoma_models = [
#         os.path.join(MODEL_DIR, "melanoma_models/xception_finetuned.keras"),
#         os.path.join(MODEL_DIR, "melanoma_models/densenet_finetuned.keras"),
#         os.path.join(MODEL_DIR, "melanoma_models/cnn_model.keras")
#     ]
#     mel_score = predict_binary_ensemble(img_tensor, melanoma_models, [0.4, 0.3, 0.3])
#     if mel_score > 0.5:
#         return {
#             "predicted_class": "mel",
#             "confidence": round(float(mel_score), 4),
#             "alternatives": {
#                 "mel": round(float(mel_score), 4),
#                 "not_mel": round(1 - float(mel_score), 4)
#             }
#         }
#
#     nevus_models = [
#         os.path.join(MODEL_DIR, "nevus_models/xception_finetuned.keras"),
#         os.path.join(MODEL_DIR, "nevus_models/densenet_finetuned.keras"),
#         os.path.join(MODEL_DIR, "nevus_models/cnn_finetuned.keras")
#     ]
#     nevus_score = predict_binary_ensemble(img_tensor, nevus_models, [0.35, 0.55, 0.1])
#     if nevus_score < 0.5:
#         return {
#             "predicted_class": "nv",
#             "confidence": round(1 - float(nevus_score), 4),
#             "alternatives": {
#                 "nv": round(1 - float(nevus_score), 4),
#                 "not_nv": round(float(nevus_score), 4)
#             }
#         }
#
#     binary_models = [
#         os.path.join(MODEL_DIR, "binary_models/xception_finetuned.keras"),
#         os.path.join(MODEL_DIR, "binary_models/densenet_finetuned.keras"),
#         os.path.join(MODEL_DIR, "binary_models/cnn_finetuned.keras")
#     ]
#     binary_score = predict_binary_ensemble(img_tensor, binary_models, [0.3, 0.3, 0.4])
#     is_malignant = binary_score > 0.5
#
#     if is_malignant:
#         malignant_models = [
#             os.path.join(MODEL_DIR, "malignant_models/xception_model.keras"),
#             os.path.join(MODEL_DIR, "malignant_models/densenet_finetuned.keras"),
#             os.path.join(MODEL_DIR, "malignant_models/cnn_finetuned.keras")
#         ]
#         classes = ['akiec', 'bcc']
#         preds = []
#         for path in malignant_models:
#             K.clear_session()
#             model = load_model(path)
#             preds.append(model.predict(img_tensor, verbose=0)[0])
#             del model
#         final_probs = np.average(preds, axis=0, weights=[0.2, 0.4, 0.4])
#         pred_idx = np.argmax(final_probs)
#         return {
#             "predicted_class": classes[pred_idx],
#             "confidence": round(float(final_probs[pred_idx]), 4),
#             "alternatives": {cls: round(float(prob), 4) for cls, prob in zip(classes, final_probs)}
#         }
#     else:
#         benign_models = [
#             os.path.join(MODEL_DIR, "benign_models/xception_finetuned.keras"),
#             os.path.join(MODEL_DIR, "benign_models/densenet_model.keras"),
#             os.path.join(MODEL_DIR, "benign_models/cnn_finetuned.keras")
#         ]
#         classes = ['bkl', 'df', 'vasc']
#         preds = []
#         for path in benign_models:
#             K.clear_session()
#             model = load_model(path)
#             preds.append(model.predict(img_tensor, verbose=0)[0])
#             del model
#         final_probs = np.average(preds, axis=0, weights=[0.2, 0.6, 0.2])
#         pred_idx = np.argmax(final_probs)
#         return {
#             "predicted_class": classes[pred_idx],
#             "confidence": round(float(final_probs[pred_idx]), 4),
#             "alternatives": {cls: round(float(prob), 4) for cls, prob in zip(classes, final_probs)}
#         }
# --- End ensemble pipeline functions ---

# Create temp directory
os.makedirs("temp", exist_ok=True)

# Class label metadata
CLASS_DETAILS = {
    'MEL': {
        'full_label': 'Melanoma',
        'risk_level': 'High risk',
        'advice': 'Consult a dermatologist immediately. Melanoma can be aggressive and requires urgent attention.'
    },
    'NV': {
        'full_label': 'Melanocytic Nevus',
        'risk_level': 'Low risk',
        'advice': 'No intervention required. Monitor periodically for changes.'
    },
    'BCC': {
        'full_label': 'Basal Cell Carcinoma',
        'risk_level': 'Moderate risk',
        'advice': 'Consult a dermatologist for evaluation. Early treatment is usually effective.'
    },
    'AKIEC': {
        'full_label': 'Actinic Keratoses / Intraepithelial Carcinoma',
        'risk_level': 'High risk',
        'advice': 'Requires medical assessment and possible biopsy to determine cancer risk.'
    },
    'BKL': {
        'full_label': 'Benign Keratosis',
        'risk_level': 'Low risk',
        'advice': 'Generally harmless. Cosmetic removal can be considered.'
    },
    'DF': {
        'full_label': 'Dermatofibroma',
        'risk_level': 'Low risk',
        'advice': 'Harmless fibrous lesion. No treatment necessary unless symptomatic.'
    },
    'VASC': {
        'full_label': 'Vascular Lesion',
        'risk_level': 'Low to moderate risk',
        'advice': 'Consult a dermatologist for cosmetic or vascular concerns.'
    }
}


@router.post("/detect")
async def detect_lesion(file: UploadFile = File(...)):
    temp_path = Path(f"temp/{uuid.uuid4()}.jpg")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # --- Real pipeline block (uncomment when models are ready, disable dummy block) ---
        # if MODELS_AVAILABLE:
        #     result = await asyncio.to_thread(classify_image, str(temp_path))
        #     predicted = result["predicted_class"].upper()
        #     class_details = CLASS_DETAILS.get(predicted, {})
        #     predictions = [
        #         {"class": predicted, "confidence": result["confidence"]}
        #     ] + [
        #         {"class": cls.upper(), "confidence": conf}
        #         for cls, conf in result["alternatives"].items()
        #         if cls.upper() != predicted
        #     ]
        # else:
        # --- End real pipeline block ---

        # Dummy response — model files not yet available
        if True:
            predicted = "BCC"
            class_details = CLASS_DETAILS.get(predicted, {})
            predictions = [
                {"class": "BCC",   "confidence": 0.8721},
                {"class": "AKIEC", "confidence": 0.0341},
                {"class": "NV",    "confidence": 0.0124},
                {"class": "MEL",   "confidence": 0.0814},
            ]

        return {
            "predictions": predictions,
            "class_details": class_details,
            "model_used": "ensemble" if MODELS_AVAILABLE else "dummy",
        }
    finally:
        if temp_path.exists():
            temp_path.unlink()
