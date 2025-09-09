# RunPod Deployment Guide for Phoenix Knowledge Engine

## Quick Setup (15 minutes)

### 1. Create RunPod Account
- Go to https://runpod.io
- Sign up with GitHub/Google
- Add payment method ($10 minimum)

### 2. Deploy Ollama Template
- Click "Deploy" → "Templates"
- Search for "Ollama"
- Select "Ollama" template
- Choose RTX 4090 (24GB VRAM) - $0.29/hour
- Deploy

### 3. Configure Your Pod
```bash
# SSH into your pod
ssh root@[your-pod-ip]

# Pull the models
ollama pull llama3.1:8b
ollama pull mistral:7b

# Start Ollama server
ollama serve --host 0.0.0.0
```

### 4. Update Phoenix Configuration
```python
# In your local .env file
OLLAMA_BASE_URL=http://[your-pod-ip]:11434
```

### 5. Test the Connection
```bash
curl http://[your-pod-ip]:11434/api/tags
```

## Cost Optimization

### Auto-Shutdown
- Set up auto-shutdown after 1 hour of inactivity
- Use RunPod's "Serverless" mode for even cheaper costs

### Model Optimization
- Use quantized models (Q4_K_M) for faster inference
- Consider smaller models for simple tasks

## Expected Costs
- **Development**: $5-15/day (8 hours usage)
- **Production**: $50-100/month (24/7 with auto-shutdown)
- **Peak usage**: $200/month (heavy usage)

## Security
- Use SSH keys for access
- Set up firewall rules
- Use HTTPS for production
