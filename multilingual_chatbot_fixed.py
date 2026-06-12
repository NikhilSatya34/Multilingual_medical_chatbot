"""
Multilingual Medical Chatbot
Answers medical questions in multiple languages
Combines translation, language detection, and medical Q&A
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai

from language_detector import LanguageDetector
from translator_fixed import Translator

# Load environment variables
load_dotenv()


class MultilingualChatbot:
    """
    Multilingual medical chatbot
    Detects language, translates, answers, translates back
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize multilingual chatbot
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found!")
        
        # Initialize Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        # Initialize language tools
        self.detector = LanguageDetector()
        self.translator = Translator()
        
        # Chat history
        self.conversation_history = []
        self.language_stats = {}
        
        print("✅ Multilingual Chatbot initialized")
        print("   Supports 20+ languages")
    
    def answer_question(self, question: str, 
                       user_language: str = None) -> Dict:
        """
        Answer a medical question in user's language
        
        Args:
            question: Medical question (in any language)
            user_language: User's language code (auto-detect if None)
            
        Returns:
            Dictionary with question, answer, language info
        """
        print(f"\n🔄 Processing multilingual query...")
        
        # Step 1: Detect language
        if user_language is None:
            detection_result = self.detector.detect_language(question)
            user_language = detection_result['language']
            confidence = detection_result['confidence']
            print(f"   Language detected: {detection_result['flag']} {detection_result['language_name']} ({confidence}%)")
        else:
            detection_result = self.detector.detect_language(question)
            print(f"   Language: {user_language}")
        
        # Step 2: Translate to English if needed
        if user_language != 'en':
            print(f"   Translating to English...")
            translation_result = self.translator.translate(
                question, user_language, 'en'
            )
            english_question = translation_result['translated_text']
            print(f"   EN: {english_question}")
        else:
            english_question = question
            translation_result = None
        
        # Step 3: Generate answer in English
        print(f"   Generating medical answer...")
        
        system_prompt = """You are a helpful medical information assistant. 
Provide accurate, informative answers about medical topics.
Keep responses concise and educational.
Always recommend consulting healthcare professionals for specific medical advice."""
        
        prompt = f"""Answer this medical question:
{english_question}

Provide a helpful, accurate medical answer."""
        
        # NEW (WITH FALLBACK):
        try:
            response = self.model.generate_content(prompt)
            english_answer = response.text
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                english_answer = """I've reached my API quota for today. 

        This is a free tier limitation. The quota resets daily or you can upgrade to a paid plan for unlimited requests.

        Please try again in a few moments or check your API usage at: https://console.cloud.google.com/"""
            else:
                english_answer = f"⚠️ Error generating response: {str(e)}"
                original_english_answer = english_answer
        
        # Step 4: Translate back to user's language if needed
        if user_language != 'en':
            print(f"   Translating back to {user_language}...")
            back_translation = self.translator.translate(
                english_answer, 'en', user_language
            )
            user_answer = back_translation['translated_text']
        else:
            user_answer = english_answer
        
        # Step 5: Update statistics
        self._update_stats(user_language)
        
        # Step 6: Store in history
        result = {
            'original_question': question,
            'user_language': user_language,
            'english_question': english_question,
            'english_answer': original_english_answer,
            'translated_answer': user_answer,
            'language_info': detection_result,
            'success': True
        }
        
        self.conversation_history.append(result)
        
        print(f"   ✅ Response ready\n")
        
        return result
    
    def _update_stats(self, language: str):
        """
        Update language usage statistics
        
        Args:
            language: Language code
        """
        if language not in self.language_stats:
            self.language_stats[language] = 0
        
        self.language_stats[language] += 1
    
    def get_answer_in_language(self, question: str, 
                              target_language: str) -> str:
        """
        Get answer in specific language
        
        Args:
            question: Medical question
            target_language: Language code
            
        Returns:
            Answer in target language
        """
        result = self.answer_question(question)
        
        if target_language == 'en':
            return result['english_answer']
        
        # Translate to target language
        translation = self.translator.translate(
            result['english_answer'], 'en', target_language
        )
        
        return translation['translated_text']
    
    def answer_in_multiple_languages(self, question: str,
                                     languages: List[str]) -> Dict:
        """
        Get answer in multiple languages
        
        Args:
            question: Medical question
            languages: List of language codes
            
        Returns:
            Dictionary with answers in multiple languages
        """
        print(f"🌍 Generating answers in {len(languages)} languages...")
        
        # Get English answer first
        result = self.answer_question(question, 'en')
        english_answer = result['english_answer']
        
        answers = {'en': english_answer}
        
        # Translate to other languages
        for lang in languages:
            if lang == 'en':
                continue
            
            translation = self.translator.translate(
                english_answer, 'en', lang
            )
            answers[lang] = translation['translated_text']
        
        return {
            'question': question,
            'answers': answers,
            'languages': list(answers.keys()),
            'total_languages': len(answers)
        }
    
    def get_statistics(self) -> Dict:
        """Get chatbot statistics"""
        return {
            'total_conversations': len(self.conversation_history),
            'languages_used': dict(self.language_stats),
            'most_common_language': max(
                self.language_stats.items(),
                key=lambda x: x[1]
            ) if self.language_stats else None,
            'supported_languages': len(self.detector.get_supported_languages())
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✅ History cleared")
    
    def get_supported_languages(self) -> Dict:
        """Get all supported languages"""
        return self.detector.get_supported_languages()


# Example usage
if __name__ == "__main__":
    print("🏥 Multilingual Medical Chatbot Example\n")
    print("="*70)
    
    # Initialize
    chatbot = MultilingualChatbot()
    
    # Test with different languages
    test_questions = [
        ("What is diabetes?", "en"),
        ("What is asthma?", "en"),
    ]
    
    print("\n📝 Multilingual Q&A Examples:\n")
    
    for question, lang in test_questions:
        print(f"Question ({lang}): {question}")
        
        result = chatbot.answer_question(question, lang)
        
        print(f"Answer ({lang}): {result['translated_answer'][:100]}...")
        print()
    
    # Statistics
    print("\n📊 Statistics:")
    stats = chatbot.get_statistics()
    print(f"Total conversations: {stats['total_conversations']}")
    print(f"Languages used: {stats['languages_used']}")
    
    print("\n" + "="*70)
