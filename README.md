# 🌲 TraiLens

> An offline-first, local-inference field naturalist journal built for the Hacktoberfest "Touch Grass" AI Challenge.

TrailLens eliminates screen time on the trail. Put your phone in airplane mode, hike screen-free, and take photos of flora, fauna, and geology. When you return, TrailLens processes your photos locally using **Moondream** via **Ollama**, extracting EXIF metadata and generating an automated Markdown field journal with zero cloud API dependencies.

## Features
- **100% Offline & Private:** Zero telemetry or cloud calls. GPS and photos stay on your device.
- **Local Vision Inference:** Powered by Moondream via Ollama.
- **EXIF Extraction:** Automatically retrieves capture timestamps and GPS markers.

## Quickstart
1. Install [Ollama](https://ollama.com) and pull the model:
   ```bash
   ollama pull moondream