import subprocess
import time

print("🚀 Starting AI Financial Document Analyzer...")

# Start FastAPI backend
backend = subprocess.Popen(["uvicorn", "api.main:app", "--reload"])

# Give backend a few seconds to start
time.sleep(3)

# Start Streamlit frontend
frontend = subprocess.Popen(["streamlit", "run", "ui/app.py"])

print("\n✅ System running successfully!")
print("⚙️  Running servers")
print("🌐 FastAPI → http://127.0.0.1:8000")
print("💻 Streamlit → http://localhost:8501")

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping servers...")
    backend.terminate()
    frontend.terminate()
    print("✅ All processes stopped successfully.")
