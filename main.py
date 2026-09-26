import voice
import brain
import time

def main():
    # Start with an empty conversation memory list
    memory = []
    
    # Wake up greeting
    voice.speak("Systems online. Core communications established. How can I assist you, sir?")
    
    # Track whether JARVIS is currently engaged in an active conversation
    active_conversation = False
    
    while True:
        # Sensitive listening state
        user_input = voice.listen()
        
        if user_input:
            user_input_lower = user_input.lower().strip()
            
            # --- GLOBAL SHUTDOWN ---
            shutdown_keywords = ["power down", "shutdown", "stop", "stop jarvis"]
            if any(cmd in user_input_lower for cmd in shutdown_keywords):
                voice.speak("Shutting down core systems. Understood, sir. Goodbye.")
                break
            
            # Context active
            active_conversation = True
            
            # --- CHOOSE THE RIGHT AI ENGINE ---
            # Default to Ollama, use cloud only when requested
            provider = "ollama"
            
            if "analyze" in user_input_lower or "market" in user_input_lower:
                provider = "gemini"  # Use Gemini for heavy data/docs/charts
                voice.speak("Consulting Gemini analytical engine...")
            elif "quick" in user_input_lower or "chat" in user_input_lower:
                provider = "groq"    # Use Groq for ultra-fast voice responses
            
            # Pass user input and engine selection to the brain
            reply, memory = brain.think(user_input, memory, provider=provider)
            
            # Speak the response out loud
            voice.speak(reply)
            
            # Visual breathing room
            print(f"\n💬 [JARVIS ({provider.upper()}) is waiting for your reply...]")
            
        else:
            if active_conversation:
                print("\n[💤 Conversation paused. JARVIS going back to idle mode.]")
                active_conversation = False

if __name__ == "__main__":
    main()