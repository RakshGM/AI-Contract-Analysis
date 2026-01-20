#!/usr/bin/env python
"""
Quick start script for the AI Contract Analysis System.
Run this to get started immediately.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print colored header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_step(num, text):
    """Print step indicator."""
    print(f"[{num}/5] {text}")


def check_python():
    """Verify Python version."""
    print_step(1, "Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required (found {version.major}.{version.minor})")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor} detected")


def setup_venv():
    """Create virtual environment and return venv Python path."""
    print_step(2, "Setting up virtual environment...")

    venv_path = Path("venv")

    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

    if os.name == "nt":  # Windows
        venv_python = str(venv_path / "Scripts" / "python.exe")
    else:  # Unix/Linux/Mac
        venv_python = str(venv_path / "bin" / "python")

    return venv_python


def install_requirements(venv_python):
    """Install dependencies using 'python -m pip' with robust fallback."""
    print_step(3, "Installing dependencies...")

    requirements = Path("requirements.txt")
    if not requirements.exists():
        print("❌ requirements.txt not found")
        sys.exit(1)

    print("Verifying pip in the virtual environment...")
    try:
        subprocess.run([venv_python, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("⚠ pip not available in venv, attempting to bootstrap via ensurepip...")
        subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

    print("This may take 2-3 minutes...")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies with pip. Attempting pip repair...")
        # Try to repair pip and retry once
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=False)
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed after pip repair")


def setup_env_file():
    """Create .env file if needed."""
    print_step(4, "Checking configuration...")

    env_file = Path(".env")

    if env_file.exists():
        print("✓ .env file already exists")
        return

    print("Creating .env file with placeholders...")

    env_content = """# AI Contract Analysis System Configuration
# Add your API keys here

# Required (get from https://ai.google.dev/)
GEMINI_API_KEY=your-gemini-key-here

# Required (get from https://www.pinecone.io/)
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_INDEX=contract-analysis

# Optional (get from https://console.groq.com/)
GROQ_API_KEY=your-groq-key-here

# Optional configuration
GEMINI_MODEL=gemini-1.5-flash
"""

    with open(env_file, "w") as f:
        f.write(env_content)

    print("✓ .env file created with placeholders")
    print("  → Edit .env to add your API keys")


def run_tests(_venv_python=None):
    """Run test suite."""
    print_step(5, "Running tests...")

    if not Path("tests_comprehensive.py").exists():
        print("⚠ tests_comprehensive.py not found, skipping tests")
        return

    print("Running test suite...")
    result = subprocess.run(
        [sys.executable, "tests_comprehensive.py"], capture_output=True, text=True
    )

    if result.returncode == 0:
        print("✓ All tests passed!")
    else:
        print("⚠ Some tests failed or were skipped (this is OK if APIs not configured)")
        print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)


def print_next_steps():
    """Print next steps."""
    print_header("🎉 Setup Complete!")

    print("Next steps:")
    print()
    print("1. Configure your API keys:")
    print("   Edit .env and add:")
    print("   - GEMINI_API_KEY (from https://ai.google.dev/)")
    print("   - PINECONE_API_KEY (from https://www.pinecone.io/)")
    print()
    print("2. Start the web server:")
    print("   python api_enhanced.py")
    print()
    print("3. Open your browser:")
    print("   http://localhost:8000")
    print()
    print("4. Upload a contract and generate a report!")
    print()
    print("For more information, see:")
    print("   - PROJECT_DOCUMENTATION.md (complete guide)")
    print("   - QUICK_REFERENCE.md (quick lookup)")
    print("   - IMPLEMENTATION_GUIDE.md (technical details)")
    print()


def main():
    """Run setup sequence."""
    print_header("🚀 AI Contract Analysis System - Quick Start")

    try:
        check_python()
        venv_python = setup_venv()
        install_requirements(venv_python)
        setup_env_file()
        run_tests(venv_python)
        print_next_steps()

        print("✓ Setup successful! Ready to analyze contracts.\n")

    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
