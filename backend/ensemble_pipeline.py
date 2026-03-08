import os

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


IMG_SIZE = 224
model_dir = "##"


def load_and_preprocess_image(img_path):
    """Load and preprocess image to model input format."""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array


def predict_binary_ensemble(img_tensor, model_paths, weights):
    """Run binary ensemble prediction with sigmoid outputs."""
    preds = []
    for path in model_paths:
        K.clear_session()
        model = load_model(path)
        preds.append(model.predict(img_tensor, verbose=0)[0][0])
        del model
    return np.average(preds, weights=weights)


def classify_image(image_path):
    """Full pipeline for single image classification with details."""
    img_tensor = load_and_preprocess_image(image_path)

    melanoma_models = [
        os.path.join(model_dir, "melanoma_models/xception_finetuned.keras"),
        os.path.join(model_dir, "melanoma_models/densenet_finetuned.keras"),
        os.path.join(model_dir, "melanoma_models/cnn_model.keras")
    ]
    mel_score = predict_binary_ensemble(
        img_tensor, melanoma_models, [0.4, 0.3, 0.3])
    if mel_score > 0.5:
        return {
            "predicted_class": "mel",
            "confidence": round(float(mel_score), 4),
            "alternatives": {
                "mel": round(float(mel_score), 4),
                "not_mel": round(1 - float(mel_score), 4)
            }
        }

    nevus_models = [
        os.path.join(model_dir, "nevus_models/xception_finetuned.keras"),
        os.path.join(model_dir, "nevus_models/densenet_finetuned.keras"),
        os.path.join(model_dir, "nevus_models/cnn_finetuned.keras")
    ]
    nevus_score = predict_binary_ensemble(
        img_tensor, nevus_models, [0.35, 0.55, 0.1])
    if nevus_score < 0.5:
        return {
            "predicted_class": "nv",
            "confidence": round(1 - float(nevus_score), 4),
            "alternatives": {
                "nv": round(1 - float(nevus_score), 4),
                "not_nv": round(float(nevus_score), 4)
            }
        }

    binary_models = [
        os.path.join(model_dir, "binary_models/xception_finetuned.keras"),
        os.path.join(model_dir, "binary_models/densenet_finetuned.keras"),
        os.path.join(model_dir, "binary_models/cnn_finetuned.keras")
    ]
    binary_score = predict_binary_ensemble(
        img_tensor, binary_models, [0.3, 0.3, 0.4])
    is_malignant = binary_score > 0.5

    if is_malignant:
        malignant_models = [
            os.path.join(model_dir, "malignant_models/xception_model.keras"),
            os.path.join(
                model_dir, "malignant_models/densenet_finetuned.keras"),
            os.path.join(model_dir, "malignant_models/cnn_finetuned.keras")
        ]
        classes = ['akiec', 'bcc']
        preds = []
        for path in malignant_models:
            K.clear_session()
            model = load_model(path)
            preds.append(model.predict(img_tensor, verbose=0)[0])
            del model
        final_probs = np.average(preds, axis=0, weights=[0.2, 0.4, 0.4])
        pred_idx = np.argmax(final_probs)
        return {
            "predicted_class": classes[pred_idx],
            "confidence": round(float(final_probs[pred_idx]), 4),
            "alternatives": {cls: round(float(prob), 4) for cls, prob in zip(classes, final_probs)}
        }

    else:
        benign_models = [
            os.path.join(model_dir, "benign_models/xception_finetuned.keras"),
            os.path.join(model_dir, "benign_models/densenet_model.keras"),
            os.path.join(model_dir, "benign_models/cnn_finetuned.keras")
        ]
        classes = ['bkl', 'df', 'vasc']
        preds = []
        for path in benign_models:
            K.clear_session()
            model = load_model(path)
            preds.append(model.predict(img_tensor, verbose=0)[0])
            del model
        final_probs = np.average(preds, axis=0, weights=[0.2, 0.6, 0.2])
        pred_idx = np.argmax(final_probs)
        return {
            "predicted_class": classes[pred_idx],
            "confidence": round(float(final_probs[pred_idx]), 4),
            "alternatives": {cls: round(float(prob), 4) for cls, prob in zip(classes, final_probs)}
        }
