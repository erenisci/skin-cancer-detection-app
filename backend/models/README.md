# Models Directory

Place the 15 trained `.keras` files here following the exact folder and file names below.
The backend auto-detects their presence and switches from dummy mode to real inference.

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

> Note: Some file names differ intentionally from the standard `_finetuned` pattern:
>
> - `melanoma_models/cnn_model.keras` (not `cnn_finetuned`)
> - `malignant_models/xception_model.keras` (not `xception_finetuned`)
> - `benign_models/densenet_model.keras` (not `densenet_finetuned`)
>
> These names must match exactly — the pipeline in `routes/detection.py` loads them by path.

## Activating Real Inference

Once all 15 files are present, open `backend/routes/detection.py` and follow the
`# --- TO ACTIVATE REAL PIPELINE ---` instructions in the comments:

1. Uncomment the TensorFlow/numpy/asyncio imports at the top.
2. Uncomment the `load_and_preprocess_image`, `predict_binary_ensemble`, and `classify_image` functions.
3. In the `/detect` endpoint, replace the `if True:` dummy block with the commented-out real pipeline block.

The model training repository is available at:
[https://github.com/erenisci/skin-cancer-detection](https://github.com/erenisci/skin-cancer-detection)
