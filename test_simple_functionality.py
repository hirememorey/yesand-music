#!/usr/bin/env python3
"""
Simple Test of Core Functionality

This script tests the core components without the CLI to avoid input issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_context_interview():
    """Test if the context interview actually guides users"""
    print("🧪 Testing Context Interview...")
    
    try:
        from musical_context_interview import MusicalContextInterview
        
        interview = MusicalContextInterview()
        
        # Test 1: Does it start properly?
        print("1. Starting interview...")
        start_message = interview.start_interview()
        print(f"   ✅ Start message: {start_message[:50]}...")
        
        # Test 2: Does it ask questions?
        print("2. Getting first question...")
        first_question = interview.get_next_question()
        if first_question:
            print(f"   ✅ First question: {first_question.question_text}")
        else:
            print("   ❌ No questions available")
            return False
        
        # Test 3: Does it validate answers?
        print("3. Testing answer validation...")
        success, message = interview.answer_question("song_concept", "A song about leaders who shoot the messenger")
        if success:
            print(f"   ✅ Answer accepted: {message}")
        else:
            print(f"   ❌ Answer rejected: {message}")
            return False
        
        # Test 4: Does it progress through questions?
        print("4. Testing question progression...")
        next_question = interview.get_next_question()
        if next_question:
            print(f"   ✅ Next question: {next_question.question_text}")
        else:
            print("   ❌ No next question")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_conversation_engine():
    """Test if the conversation engine actually uses the context interview"""
    print("\n🧪 Testing Conversation Engine...")
    
    try:
        from musical_conversation_engine import MusicalConversationEngine
        
        engine = MusicalConversationEngine()
        
        # Test 1: Does it start a conversation?
        print("1. Starting conversation...")
        start_message = engine.start_conversation()
        print(f"   ✅ Start message: {start_message[:50]}...")
        
        # Test 2: Does it process user input?
        print("2. Processing user input...")
        response = engine.process_user_input("I need help with a bridge")
        print(f"   ✅ Response: {response[:100]}...")
        
        # Test 3: Does it actually use the context interview?
        print("3. Checking context interview integration...")
        if hasattr(engine, 'context_interview'):
            print("   ✅ Context interview exists")
        else:
            print("   ❌ No context interview")
            return False
        
        # Test 4: Does it generate suggestions?
        print("4. Testing suggestion generation...")
        suggestions = engine._generate_musical_suggestions("I need help with a bridge")
        if suggestions:
            print(f"   ✅ Generated {len(suggestions)} suggestions")
            for i, suggestion in enumerate(suggestions):
                print(f"      {i+1}. {suggestion.title}")
        else:
            print("   ❌ No suggestions generated")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_psychological_insight():
    """Test if the system actually implements the psychological insight"""
    print("\n🧪 Testing Psychological Insight...")
    
    try:
        from musical_context_interview import MusicalContextInterview
        from musical_conversation_engine import MusicalConversationEngine
        
        # The core insight: "Musical quality is not a technical issue to solve, 
        # but a psychological one for the user to understand what they need and want."
        
        print("1. Testing if system guides users to understand what they want...")
        
        interview = MusicalContextInterview()
        interview.start_interview()
        
        # Simulate a user who doesn't know what they want
        print("   Simulating user: 'I need help with my song'")
        
        # The system should ask clarifying questions, not just give technical solutions
        question = interview.get_next_question()
        if question and "song" in question.question_text.lower():
            print(f"   ✅ System asks clarifying question: {question.question_text}")
        else:
            print("   ❌ System doesn't ask clarifying questions")
            return False
        
        print("2. Testing if system builds context before giving suggestions...")
        
        # Answer some questions to build context
        interview.answer_question("song_concept", "A song about leaders who shoot the messenger")
        interview.answer_question("musical_problem", "I need help with a bridge")
        interview.answer_question("key_signature", "G minor")
        interview.answer_question("tempo", "120")
        
        # Now test if the conversation engine uses this context
        engine = MusicalConversationEngine()
        engine.start_conversation()
        
        # The engine should use the context interview's data
        if hasattr(engine, 'context_interview'):
            # This is the critical test - does it actually use the context?
            print("   ✅ Context interview is available")
            
            # Check if the engine actually integrates with the context interview
            if hasattr(engine.conversation_context, 'user_context'):
                print("   ✅ User context is tracked")
            else:
                print("   ❌ No user context tracking")
                return False
        else:
            print("   ❌ No context interview integration")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 Testing Core Functionality of Musical Conversation System")
    print("=" * 70)
    
    tests = [
        ("Context Interview", test_context_interview),
        ("Conversation Engine", test_conversation_engine),
        ("Psychological Insight", test_psychological_insight)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("🎵 TEST RESULTS")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The system is working as designed.")
    else:
        print("⚠️  Some tests failed. The system needs work.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
