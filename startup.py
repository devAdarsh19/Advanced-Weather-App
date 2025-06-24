
import subprocess

def is_wsl_running(running_distro="Ubuntu"):
    try:
        result = subprocess.run(["wsl", "-l", "--running"], capture_output=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        try:
            inst = result.stdout.decode("utf-16-le")
        except UnicodeDecodeError:
            inst = result.stdout.decode("utf-8", errors="ignore")
            
        return running_distro.lower() in inst.lower()
    
    except Exception as e:
        print(f"[ERROR] Error while checking for active Ubuntu instance: {e}")

def start_processes():
    redis_startup_bat_file = "redis_startup.bat"
    
    print(f"----- Running startup processes -----")
    # checking for active wsl / ubuntu instance
    print(f"Ubuntu running: {is_wsl_running("Ubuntu")}")
    if not is_wsl_running("Ubuntu"):
        try:
            # Starting wsl if not found
            print(f"----- Attempting Redis Start -----")
            subprocess.run(["start", redis_startup_bat_file], shell=True)
            print(f"----- Redis running -----")
        except Exception as e:
            print(f"[ERROR] Error while running .bat file for redis startup: \n{e}")
            raise
    else:
        print(f"---- Redis instance already running")
    
    print("#################################")
    
    try:
        print(f"----- Starting main app -----")
        subprocess.run(["uvicorn", "main:app", "--reload"])
    except Exception as e:
        print(f"[ERROR] Error while running starting app: \n{e}")
        raise
    
if __name__ == "__main__":
    start_processes()
