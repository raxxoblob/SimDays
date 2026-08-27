import subprocess
import time
import os
import re

TASKS_FILE = "tasks.txt"
MEMORY_FILE = "AGENT_MEMORY.md"
PROJECT_DIR = os.path.expanduser("~/Documents/SimDays/SimDays")
RENPY_PATH = "/Applications/renpy-8.5.3-sdk/renpy.sh"
LINT_CMD = f"{RENPY_PATH} {PROJECT_DIR} lint"

def init_files():
    tasks_path = os.path.join(PROJECT_DIR, TASKS_FILE)
    memory_path = os.path.join(PROJECT_DIR, MEMORY_FILE)
    
    if not os.path.exists(tasks_path):
        with open(tasks_path, "w", encoding="utf-8") as f:
            f.write("")
            
    if not os.path.exists(memory_path):
        with open(memory_path, "w", encoding="utf-8") as f:
            f.write("# Historia zmian Agenta\n\n")

def check_renpy_errors():
    """Automatycznie uruchamia linter Ren'Py i wyciąga błędy."""
    print("\n[AUTO-LINT] Sprawdzanie poprawności kodu gier w Ren'Py...")
    res = subprocess.run(LINT_CMD, shell=True, capture_output=True, text=True)
    output = res.stdout + "\n" + res.stderr
    
    if res.returncode != 0 or "expected statement" in output or "ERROR" in output or "Exception" in output:
        print("[AUTO-LINT] Wykryto błędy w projekcie! Przekazywanie do naprawy...")
        lines = [line for line in output.splitlines() if "File " in line or "error" in line.lower() or "expected" in line.lower()]
        return "\n".join(lines[-15:]) if lines else output[-1000:]
    
    print("[AUTO-LINT] Kod gry jest czysty, brak błędów kompilacji.")
    return None

def execute_aider(task_text):
    print("\n==========================================")
    print(f"Uruchamianie zadania: {task_text[:100]}...")
    print("==========================================\n")
    
    found_files = re.findall(r'[\w/\\-]+\.(?:rpy|py|md)', task_text)
    
    cmd = [
        "aider",
        "--openai-api-base", "http://192.168.1.102:1234/v1",
        "--openai-api-key", "lm-studio",
        "--model", "openai/huihui-qwen3.8-27b-abliterated",
        "--edit-format", "diff",
        "--subtree-only",
        "--map-tokens", "0",
        "--no-show-model-warnings",
        "--read", "CONVENTIONS.md",
        "--file", MEMORY_FILE,
    ]

    if found_files:
        for file_path in set(found_files):
            if file_path not in cmd:
                cmd.extend(["--file", file_path])
    else:
        cmd.extend(["--file", "game/script.rpy"])

    cmd.extend([
        "--message", task_text,
        "--yes-always"
    ])
    
    try:
        subprocess.run(cmd, cwd=PROJECT_DIR)
    except Exception as e:
        print(f"\n[BŁĄD AIDER]: {e}")

def run_loop():
    init_files()
    
    # 1. Najpierw sprawdzamy błędy w Ren'Py
    errors = check_renpy_errors()
    if errors:
        fix_task = f"Napraw błędy zgłoszone przez linter Ren'Py:\n\n{errors}"
        execute_aider(fix_task)
        return True

    # 2. Jeśli nie ma błędów, czytamy zadanie z tasks.txt
    tasks_path = os.path.join(PROJECT_DIR, TASKS_FILE)
    with open(tasks_path, "r", encoding="utf-8") as f:
        tasks = [line.strip() for line in f.readlines() if line.strip()]

    if tasks:
        current_task = tasks[0]
        remaining_tasks = tasks[1:]
        
        execute_aider(current_task)
        
        with open(tasks_path, "w", encoding="utf-8") as f:
            f.write("\n".join(remaining_tasks) + ("\n" if remaining_tasks else ""))
        return True

    print("Brak zadań w tasks.txt i brak błędów w kodzie. Czekam...")
    return False

if __name__ == "__main__":
    os.chdir(PROJECT_DIR)
    print("Agent Game Dev uruchomiony (Automatyczny Linter + Autonomiczne naprawy)...")
    while True:
        try:
            has_work = run_loop()
            time.sleep(5 if has_work else 15)
        except Exception as e:
            print(f"Błąd pętli głównej: {e}")
            time.sleep(10)
