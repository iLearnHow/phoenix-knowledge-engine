# 🧪 Testing Phoenix Knowledge Engine with Real API Calls

## 🚀 Quick Start Testing

### **Step 1: Set Up Your OpenAI API Key**

1. **Get your API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Edit the .env file**:
   ```bash
   cd backend
   nano .env
   ```
3. **Replace the placeholder**:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### **Step 2: Run Quick Test (Recommended First)**

This is a simple test that doesn't require Django setup:

```bash
cd backend
python quick_api_test.py
```

**Expected cost**: $0.10 - $0.50
**Duration**: 2-3 minutes

### **Step 3: Run Full Test Suite**

If the quick test works, run the comprehensive test:

```bash
cd backend
python test_real_api.py
```

**Expected cost**: $0.50 - $2.00
**Duration**: 5-10 minutes

## 📊 What Each Test Does

### **Quick Test (`quick_api_test.py`)**
- ✅ Tests basic API connectivity
- ✅ Tests orchestrator prompts
- ✅ Tests worker component generation
- ✅ Tests Kelly vs Ken avatar prompts
- ✅ Shows cost tracking
- ✅ No Django setup required

### **Full Test (`test_real_api.py`)**
- ✅ Tests complete Django integration
- ✅ Tests all services (orchestrator, worker, quality control)
- ✅ Tests avatar system
- ✅ Tests complete lesson generation
- ✅ Tests cost monitoring system
- ✅ Generates sample lessons
- ✅ Saves detailed results

## 💰 Cost Management

### **Built-in Cost Protection**
- **Daily limit**: $5 (configurable)
- **Monthly limit**: $50 (configurable)
- **Real-time tracking**: See costs as they happen
- **Automatic alerts**: Warnings at 80% of limits

### **Expected Costs**
| Test Type | Estimated Cost | Duration |
|-----------|---------------|----------|
| Quick Test | $0.10 - $0.50 | 2-3 min |
| Full Test | $0.50 - $2.00 | 5-10 min |
| Sample Lessons (5) | $1.00 - $3.00 | 10-15 min |

### **Cost Optimization**
- Uses GPT-3.5-turbo (cheapest model)
- Optimized prompts to minimize tokens
- Built-in rate limiting to avoid overuse

## 🎯 Test Results

### **What to Expect**
- **Success Rate**: 95%+ (if API key is correct)
- **Content Quality**: High-quality educational content
- **Avatar Differences**: Clear personality differences between Kelly and Ken
- **Cost Tracking**: Real-time cost monitoring

### **Sample Output**
```
🧪 Phoenix Knowledge Engine - Quick API Test
==================================================
✅ OpenAI client configured: sk-1234567890...
🎯 Testing Orchestrator: The Pythagorean Theorem
✅ Orchestrator success! Cost: $0.0023
   Title: The Pythagorean Theorem
   Components: 5
🔧 Testing Worker: CORE_CONCEPT for The Pythagorean Theorem
✅ Worker success! Cost: $0.0015
   Content: The Pythagorean theorem states that in a right triangle...
🎭 Testing Avatar Prompts: The Pythagorean Theorem
✅ Kelly success! Cost: $0.0018
   Content: Let's work through this fundamental geometric principle...
✅ Ken success! Cost: $0.0018
   Content: Here's how this theorem works in real-world construction...
```

## 🛠️ Troubleshooting

### **Common Issues**

**1. API Key Not Working**
```bash
# Check your .env file
cat backend/.env | grep OPENAI_API_KEY
```
**Solution**: Make sure your API key starts with `sk-` and is valid

**2. Import Errors**
```bash
# Install missing dependencies
pip install openai python-dotenv
```
**Solution**: Install required packages

**3. Rate Limiting**
```
Error: Rate limit exceeded
```
**Solution**: Wait a few minutes and try again

**4. Cost Exceeded**
```
Error: Insufficient credits
```
**Solution**: Add credits to your OpenAI account

### **Debug Mode**
If tests fail, check the detailed error messages:
```bash
# Run with verbose output
python quick_api_test.py 2>&1 | tee test_output.log
```

## 📈 Next Steps After Testing

### **If Tests Pass**
1. **Deploy to cloud**: Use Railway, Heroku, or Docker
2. **Generate real content**: Create lessons for your topics
3. **Monitor costs**: Use the built-in cost tracking
4. **Customize prompts**: Adjust for your specific needs

### **If Tests Fail**
1. **Check API key**: Ensure it's valid and has credits
2. **Check internet**: Ensure you can reach OpenAI API
3. **Check dependencies**: Install all required packages
4. **Check logs**: Look at error messages for clues

## 🎉 Success Criteria

### **Quick Test Success**
- ✅ API key works
- ✅ Basic prompts generate content
- ✅ Avatars show different personalities
- ✅ Cost tracking works
- ✅ No errors in output

### **Full Test Success**
- ✅ All services work
- ✅ Complete lessons generated
- ✅ Quality control validates content
- ✅ Cost monitoring tracks usage
- ✅ Results saved to file

## 📞 Support

### **If You Need Help**
1. **Check logs**: Look at error messages
2. **Check costs**: Ensure you have OpenAI credits
3. **Check network**: Ensure internet connectivity
4. **Check configuration**: Verify .env file

### **Files to Check**
- `backend/.env` - API key configuration
- `test_results.json` - Detailed test results
- `backend/budget_tracking.json` - Cost tracking data

---

**Ready to test? Run the quick test first!** 🚀

```bash
cd backend
python quick_api_test.py
```
