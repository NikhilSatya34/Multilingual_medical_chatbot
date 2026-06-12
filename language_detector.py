"""
Language Detector
Automatically detects the language of input text
Supports 50+ languages
"""

from typing import Dict, Tuple
import langdetect
from langdetect import detect, detect_langs


class LanguageDetector:
    """
    Detects the language of text input
    Identifies language code and confidence
    """
    
    def __init__(self):
        """Initialize language detector"""
        self.supported_languages = {
            'en': '🇬🇧 English',
            'es': '🇪🇸 Spanish',
            'fr': '🇫🇷 French',
            'de': '🇩🇪 German',
            'pt': '🇵🇹 Portuguese',
            'zh-cn': '🇨🇳 Chinese (Simplified)',
            'zh-tw': '🇨🇳 Chinese (Traditional)',
            'ja': '🇯🇵 Japanese',
            'hi': '🇮🇳 Hindi',
            'ar': '🇸🇦 Arabic',
            'ru': '🇷🇺 Russian',
            'it': '🇮🇹 Italian',
            'nl': '🇳🇱 Dutch',
            'pl': '🇵🇱 Polish',
            'tr': '🇹🇷 Turkish',
            'vi': '🇻🇳 Vietnamese',
            'ko': '🇰🇷 Korean',
            'th': '🇹🇭 Thai',
            'id': '🇮🇩 Indonesian',
            'fil': '🇵🇭 Filipino',
            'te': '🇮🇳 Telugu',
            'ta': '🇮🇳 Tamil',
            'ml': '🇮🇳 Malayalam'
        }
        
        print("✅ Language Detector initialized")
        print(f"   Supported languages: {len(self.supported_languages)}")
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect the language of input text
        
        Args:
            text: Input text to detect
            
        Returns:
            Dictionary with language info
        """
        if not text or len(text.strip()) < 2:
            return {
                'language': 'en',
                'language_name': 'English',
                'confidence': 0.0,
                'is_supported': True,
                'flag': '🇬🇧'
            }
        
        try:
            # Detect language with confidence
            detected_lang = detect(text)
            
            # Get all probability scores
            detected_langs_list = detect_langs(text)
            confidence = max([lang.prob for lang in detected_langs_list]) if detected_langs_list else 0
            
            # Get language name
            language_name = self.supported_languages.get(
                detected_lang,
                detected_lang.upper()
            )
            
            # Check if supported
            is_supported = detected_lang in self.supported_languages
            
            # Get flag emoji
            flag = self._get_flag_emoji(detected_lang)
            
            return {
                'language': detected_lang,
                'language_name': language_name,
                'confidence': round(confidence * 100, 2),
                'is_supported': is_supported,
                'flag': flag,
                'all_probabilities': [
                    {'lang': str(lang).split(':')[0], 'prob': round(lang.prob * 100, 2)}
                    for lang in detected_langs_list
                ]
            }
        
        except Exception as e:
            print(f"⚠️ Detection error: {str(e)}")
            return {
                'language': 'en',
                'language_name': 'English (Default)',
                'confidence': 0.0,
                'is_supported': True,
                'flag': '🇬🇧',
                'error': str(e)
            }
    
    def detect_multiple(self, texts: list) -> list:
        """
        Detect language for multiple texts
        
        Args:
            texts: List of texts
            
        Returns:
            List of detection results
        """
        results = []
        for text in texts:
            result = self.detect_language(text)
            results.append(result)
        
        return results
    
    def _get_flag_emoji(self, language_code: str) -> str:
        """
        Get flag emoji for language code
        
        Args:
            language_code: Language code (e.g., 'en', 'es')
            
        Returns:
            Flag emoji
        """
        flag_map = {
            'en': '🇬🇧',
            'es': '🇪🇸',
            'fr': '🇫🇷',
            'de': '🇩🇪',
            'pt': '🇵🇹',
            'zh': '🇨🇳',
            'zh-cn': '🇨🇳',
            'zh-tw': '🇹🇼',
            'ja': '🇯🇵',
            'hi': '🇮🇳',
            'ar': '🇸🇦',
            'ru': '🇷🇺',
            'it': '🇮🇹',
            'nl': '🇳🇱',
            'pl': '🇵🇱',
            'tr': '🇹🇷',
            'vi': '🇻🇳',
            'ko': '🇰🇷',
            'th': '🇹🇭',
            'id': '🇮🇩',
            'fil': '🇵🇭',
            'te': '🇮🇳',
            'ta': '🇮🇳',
            'ml': '🇮🇳'
        }
        
        return flag_map.get(language_code, '🌐')
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if language is supported for translation
        
        Args:
            language_code: Language code
            
        Returns:
            True if supported
        """
        return language_code in self.supported_languages
    
    def get_supported_languages(self) -> Dict:
        """Get all supported languages"""
        return self.supported_languages
    
    def get_primary_language(self, text: str) -> str:
        """
        Get the primary language code
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'es', 'fr')
        """
        result = self.detect_language(text)
        return result['language']


# Example usage
if __name__ == "__main__":
    print("🌐 Language Detector Example\n")
    print("="*70)
    
    detector = LanguageDetector()
    
    # Test with different languages
    test_texts = [
        "What is diabetes?",  # English
        "¿Qué es la diabetes?",  # Spanish
        "Qu'est-ce que le diabète?",  # French
        "Was ist Diabetes?",  # German
        "O que é diabetes?",  # Portuguese
        "糖尿病是什么?",  # Chinese
    ]
    
    print("\n📊 Language Detection Results:\n")
    
    for text in test_texts:
        result = detector.detect_language(text)
        print(f"Text: {text}")
        print(f"  Language: {result['flag']} {result['language_name']}")
        print(f"  Confidence: {result['confidence']}%")
        print(f"  Supported: {'✅ Yes' if result['is_supported'] else '❌ No'}")
        print()
    
    print("="*70)
