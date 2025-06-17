import subprocess
import time

def run_wsl_cmd(script: str):
    return subprocess.run(["wsl", "bash", "-c", script], capture_output=True, text=True)

def is_redis_running():
    result = run_wsl_cmd("pgrep redis-server")
    return result.returncode == 0

def start_redis():
    print("➡️ Starting Redis...")
    run_wsl_cmd("nohup redis-server > /dev/null 2>&1 &")
    time.sleep(1)

def wait_for_redis(timeout=10):
    print("⏳ Waiting for Redis to respond to PING...")
    start = time.time()
    while time.time() - start < timeout:
        result = run_wsl_cmd("redis-cli ping")
        if "PONG" in result.stdout:
            print("✅ Redis is up and responding.")
            return True
        time.sleep(0.5)
    print("❌ Redis failed to respond within timeout.")
    return False

def ensure_redis_alive():
    if is_redis_running():
        print("ℹ️ Redis already running.")
    else:
        start_redis()

    if not wait_for_redis():
        raise RuntimeError("Redis failed to start or respond.")

# Run this before your app connects to Redis
