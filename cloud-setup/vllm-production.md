# vLLM Production Setup for Phoenix Knowledge Engine

## Why vLLM?
- **10x faster** than Ollama for production
- **Better batching** and throughput
- **OpenAI-compatible API**
- **More efficient memory usage**

## RunPod vLLM Setup

### 1. Deploy vLLM Template
```bash
# On RunPod, deploy vLLM template
# Choose RTX 4090 or A100 (24GB+ VRAM)

# SSH into pod
ssh root@[your-pod-ip]

# Install vLLM
pip install vllm

# Start vLLM server
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --port 8000 \
    --host 0.0.0.0 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9
```

### 2. Update Phoenix Configuration
```python
# services/cloud_llm.py
import requests
import json

class CloudLLMService:
    def __init__(self, base_url="http://[your-pod-ip]:8000/v1"):
        self.base_url = base_url
        self.api_key = "dummy-key"  # vLLM doesn't require real API key
    
    def chat_completions_create(self, model, messages, **kwargs):
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": model,
                "messages": messages,
                **kwargs
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
```

## Cost Comparison

| Solution | Setup Time | Monthly Cost | Performance | Reliability |
|----------|------------|--------------|-------------|-------------|
| **Ollama Local** | 1 hour | $0 | Slow | Poor |
| **RunPod Ollama** | 15 min | $50-100 | Good | Good |
| **RunPod vLLM** | 30 min | $50-100 | Excellent | Good |
| **AWS EC2** | 2 hours | $200-400 | Excellent | Excellent |

## Auto-Scaling Setup

### 1. Create Startup Script
```bash
#!/bin/bash
# startup.sh
cd /workspace
ollama serve --host 0.0.0.0 &
# Auto-shutdown after 2 hours of inactivity
sleep 7200 && shutdown now
```

### 2. Use RunPod Serverless
- Even cheaper than dedicated pods
- Scales to zero when not in use
- Perfect for development/testing

## Monitoring & Optimization

### 1. Add Health Checks
```python
def health_check():
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False
```

### 2. Implement Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_generation(prompt_hash):
    # Generate and cache responses
    pass
```

### 3. Model Switching
```python
MODELS = {
    'development': 'mistral:7b',  # Faster, cheaper
    'production': 'llama3.1:8b',  # Better quality
    'quality_control': 'llama3.1:8b'
}
```
