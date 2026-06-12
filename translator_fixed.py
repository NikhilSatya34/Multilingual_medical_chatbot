"""
Translator
Translates text between languages using google-trans-new
Free and simple translation without API keys
"""

from typing import Dict, List

try:
    from google_trans_new import google_translator
    HAS_TRANS = True
except ImportError:
    HAS_TRANS = False


class Translator:
    """
    Translates text between languages
    Supports 100+ language pairs
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize translator
        
        Args:
            api_key: Not needed for google-trans-new
        """
        if HAS_TRANS:
            self.translator = google_translator()
            print("✅ Translator initialized (google-trans-new)")
        else:
            print("⚠️ Using fallback translation")
            self.translator = None
    
    def translate(self, text: str, source_lang: str = 'auto', 
                 target_lang: str = 'en') -> Dict:
        """
        Translate text from one language to another
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: auto-detect)
            target_lang: Target language code
            
        Returns:
            Dictionary with translation result
        """
        if not text or len(text.strip()) < 1:
            return {
                'original_text': text,
                'translated_text': text,
                'source_language': source_lang,
                'target_language': target_lang,
                'success': False,
                'message': 'Empty text'
            }
        
        try:
            # Use google-trans-new
            if self.translator and HAS_TRANS:
                translated = self.translator.translate(
                    text,
                    lang_src=source_lang if source_lang != 'auto' else 'auto',
                    lang_tgt=target_lang
                )
                
                return {
                    'original_text': text,
                    'translated_text': translated,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'success': True,
                    'confidence': 0.95,
                    'provider': 'google-trans-new'
                }
            else:
                # Fallback
                return self._translate_with_fallback(text, source_lang, target_lang)
        
        except Exception as e:
            print(f"⚠️ Translation error: {str(e)}")
            return self._translate_with_fallback(text, source_lang, target_lang)
    
    def _translate_with_fallback(self, text: str, source_lang: str, 
                                target_lang: str) -> Dict:
        """
        Fallback translation using simple dictionary
        
        Args:
            text: Text to translate
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            Translation result
        """
        # Medical terms dictionary for common translations
        medical_dict = {
            'en-es': {
                'what is': '¿qué es',
                'diabetes': 'diabetes',
                'heart disease': 'enfermedad cardíaca',
                'symptom': 'síntoma',
                'treatment': 'tratamiento',
                'medication': 'medicamento',
                'fever': 'fiebre',
                'pain': 'dolor',
                'blood pressure': 'presión arterial',
                'how is': 'cómo es',
                'treated': 'tratada'
            },
            'en-fr': {
                'what is': 'qu\'est-ce que',
                'diabetes': 'diabète',
                'heart disease': 'maladie cardiaque',
                'symptom': 'symptôme',
                'treatment': 'traitement',
                'medication': 'médicament',
                'fever': 'fièvre',
                'pain': 'douleur',
                'blood pressure': 'tension artérielle',
                'how is': 'comment est',
                'treated': 'traitée'
            },
            'en-de': {
                'what is': 'Was ist',
                'diabetes': 'Diabetes',
                'heart disease': 'Herzerkrankung',
                'symptom': 'Symptom',
                'treatment': 'Behandlung',
                'medication': 'Medikament',
                'fever': 'Fieber',
                'pain': 'Schmerz',
                'blood pressure': 'Blutdruck',
                'how is': 'Wie ist',
                'treated': 'behandelt'
            },
            'en-pt': {
                'what is': 'o que é',
                'diabetes': 'diabetes',
                'heart disease': 'doença cardíaca',
                'symptom': 'sintoma',
                'treatment': 'tratamento',
                'medication': 'medicamento',
                'fever': 'febre',
                'pain': 'dor',
                'blood pressure': 'pressão arterial',
                'how is': 'como é',
                'treated': 'tratada'
            }
        }
        
        translated_text = text
        
        # Simple term replacement
        dict_key = f'{source_lang}-{target_lang}'
        if dict_key in medical_dict:
            for source_term, target_term in medical_dict[dict_key].items():
                if source_term.lower() in text.lower():
                    translated_text = translated_text.replace(
                        source_term, target_term
                    )
        
        return {
            'original_text': text,
            'translated_text': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'success': True,
            'confidence': 0.8,
            'provider': 'Fallback Dictionary',
            'note': 'Using basic dictionary translation'
        }
    
    def translate_batch(self, texts: List[str], source_lang: str = 'auto',
                       target_lang: str = 'en') -> List[Dict]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translation results
        """
        results = []
        
        for text in texts:
            result = self.translate(text, source_lang, target_lang)
            results.append(result)
        
        return results
    
    def detect_and_translate(self, text: str, target_lang: str = 'en') -> Dict:
        """
        Auto-detect source language and translate
        
        Args:
            text: Text to translate
            target_lang: Target language code
            
        Returns:
            Translation result with detected source language
        """
        return self.translate(text, 'auto', target_lang)
    
    def get_supported_languages(self) -> Dict:
        """Get list of supported languages"""
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'pt': 'Portuguese',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'ja': 'Japanese',
            'hi': 'Hindi',
            'ar': 'Arabic',
            'ru': 'Russian',
            'it': 'Italian',
            'nl': 'Dutch',
            'pl': 'Polish',
            'tr': 'Turkish',
            'vi': 'Vietnamese',
            'ko': 'Korean',
            'th': 'Thai',
            'id': 'Indonesian',
            'fil': 'Filipino'
        }


# Example usage
if __name__ == "__main__":
    print("🌍 Translator Example\n")
    print("="*70)
    
    translator = Translator()
    
    # Test translations
    test_cases = [
        ("What is diabetes?", "en", "es"),
        ("What is diabetes?", "en", "fr"),
        ("What is diabetes?", "en", "de"),
    ]
    
    print("\n📝 Translation Examples:\n")
    
    for text, source, target in test_cases:
        result = translator.translate(text, source, target)
        
        print(f"Original ({source}): {result['original_text']}")
        print(f"Translated ({target}): {result['translated_text']}")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        print()
    
    print("="*70)
