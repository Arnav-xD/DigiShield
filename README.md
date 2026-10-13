# DigiShield

A real-time speech transcription and scam-risk scoring project built with **Python, faster-whisper, multilingual DistilBERT, and Streamlit**.

The app captures microphone or system audio, transcribes it, and displays a risk level, model scores, flagged phrases, and recent transcripts.

## How it works

1. An audio worker captures mono audio at 16 kHz.
2. Audio chunks pass through a queue to a transcription worker.
3. The worker buffers roughly three seconds of audio and skips low-energy buffers.
4. The Whisper `small` model transcribes English speech with voice-activity filtering.
5. A fine-tuned `distilbert-base-multilingual-cased` classifier scores the transcript.
6. The scorer averages the latest five predictions and returns the risk level.
7. The Streamlit dashboard receives results through a second queue.

| Smoothed score | Risk label |
| --- | --- |
| Below 0.50 | LOW |
| 0.50 to below 0.60 | MEDIUM |
| 0.60 or higher | HIGH |

Keyword matching also returns phrases such as `digital arrest` and `transfer money`. The keyword-based risk override is commented out in the current scorer.

## Run locally

From the repository directory, install the libraries used by the app and training code:

```bash
python -m pip install streamlit numpy pandas torch transformers datasets accelerate faster-whisper soundcard sounddevice
```

Train the classifier before starting the dashboard:

```bash
python train_model.py
python -m streamlit run app.py
```

`train_model.py` uses `your_dataset.csv`, trains for three epochs, and writes the model and tokenizer to `model_artifacts/bert_finetuned/`. These trained artifacts are not included in the repository. Initial model loading needs access to the pretrained models.

The CSV must contain `text` or `transcript`, plus `label`: `0` for not-scam and `1` for scam. The training code oversamples the minority class when the imbalance ratio exceeds 5.

The dashboard selects CUDA/float16 when available and CPU/int8 otherwise. Audio capture uses devices on the machine running Python; system loopback depends on the local audio backend.

## Read the code

| File | Role |
| --- | --- |
| [app.py](app.py) | Dashboard, model loading, audio/transcription workers, and transcript history |
| [nlp_scorer.py](nlp_scorer.py) | Training, saved-model loading, keyword matching, smoothing, and risk thresholds |
| [train_model.py](train_model.py) | Training entry point |
| [your_dataset.csv](your_dataset.csv) | Included labeled training data |
| [realtime_asr.py](realtime_asr.py) | Terminal transcription and scoring |
| [try.py](try.py) | Alternate terminal implementation |

Start with `BERTScorer.score()` to understand the returned scores, then follow `transcribe_score_thread()` in `app.py` to see how audio becomes a dashboard result.

## Terminal mode

```bash
python realtime_asr.py
```

This script starts system-audio capture, accepts `m` + Enter to toggle the microphone, and stops with Ctrl+C. Unlike the dashboard, it explicitly configures Whisper for CUDA/float16.
