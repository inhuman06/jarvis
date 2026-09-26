import time
import os
import pyautogui

def handle_macro(action: str, value: str = ""):
    """
    Core automation engine optimized for the TradingView Windows Desktop App.
    """
    action = action.lower().strip()
    value = value.upper().strip() if value else ""
    
    print(f"\n[🎮 TradingView Desktop Module executing: '{action}' | Param: '{value}']")
    
    try:
        if action == "open_tv":
            print("[🚀 Launching TradingView Desktop App via Windows Shell]")
            # Opens the official installed Windows desktop app directly
            os.startfile("shell:AppsFolder\TradingView.Desktop")
            return "Launching your local TradingView desktop application now, sir."
            
        # ⚠️ CRITICAL TIME DELAY: Gives you 1.5 seconds to make sure the app window 
        # is selected so Windows focuses inputs onto your charts before typing!
        time.sleep(1.5)
        
        if action == "change_ticker":
            pyautogui.write(value)
            time.sleep(0.3)
            pyautogui.press('enter')
            return f"Switched desktop chart ticker to {value}, sir."
            
        elif action == "change_timeframe":
            pyautogui.write(value)
            time.sleep(0.3)
            pyautogui.press('enter')
            return f"Adjusted desktop chart timeframe interval to {value}, sir."
            
        elif action == "add_alert":
            pyautogui.hotkey('alt', 'a')
            return "Opened the desktop alert configuration panel, sir."
            
        elif action == "clear_drawings":
            pyautogui.hotkey('alt', 'b')
            return "Wiped all custom drawing placements from the active layout canvas, sir."
            
        elif action == "toggle_indicators":
            pyautogui.press('/')
            return "Displaying the script and analytical indicators search box, sir."

        elif action == "draw_horizontal_line":
            pyautogui.hotkey('alt', 'h')
            return "Placed a horizontal line anchor onto the layout canvas, sir."

        return f"The desktop action '{action}' is unmapped in the core modules, sir."
        
    except Exception as e:
        return f"TradingView app automation layer experienced an error: {e}"