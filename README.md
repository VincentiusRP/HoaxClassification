# Hoax Title Classifier (IndoBERT) — Flask App

## 1. Export model dari Google Colab

Di notebook Colab, setelah training selesai (model `indo_model` dan `indo_tokenizer`), jalankan:

```python
indo_model.save_pretrained("indo_hoax_model")
indo_tokenizer.save_pretrained("indo_hoax_model")

# zip lalu download
import shutil
shutil.make_archive("indo_hoax_model", "zip", "indo_hoax_model")

from google.colab import files
files.download("indo_hoax_model.zip")
```

## 2. Pindah ke VSCode (lokal)

1. Install Python 3.10+ dan VSCode (extension Python).
2. Extract project zip ini (hoax_app), lalu extract `indo_hoax_model.zip` hasil dari Colab ke dalam folder `hoax_app/model/` sehingga isinya:

```
hoax_app/
├── app.py
├── requirements.txt
├── model/
│   ├── config.json
│   ├── model.safetensors (atau pytorch_model.bin)
│   ├── tokenizer_config.json
│   ├── vocab.txt
│   └── special_tokens_map.json
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

3. Buat virtual environment (opsional tapi disarankan):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

> Jika tidak punya GPU, pip akan install torch versi CPU — tetap berfungsi normal, hanya lebih lambat sedikit.

## 3. Jalankan App

```bash
python app.py
```

Buka browser ke: http://127.0.0.1:5000

## Catatan
- Label: 0 = Non-Hoax (Valid), 1 = Hoax (sesuai mapping training di notebook).
- Input dipotong/padding ke max_length=64 token, sama seperti saat training.
- Model yang digunakan: IndoBERT (`indobenchmark/indobert-base-p1`) karena akurasinya lebih tinggi (92.6%) dibanding BERT multilingual (90.4%).
