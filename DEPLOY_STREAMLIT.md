# 🚀 Deploy to Streamlit Cloud

## Quick Deploy Instructions

### 1. Prerequisites
- GitHub account with this repository
- Streamlit Cloud account (free): https://streamlit.io/cloud

### 2. Get API Keys
1. **Google Gemini API**: https://ai.google.dev/
2. **Pinecone**: https://www.pinecone.io/ (free tier available)

### 3. Deploy Steps

1. **Go to Streamlit Cloud**: https://share.streamlit.io/

2. **Click "New app"**

3. **Fill in the details**:
   - **Repository**: `RakshGM/AI-Contract-Analysis`
   - **Branch**: `main`
   - **Main file path**: `app_ui.py`

4. **Click "Advanced settings"** and add your secrets:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   PINECONE_API_KEY = "your_actual_pinecone_api_key"
   PINECONE_INDEX = "your_pinecone_index_name"
   ```

5. **Click "Deploy"**

6. **Wait 2-3 minutes** for the app to build and deploy

### 4. Your App URL
Your app will be available at:
```
https://rakshgm-ai-contract-analysis.streamlit.app
```

Or similar (Streamlit will generate the URL)

### 5. Update GitHub Pages
Once deployed, update `index.html` line 6 with your actual Streamlit app URL:
```html
<meta http-equiv="refresh" content="3;url=YOUR_STREAMLIT_APP_URL">
```

## Troubleshooting

### Issue: App crashes on startup
- **Solution**: Make sure all secrets are added in Streamlit Cloud settings

### Issue: Import errors
- **Solution**: Check that `requirements.txt` includes all dependencies

### Issue: Pinecone connection fails
- **Solution**: Verify your Pinecone index exists and API key is correct

## Files for Streamlit Cloud

✅ `app_ui.py` - Main application file  
✅ `requirements.txt` - Python dependencies  
✅ `.streamlit/config.toml` - Streamlit configuration  
✅ `packages.txt` - System dependencies (if needed)  
✅ `.streamlit/secrets.toml.example` - Example secrets file  

## Post-Deployment

1. Test your live app
2. Share the URL: `https://your-app.streamlit.app`
3. GitHub Pages will auto-redirect visitors to your live app
4. Update README.md with your live app link

## Support

- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/
