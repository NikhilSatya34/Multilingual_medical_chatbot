"""
Multilingual Medical Chatbot - Streamlit App
Beautiful web interface for multi-language medical Q&A
"""

import streamlit as st
import os
from dotenv import load_dotenv
from multilingual_chatbot_fixed import MultilingualChatbot
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multilingual Medical Chatbot",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .language-button { margin: 5px; }
    .stats-box { padding: 15px; background-color: #f0f8ff; border-radius: 10px; margin: 10px 0; }
    .answer-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #4caf50;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        margin: 20px 0;
        font-size: 16px;
        line-height: 1.8;
        color: #1b5e20;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chatbot_initialized" not in st.session_state:
    with st.spinner("🌍 Initializing Multilingual Chatbot..."):
        try:
            API_KEY = os.getenv("GEMINI_API_KEY")
            if not API_KEY:
                st.error("❌ GEMINI_API_KEY not found!")
                st.stop()
            
            st.session_state.chatbot = MultilingualChatbot(API_KEY)
            st.session_state.chatbot_initialized = True
            st.session_state.messages = []
            st.session_state.selected_language = "en"
        except Exception as e:
            st.error(f"❌ Initialization failed: {str(e)}")
            st.stop()

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🌍")
with col2:
    st.markdown("# Multilingual Medical Chatbot")
    st.markdown("*Ask medical questions in 20+ languages*")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🌐 Multi-Language", "📊 Statistics", "ℹ️ About"])

# ========== TAB 1: CHAT ==========
with tab1:
    st.subheader("Ask a Medical Question")
    
    # Sidebar settings
    with st.sidebar:
        st.markdown("### ⚙️ Chat Settings")
        st.session_state.selected_language = st.selectbox(
            "Select Language",
            options={
                'en': '🇬🇧 English',
                'es': '🇪🇸 Spanish',
                'fr': '🇫🇷 French',
                'de': '🇩🇪 German',
                'pt': '🇵🇹 Portuguese',
                'zh-cn': '🇨🇳 Chinese',
                'ja': '🇯🇵 Japanese',
                'hi': '🇮🇳 Hindi'
            },
            format_func=lambda x: {
                'en': '🇬🇧 English',
                'es': '🇪🇸 Spanish',
                'fr': '🇫🇷 French',
                'de': '🇩🇪 German',
                'pt': '🇵🇹 Portuguese',
                'zh-cn': '🇨🇳 Chinese',
                'ja': '🇯🇵 Japanese',
                'hi': '🇮🇳 Hindi'
            }[x]
        )
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_question = st.text_input(
            "Enter your medical question:",
            placeholder="Ask in any language...",
            label_visibility="collapsed"
        )
    with col2:
        submit = st.button("🔍 Ask", use_container_width=True)
    
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.rerun()
    
    if submit and user_question:
        with st.spinner("🔄 Processing..."):
            result = st.session_state.chatbot.answer_question(
                user_question,
                st.session_state.selected_language
            )
        
        st.session_state.messages.append(result)
    
    # Display conversation
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("📋 Conversation History")
        
        for i, msg in enumerate(st.session_state.messages, 1):
            with st.container():
                st.markdown(f"### ❓ Q{i}: {msg['original_question']}")
                
                # Language info
                lang_info = msg['language_info']
                st.markdown(f"*Language: {lang_info['flag']} {lang_info['language_name']} ({lang_info['confidence']}%)*")
                
                # Answer
                st.markdown("#### 🤖 Answer:")
                st.markdown(f"<div class='answer-box'>{msg['translated_answer']}</div>", 
                           unsafe_allow_html=True)
                
                # English version
                with st.expander("📝 View in English"):
                    st.markdown(msg['english_answer'])
                
                st.markdown("---")

# ========== TAB 2: MULTI-LANGUAGE ==========
with tab2:
    st.subheader("🌐 Get Answer in Multiple Languages")
    
    question = st.text_input(
        "Enter a medical question:",
        placeholder="Ask once, get answers in multiple languages"
    )
    
    # Select languages
    available_langs = {
        'en': '🇬🇧 English',
        'es': '🇪🇸 Spanish',
        'fr': '🇫🇷 French',
        'de': '🇩🇪 German',
        'pt': '🇵🇹 Portuguese',
        'zh-cn': '🇨🇳 Chinese',
        'ja': '🇯🇵 Japanese'
    }
    
    selected_languages = st.multiselect(
        "Select languages for translation:",
        options=list(available_langs.keys()),
        default=['en', 'es', 'fr'],
        format_func=lambda x: available_langs[x]
    )
    
    if st.button("🌍 Translate"):
        if question and selected_languages:
            with st.spinner("🔄 Translating to multiple languages..."):
                result = st.session_state.chatbot.answer_in_multiple_languages(
                    question,
                    selected_languages
                )
            
            st.success(f"✅ Answer available in {result['total_languages']} languages!")
            
            # Display answers
            cols = st.columns(min(2, len(result['answers'])))
            
            for idx, (lang, answer) in enumerate(result['answers'].items()):
                with cols[idx % len(cols)]:
                    flag = available_langs.get(lang, '🌐')
                    st.markdown(f"### {flag}")
                    st.markdown(answer)

# ========== TAB 3: STATISTICS ==========
with tab3:
    st.subheader("📊 Chatbot Statistics")
    
    stats = st.session_state.chatbot.get_statistics()
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Questions", stats['total_conversations'])
    with col2:
        st.metric("Languages Used", len(stats['languages_used']))
    with col3:
        st.metric("Supported Languages", stats['supported_languages'])
    
    st.markdown("---")
    
    # Language distribution
    if stats['languages_used']:
        st.markdown("### 🗣️ Language Distribution")
        
        lang_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French',
            'de': 'German', 'pt': 'Portuguese', 'zh-cn': 'Chinese',
            'ja': 'Japanese', 'hi': 'Hindi'
        }
        
        df = pd.DataFrame([
            {'Language': lang_names.get(k, k), 'Count': v}
            for k, v in stats['languages_used'].items()
        ])
        
        st.bar_chart(df.set_index('Language'))

# ========== TAB 4: ABOUT ==========
with tab4:
    st.subheader("ℹ️ About Multilingual Medical Chatbot")
    
    st.markdown("""
    ### 🌍 Supported Languages
    
    - 🇬🇧 English
    - 🇪🇸 Spanish
    - 🇫🇷 French
    - 🇩🇪 German
    - 🇵🇹 Portuguese
    - 🇨🇳 Chinese
    - 🇯🇵 Japanese
    - 🇮🇳 Hindi
    - And 12+ more languages!
    
    ### ✨ Features
    
    ✅ Automatic language detection
    ✅ Real-time translation
    ✅ Multi-language answers
    ✅ Language statistics
    ✅ Medical knowledge integration
    ✅ Beautiful multi-language UI
    
    ### 🛠️ Technology
    
    - Language Detection: langdetect
    - Translation: Google Translate
    - LLM: Google Gemini API
    - Framework: Streamlit
    
    ### ⚠️ Medical Disclaimer
    
    This chatbot provides educational information only.
    **Always consult healthcare professionals for medical advice.**
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌍 Multilingual Medical Chatbot | Week 4 | Elevance Skills Internship</p>
    <p style='font-size: 12px; color: gray;'>⚠️ For educational purposes only.</p>
</div>
""", unsafe_allow_html=True)
