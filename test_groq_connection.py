"""
Test Groq API connection and setup
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_groq_connection():
    """Test Groq API connection"""
    
    print("=" * 70)
    print("🔍 GROQ API CONNECTION TEST")
    print("=" * 70)
    
    # Check for API key
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key:
        print("\n❌ GROQ_API_KEY not found in .env file")
        print("\n📝 To fix this:")
        print("   1. Go to https://console.groq.com/keys")
        print("   2. Create a new API key")
        print("   3. Add to your .env file:")
        print("      GROQ_API_KEY=gsk_your_key_here")
        print("\n📖 See GROQ_SETUP.md for detailed instructions")
        return False
    
    print(f"\n✅ GROQ_API_KEY found: {groq_key[:20]}...")
    
    # Try to import Groq
    try:
        from groq import Groq
        print("✅ Groq package installed")
    except ImportError:
        print("❌ Groq package not installed")
        print("   Run: pip install groq")
        return False
    
    # Test API connection
    try:
        print("\n🔌 Testing API connection...")
        client = Groq(api_key=groq_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Connection successful!' if you can read this."}],
            max_tokens=50,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your Groq API is working perfectly!")
        print("=" * 70)
        print("\n📊 Your Groq Plan:")
        print("   - Model: llama-3.3-70b-versatile")
        print("   - Free Tier: 14,400 requests/day")
        print("   - Context: 128K tokens")
        print("\n✨ You can now run the contract analysis system!")
        print("   → python -m ai_agents.main")
        print("   → streamlit run app_ui.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ API Connection Failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your API key is correct")
        print("   2. Verify you have internet connection")
        print("   3. Visit https://console.groq.com to check your account")
        return False

if __name__ == "__main__":
    test_groq_connection()
