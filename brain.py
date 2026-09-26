import os
import ollama
import commands 
from dotenv import load_dotenv
from groq import Groq
from google import genai
import json
import copy

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

groq_client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
gemini_client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

SYSTEM_PROMPT = """
You are Jarvis, an advanced AI assistant with complete control over the host's Windows operating system.
Keep your replies brief, clear, and professional. One or two short sentences maximum.

CRITICAL INSTRUCTION: If the user asks a general knowledge or factual question (e.g., "what is quantum physics", "explain artificial intelligence", or asks you to define something), do NOT call any web-browsing or file tools. Instead, answer them directly and concisely using your own internal knowledge.

Only invoke a tool when explicitly ordered to perform a direct action on the host PC system:
1. 'open_pc_app': Use when the user asks to launch a local program.
2. 'close_pc_app': Use when the user specifically asks to close, exit, terminate, or kill any windows application.
3. 'open_website': Use when they want to navigate to a specific URL link or open a specific web platform.
4. 'control_tradingview': Use strictly when the user wants to open, view, modify, or control their installed TradingView Desktop app features.
5. 'type_text_into_active_window': Use when the user tells you to type or send text into a focused text field.
6. 'execute_windows_system_command': Use for general system commands like making directories or running scripts.
"""

AVAILABLE_TOOLS = {
    'open_pc_app': commands.open_pc_app,
    'close_pc_app': commands.close_pc_app,
    'open_website': commands.open_website,
    'control_tradingview': commands.control_tradingview,
    'type_text_into_active_window': commands.type_text_into_active_window,
    'execute_windows_system_command': commands.execute_windows_system_command
}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "open_pc_app",
            "description": "Scans Windows and opens an installed local desktop application or system shortcut folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The exact name of the application or folder to locate and launch."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_pc_app",
            "description": "Forcefully terminates any running background windows application or process by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "The name of the application process to terminate (e.g. calculator, notepad, chrome, edge)."}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Launches web URLs or performs google web queries in Google Chrome.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url_or_name": {"type": "string", "description": "Web app nickname or standard internet address format."}
                },
                "required": ["url_or_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "control_tradingview",
            "description": "Controls your running local TradingView app features like changing indicators, assets, drawing lines, or layout adjustments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string", 
                        "enum": ["open_tv", "change_ticker", "change_timeframe", "add_alert", "clear_drawings", "toggle_indicators", "draw_horizontal_line"],
                        "description": "The specific TradingView chart command action sequence required."
                    },
                    "value": {"type": "string", "description": "The target argument like a symbol or timeframe interval. Leave blank if not required."}
                },
                "required": ["action"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "type_text_into_active_window",
            "description": "Simulates keyboard keystrokes to type continuous text strings into the currently active text box.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt_text": {"type": "string", "description": "The raw message text block that must be written."}
                },
                "required": ["prompt_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_windows_system_command",
            "description": "Executes a raw command inside cmd.exe.",
            "parameters": {
                "type": "object",
                "properties": {
                    "os_command": {"type": "string", "description": "The converted functional Windows cmd line string."}
                },
                "required": ["os_command"]
            }
        }
    }
]

def think(text, conversation_history, provider="ollama"):
    provider = provider.lower()
    if not conversation_history:
        conversation_history.append({"role": "system", "content": SYSTEM_PROMPT})
    conversation_history.append({"role": "user", "content": text})

    try:
        # =====================================================================
        # ENGINE 1: OLLAMA
        # =====================================================================
        if provider == "ollama":
            ollama_history = copy.deepcopy(conversation_history)
            for msg in ollama_history:
                if msg.get('role') == 'assistant' and 'tool_calls' in msg:
                    for tc in msg['tool_calls']:
                        if isinstance(tc['function']['arguments'], str):
                            try:
                                tc['function']['arguments'] = json.loads(tc['function']['arguments'])
                            except:
                                pass

            response = ollama.chat(
                model="qwen2.5:3b",
                messages=ollama_history,
                tools=TOOLS_SCHEMA,
                keep_alive=-1,
                options={"num_predict": 128, "temperature": 0.1}
            )

            if response.get('message', {}).get('tool_calls'):
                assistant_message = response['message']
                conversation_history.append(assistant_message)
                
                for tool_call in assistant_message.get('tool_calls', []):
                    function_name = tool_call['function']['name']
                    arguments = tool_call['function']['arguments']
                    
                    if isinstance(arguments, str):
                        arguments = json.loads(arguments)
                    
                    print(f"\n[🔧 JARVIS invoking tool: {function_name}({arguments})]")
                    
                    if function_name in AVAILABLE_TOOLS:
                        tool_func = AVAILABLE_TOOLS[function_name]
                        tool_result = tool_func(**arguments)
                        
                        conversation_history.append({
                            'role': 'tool',
                            'content': str(tool_result),
                            'name': function_name
                        })
                
                ollama_history_2 = copy.deepcopy(conversation_history)
                for msg in ollama_history_2:
                    if msg.get('role') == 'assistant' and 'tool_calls' in msg:
                        for tc in msg['tool_calls']:
                            if isinstance(tc['function']['arguments'], str):
                                try:
                                    tc['function']['arguments'] = json.loads(tc['function']['arguments'])
                                except:
                                    pass

                final_response = ollama.chat(
                    model="qwen2.5:3b", 
                    messages=ollama_history_2,
                    keep_alive=-1,
                    options={"num_predict": 64, "temperature": 0.4}
                )
                reply = final_response['message']['content'].strip()
                conversation_history.append(final_response['message'])
                return reply, conversation_history

            reply = response["message"]["content"].strip()
            conversation_history.append({"role": "assistant", "content": reply})
            return reply, conversation_history

        # =====================================================================
        # ENGINE 2: GROQ
        # =====================================================================
        elif provider == "groq":
            if not groq_client:
                return "Groq key missing from configuration, sir.", conversation_history
            
            groq_history = copy.deepcopy(conversation_history)
            for msg in groq_history:
                if 'tool_calls' in msg and msg['tool_calls']:
                    for tc in msg['tool_calls']:
                        if isinstance(tc['function']['arguments'], dict):
                            tc['function']['arguments'] = json.dumps(tc['function']['arguments'])

            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_history, 
                max_tokens=128,
                temperature=0.3
            )
            reply = completion.choices[0].message.content.strip()
            conversation_history.append({"role": "assistant", "content": reply})
            return reply, conversation_history

    except Exception as e:
        return f"Brain operation execution fault encountered: {e}", conversation_history