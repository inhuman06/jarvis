import os
import subprocess
import time
import webbrowser
import pyautogui
from win32com.client import Dispatch

# 🌐 Import your standalone module here
import tradingview

def open_pc_app(app_name: str):
    """Dynamically scans the Windows Applications folder for an installed software match."""
    app_name = app_name.lower().strip()
    print(f"\n[🔍 Scanning Windows System for: '{app_name}'...]")
    
    if app_name in ["recycle bin", "trash", "bin"]:
        os.system("start explorer.exe shell:RecycleBinFolder")
        return "Opening the Recycle Bin for you now, sir."
        
    if app_name in ["control panel", "settings"]:
        os.system("start control")
        return "Opening the Control Panel, sir."

    try:
        objShell = Dispatch("Shell.Application")
        objFolder = objShell.NameSpace("shell:AppsFolder")
        
        for item in objFolder.Items():
            if app_name in item.Name.lower():
                print(f"[🚀 Found match: {item.Name} | Executing path: {item.Path}]")
                os.startfile(f"shell:AppsFolder\\{item.Path}")
                return f"I have successfully launched {item.Name}, sir."
                
        return f"I searched your system, sir, but couldn't find an application named '{app_name}'."
    except Exception as e:
        return f"Encountered a system error while trying to open the application: {e}"


def close_pc_app(app_name: str):
    """
    Universal Window Closure Engine.
    Locates any running program matching the target title on screen and forces it to close.
    Handles both legacy desktop software (.exe) and modern Windows Store UWP apps cleanly.
    """
    app_name_clean = app_name.lower().strip().replace(".exe", "")
    print(f"\n[🛡️ JARVIS Close Request received for window matching: '{app_name_clean}']")

    # 1. First Pass: GUI Window Search
    # This loop finds the actual visual window frame on your screen (even modern Windows Store layout windows)
    all_windows = pyautogui.getAllWindows()
    closed_any = False

    for window in all_windows:
        if app_name_clean in window.title.lower() and window.title != "":
            print(f"[💥 Found matching window title: '{window.title}' | Attempting closure...]")
            try:
                window.close() # Sends a standard WM_CLOSE system instruction to the active frame container
                closed_any = True
            except Exception as win_err:
                print(f"[⚠️ Window close command failed: {win_err}. Falling back to hard process kill...]")

    if closed_any:
        # Give the operating system a split second to release memory and drop the frame interface safely
        time.sleep(0.5)
        return f"I have successfully closed the {app_name} layout window, sir."

    # 2. Second Pass: Hard Process Fallback
    # If no window title matched, execute a raw wildcard process taskkill statement
    process_map = {
        "calculator": ["CalculatorApp.exe", "calc.exe", "Calculator.exe"],
        "calc": ["CalculatorApp.exe", "calc.exe", "Calculator.exe"],
        "notepad": ["notepad.exe"],
        "chrome": ["chrome.exe"],
        "edge": ["msedge.exe"],
        "tradingview": ["TradingView.exe"],
        "spotify": ["Spotify.exe"],
        "discord": ["Discord.exe"],
        "taskmgr": ["taskmgr.exe"],
        "cmd": ["cmd.exe"],
        "whatsapp": ["WhatsApp.exe", "WhatsAppDesktop.exe", "WhatsApp*"]
    }

    if app_name_clean in process_map:
        kill_targets = " ".join([f"/im {proc}" for proc in process_map[app_name_clean]])
        os_command = f"taskkill /f {kill_targets}"
    else:
        os_command = f"taskkill /f /im {app_name_clean}.exe /im {app_name_clean}"

    try:
        result = subprocess.run(
            os_command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=5,
            env=os.environ
        )
        if result.returncode == 0:
            return f"I have forcefully terminated the {app_name} background process thread, sir."
        else:
            return f"The process or window for {app_name} does not appear to be active on your screens right now, sir."
    except Exception as e:
        return f"Failed to execute process termination layout routine: {e}"


def open_website(url_or_name: str):
    """Force opens a website inside Google Chrome or falls back to system browser."""
    print(f"\n[🌐 Attempting to open website: '{url_or_name}'...]")
    web_map = {
        "chatgpt": "https://chatgpt.com",
        "openai": "https://openai.com",
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "tradingview": "https://www.tradingview.com",
        "github": "https://github.com"
    }
    clean_target = url_or_name.lower().strip()
    
    if clean_target in web_map:
        target_url = web_map[clean_target]
    else:
        if "." in clean_target:
            target_url = clean_target if clean_target.startswith("http") else f"https://{clean_target}"
        else:
            target_url = f"https://www.google.com/search?q={url_or_name}"

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    chrome_launched = False
    
    for path in chrome_paths:
        if os.path.exists(path):
            try:
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
                webbrowser.get('chrome').open(target_url)
                chrome_launched = True
                break
            except Exception:
                continue

    if not chrome_launched:
        try:
            webbrowser.open(target_url)
        except Exception as e:
            return f"Failed to open the website due to an error: {e}"
    return f"Opening {url_or_name} now, sir."


def control_tradingview(action: str, value: str = ""):
    """Passes chart commands over to our standalone tradingview module file."""
    return tradingview.handle_macro(action=action, value=value)


def type_text_into_active_window(prompt_text: str):
    """Simulates physical keyboard inputs to type strings into any active window."""
    if not prompt_text:
        return "No text was provided for me to type, sir."
    print(f"\n[⌨️ JARVIS Typing Macro: '{prompt_text}']")
    try:
        time.sleep(0.5)
        pyautogui.write(prompt_text, interval=0.01)
        time.sleep(0.2)
        pyautogui.press('enter')
        return "Successfully typed and submitted your prompt, sir."
    except Exception as e:
        return f"Failed to execute typing macro tool: {e}"


def execute_windows_system_command(os_command: str):
    """Executes a raw command directly inside the Windows Command Prompt (cmd.exe)."""
    if not os_command:
        return "No system command was provided, sir."
    
    print(f"\n[🖥️ JARVIS OS Action: Executing '{os_command}']")
    try:
        result = subprocess.run(
            os_command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10,
            env=os.environ
        )
        if result.returncode == 0:
            output = result.stdout.strip() if result.stdout else "Command completed successfully."
            return f"System output: {output}"
        else:
            return f"System reported an error or process was ended: {result.stderr.strip()}"
    except Exception as e:
        return f"Failed to execute OS command: {e}"