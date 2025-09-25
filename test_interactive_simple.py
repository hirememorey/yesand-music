#!/usr/bin/env python3
"""
Simple test of interactive input handling
"""

import os
import sys

def test_interactive_input():
    """Test basic interactive input handling"""
    
    print("🔍 Testing Interactive Input Handling")
    print("=" * 50)
    
    try:
        print("Type 'test' and press Enter (or 'quit' to exit):")
        
        while True:
            try:
                user_input = input("🎵 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'test':
                    print("✅ Input received successfully!")
                    print("This proves interactive input is working.")
                    break
                else:
                    print(f"🤖 You said: {user_input}")
                    print("Type 'test' to continue or 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n❌ EOF Error - this is likely the issue!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_interactive_input()
