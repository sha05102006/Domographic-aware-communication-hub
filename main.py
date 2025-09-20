import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import time

# Page configuration
st.set_page_config(
    page_title="Demographic-Aware Communication Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.5rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #262730;
        border-radius: 10px;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #262730;
        border-radius: 10px;
        border: 2px solid #e1e5e9;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profiles' not in st.session_state:
    st.session_state.user_profiles = {}
if 'communication_analytics' not in st.session_state:
    st.session_state.communication_analytics = []

@st.cache_resource
def load_granite_model():
    """Load IBM Granite model and tokenizer"""
    try:
        with st.spinner("🚀 Loading IBM Granite Model... This may take a few minutes on first load."):
            tokenizer = AutoTokenizer.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
            model = AutoModelForCausalLM.from_pretrained("ibm-granite/granite-3.3-2b-instruct")
            
            # Move to GPU if available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
            
        return tokenizer, model, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

def generate_response(prompt, demographic_context="", max_tokens=200):
    """Generate response using IBM Granite model"""
    if not st.session_state.model_loaded:
        st.error("Model not loaded. Please wait for model initialization.")
        return "Model not available"
    
    try:
        tokenizer, model, device = st.session_state.granite_components
        
        # Create context-aware prompt
        system_prompt = f"""You are a demographic-aware communication assistant. 
        Demographic Context: {demographic_context}
        
        Please provide a response that is culturally sensitive, appropriate for the target demographic, 
        and professionally crafted. Consider factors like age, cultural background, communication style preferences, 
        and professional context when generating your response."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        return response.strip()
        
    except Exception as e:
        return f"Error generating response: {str(e)}"

def analyze_communication_style(text):
    """Analyze communication style using pattern matching"""
    analysis = {
        'formality': 'neutral',
        'tone': 'neutral',
        'complexity': 'medium',
        'key_phrases': [],
        'sentiment': 'neutral'
    }
    
    # Formality analysis
    formal_indicators = ['please', 'thank you', 'regards', 'sincerely', 'respectfully']
    informal_indicators = ['hey', 'yeah', 'cool', 'awesome', 'thanks']
    
    formal_count = sum(1 for word in formal_indicators if word in text.lower())
    informal_count = sum(1 for word in informal_indicators if word in text.lower())
    
    if formal_count > informal_count:
        analysis['formality'] = 'formal'
    elif informal_count > formal_count:
        analysis['formality'] = 'informal'
    
    # Tone analysis
    positive_words = ['great', 'excellent', 'wonderful', 'amazing', 'fantastic']
    negative_words = ['bad', 'terrible', 'awful', 'disappointing', 'poor']
    
    positive_count = sum(1 for word in positive_words if word in text.lower())
    negative_count = sum(1 for word in negative_words if word in text.lower())
    
    if positive_count > negative_count:
        analysis['tone'] = 'positive'
    elif negative_count > positive_count:
        analysis['tone'] = 'negative'
    
    # Complexity analysis
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    if avg_sentence_length > 20:
        analysis['complexity'] = 'high'
    elif avg_sentence_length < 10:
        analysis['complexity'] = 'low'
    
    return analysis

# Main App
def main():
    st.markdown('<h1 class="main-header">🌍 Demographic-Aware Communication Hub</h1>', unsafe_allow_html=True)
    
    # Load model if not already loaded
    if not st.session_state.model_loaded:
        tokenizer, model, device = load_granite_model()
        if tokenizer and model:
            st.session_state.granite_components = (tokenizer, model, device)
            st.session_state.model_loaded = True
            st.success("✅ IBM Granite Model loaded successfully!")
            st.rerun()
    
    # Sidebar for navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/128/15581/15581407.png", width=300)
    
    feature = st.sidebar.selectbox(
        "🚀 Choose Feature",
        [
            "📝 Smart Message Composer",
            "🎯 Demographic Profiler",
            "💬 Conversation Optimizer",
            "📊 Communication Analytics",
            "🌐 Cultural Adaptation Engine",
            "🔍 Message Tone Analyzer"
        ]
    )
    
    # Feature 1: Smart Message Composer
    if feature == "📝 Smart Message Composer":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Smart Message Composer")
        st.markdown("Craft messages tailored to specific demographics with AI assistance")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            message_type = st.selectbox(
                "Message Type",
                ["Professional Email", "Marketing Copy", "Customer Support", "Social Media Post", "Presentation Script"]
            )
            
            target_demographic = st.multiselect(
                "Target Demographics",
                ["Young Adults (18-25)", "Professionals (26-40)", "Senior Citizens (60+)", 
                 "Students", "Parents", "Tech-Savvy", "Traditional", "Urban", "Rural"]
            )
            
            user_input = st.text_area(
                "Your Message Draft",
                placeholder="Enter your message that needs demographic optimization...",
                height=150
            )
            
        with col2:
            st.markdown("### 🎯 Quick Settings")
            tone_preference = st.select_slider(
                "Desired Tone",
                ["Very Formal", "Formal", "Neutral", "Casual", "Very Casual"]
            )
            
            complexity_level = st.select_slider(
                "Language Complexity",
                ["Simple", "Moderate", "Complex", "Technical"]
            )
        
        if st.button("🎨 Optimize Message", type="primary"):
            if user_input and st.session_state.model_loaded:
                demographic_context = f"""
                Target Demographics: {', '.join(target_demographic)}
                Message Type: {message_type}
                Tone Preference: {tone_preference}
                Complexity Level: {complexity_level}
                """
                
                with st.spinner("🤖 IBM Granite AI is optimizing your message..."):
                    optimized_message = generate_response(
                        f"Please optimize this message for the specified demographics: {user_input}",
                        demographic_context
                    )
                
                st.markdown("### ✨ Optimized Message")
                st.success(optimized_message)
                
                # Store in conversation history
                st.session_state.conversation_history.append({
                    'timestamp': datetime.now(),
                    'original': user_input,
                    'optimized': optimized_message,
                    'demographics': target_demographic,
                    'type': message_type
                })
    
    # Feature 2: Demographic Profiler
    elif feature == "🎯 Demographic Profiler":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Demographic Profiler")
        st.markdown("Create detailed profiles for targeted communication")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            profile_name = st.text_input("Profile Name", placeholder="e.g., Tech Startup Audience")
            
            demographics = {
                'age_group': st.selectbox("Age Group", ["18-25", "26-35", "36-45", "46-55", "55+"]),
                'education': st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD", "Professional"]),
                'profession': st.selectbox("Profession", ["Student", "Professional", "Executive", "Entrepreneur", "Retired"]),
                'location': st.selectbox("Location Type", ["Urban", "Suburban", "Rural"]),
                'tech_savviness': st.slider("Tech Savviness", 1, 10, 5),
                'communication_preference': st.selectbox("Preferred Communication Style", 
                                                       ["Direct", "Diplomatic", "Casual", "Formal", "Technical"])
            }
            
            cultural_notes = st.text_area("Cultural Considerations", 
                                        placeholder="Any specific cultural, regional, or contextual notes...")
        
        with col2:
            if st.button("🔬 Generate Profile Analysis", type="primary"):
                if profile_name and st.session_state.model_loaded:
                    profile_prompt = f"""
                    Create a comprehensive communication profile analysis for:
                    Age: {demographics['age_group']}
                    Education: {demographics['education']}
                    Profession: {demographics['profession']}
                    Location: {demographics['location']}
                    Tech Level: {demographics['tech_savviness']}/10
                    Style: {demographics['communication_preference']}
                    Cultural Notes: {cultural_notes}
                    
                    Provide insights on preferred communication channels, message length, tone, timing, and key motivators.
                    """
                    
                    with st.spinner("🧠 Analyzing demographic profile..."):
                        analysis = generate_response(profile_prompt, max_tokens=300)
                    
                    st.markdown("### 📋 Profile Analysis")
                    st.info(analysis)
                    
                    # Save profile
                    st.session_state.user_profiles[profile_name] = {
                        'demographics': demographics,
                        'cultural_notes': cultural_notes,
                        'analysis': analysis,
                        'created': datetime.now()
                    }
        
        # Display saved profiles
        if st.session_state.user_profiles:
            st.markdown("### 💾 Saved Profiles")
            for name, profile in st.session_state.user_profiles.items():
                with st.expander(f"👤 {name}"):
                    st.json(profile['demographics'])
                    if profile.get('analysis'):
                        st.markdown("**Analysis:**")
                        st.write(profile['analysis'])
    
    # Feature 3: Conversation Optimizer
    elif feature == "💬 Conversation Optimizer":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Conversation Optimizer")
        st.markdown("Real-time conversation enhancement and suggestion engine")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Select existing profile or create quick profile
        profile_option = st.radio("Choose Profile", ["Use Existing Profile", "Quick Profile Setup"])
        
        if profile_option == "Use Existing Profile":
            if st.session_state.user_profiles:
                selected_profile = st.selectbox("Select Profile", list(st.session_state.user_profiles.keys()))
                current_profile = st.session_state.user_profiles[selected_profile]
            else:
                st.warning("No saved profiles found. Please create a profile first.")
                current_profile = None
        else:
            st.markdown("#### Quick Profile")
            col1, col2, col3 = st.columns(3)
            with col1:
                quick_age = st.selectbox("Age", ["18-25", "26-40", "40+"])
            with col2:
                quick_context = st.selectbox("Context", ["Business", "Personal", "Educational", "Customer Service"])
            with col3:
                quick_relationship = st.selectbox("Relationship", ["Colleague", "Client", "Friend", "Stranger"])
            
            current_profile = {
                'demographics': {'age_group': quick_age},
                'context': quick_context,
                'relationship': quick_relationship
            }
        
        # Conversation interface
        if current_profile:
            conversation_context = st.text_area(
                "Conversation Context",
                placeholder="Describe the situation or provide background context...",
                height=100
            )
            
            your_message = st.text_area(
                "Your Message",
                placeholder="Type your message here...",
                height=120
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✨ Get Suggestions", type="primary"):
                    if your_message and st.session_state.model_loaded:
                        optimization_prompt = f"""
                        Context: {conversation_context}
                        Target Profile: {current_profile}
                        Original Message: {your_message}
                        
                        Provide 3 optimized versions of this message:
                        1. More Professional
                        2. More Engaging  
                        3. More Concise
                        
                        Also suggest potential responses they might give and how to handle them.
                        """
                        
                        with st.spinner("🎯 Optimizing conversation..."):
                            suggestions = generate_response(optimization_prompt, max_tokens=400)
                        
                        st.markdown("### 💡 Optimization Suggestions")
                        st.success(suggestions)
            
            with col2:
                if st.button("🔍 Analyze Tone"):
                    if your_message:
                        analysis = analyze_communication_style(your_message)
                        
                        st.markdown("### 📊 Message Analysis")
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.metric("Formality", analysis['formality'].title())
                            st.metric("Tone", analysis['tone'].title())
                        
                        with col_b:
                            st.metric("Complexity", analysis['complexity'].title())
    
    # Feature 4: Communication Analytics
    elif feature == "📊 Communication Analytics":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Communication Analytics Dashboard")
        st.markdown("Analyze your communication patterns and effectiveness")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.conversation_history:
            # Analytics overview
            total_messages = len(st.session_state.conversation_history)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Total Messages", total_messages)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                unique_demographics = len(set(str(msg.get('demographics', [])) for msg in st.session_state.conversation_history))
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Unique Demographics", unique_demographics)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                message_types = [msg.get('type', 'Unknown') for msg in st.session_state.conversation_history]
                most_common_type = Counter(message_types).most_common(1)[0][0] if message_types else "None"
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Most Used Type", most_common_type)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                recent_activity = sum(1 for msg in st.session_state.conversation_history 
                                    if (datetime.now() - msg['timestamp']).days < 7)
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("This Week", recent_activity)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Message types distribution
                type_counts = Counter(message_types)
                fig_types = px.pie(
                    values=list(type_counts.values()),
                    names=list(type_counts.keys()),
                    title="Message Types Distribution"
                )
                fig_types.update_layout(showlegend=True)
                st.plotly_chart(fig_types, use_container_width=True)
            
            with col2:
                # Activity over time
                dates = [msg['timestamp'].date() for msg in st.session_state.conversation_history]
                date_counts = Counter(dates)
                
                fig_timeline = px.bar(
                    x=list(date_counts.keys()),
                    y=list(date_counts.values()),
                    title="Communication Activity Timeline"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Recent messages table
            st.markdown("### 📋 Recent Messages")
            recent_messages = st.session_state.conversation_history[-10:]
            
            for i, msg in enumerate(reversed(recent_messages)):
                with st.expander(f"Message {len(recent_messages)-i} - {msg['type']} ({msg['timestamp'].strftime('%Y-%m-%d %H:%M')})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.write(msg['original'][:200] + "..." if len(msg['original']) > 200 else msg['original'])
                    with col2:
                        st.markdown("**Optimized:**")
                        st.write(msg['optimized'][:200] + "..." if len(msg['optimized']) > 200 else msg['optimized'])
                    st.markdown(f"**Demographics:** {', '.join(msg.get('demographics', []))}")
        
        else:
            st.info("No communication data available yet. Start using the Smart Message Composer to see analytics!")
    
    # Feature 5: Cultural Adaptation Engine
    elif feature == "🌐 Cultural Adaptation Engine":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 Cultural Adaptation Engine")
        st.markdown("Adapt your messages for different cultural contexts and regions")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            source_message = st.text_area(
                "Original Message",
                placeholder="Enter your message to be culturally adapted...",
                height=120
            )
            
            source_culture = st.selectbox(
                "Source Culture/Region",
                ["US/North America", "UK/Europe", "East Asia", "South Asia", "Middle East", 
                 "Latin America", "Africa", "Australia/Oceania"]
            )
            
            target_cultures = st.multiselect(
                "Target Cultures/Regions",
                ["US/North America", "UK/Europe", "East Asia", "South Asia", "Middle East", 
                 "Latin America", "Africa", "Australia/Oceania"],
                default=[]
            )
        
        with col2:
            st.markdown("### 🎭 Cultural Considerations")
            considerations = st.multiselect(
                "Focus Areas",
                ["Formality Level", "Direct vs Indirect Communication", "Time Orientation", 
                 "Hierarchy Respect", "Personal Space", "Gift Giving", "Business Etiquette"]
            )
            
            context_type = st.selectbox(
                "Communication Context",
                ["Business Meeting", "Email Correspondence", "Social Interaction", 
                 "Marketing Material", "Customer Service", "Educational Content"]
            )
        
        if st.button("🌍 Generate Cultural Adaptations", type="primary"):
            if source_message and target_cultures and st.session_state.model_loaded:
                for culture in target_cultures:
                    cultural_prompt = f"""
                    Adapt this message from {source_culture} context to {culture} context:
                    
                    Original Message: {source_message}
                    Context: {context_type}
                    Focus Areas: {', '.join(considerations)}
                    
                    Please provide:
                    1. Culturally adapted version
                    2. Key cultural considerations
                    3. Potential cultural pitfalls to avoid
                    4. Suggested delivery method/timing
                    """
                    
                    with st.spinner(f"🌏 Adapting for {culture}..."):
                        adaptation = generate_response(cultural_prompt, max_tokens=350)
                    
                    st.markdown(f"### 🌏 Adaptation for {culture}")
                    st.info(adaptation)
                    st.markdown("---")
    
    # Feature 6: Message Tone Analyzer
    elif feature == "🔍 Message Tone Analyzer":
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Message Tone Analyzer")
        st.markdown("Deep analysis of message tone, sentiment, and communication effectiveness")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analysis_text = st.text_area(
                "Text to Analyze",
                placeholder="Paste the message or conversation you want to analyze...",
                height=200
            )
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Comprehensive Analysis", "Tone Only", "Sentiment Only", "Formality Check", "Readability Assessment"]
            )
        
        with col2:
            st.markdown("### ⚙️ Analysis Settings")
            
            include_suggestions = st.checkbox("Include Improvement Suggestions", value=True)
            compare_demographics = st.checkbox("Compare Against Demographics")
            
            if compare_demographics:
                comparison_demographic = st.selectbox(
                    "Compare Against",
                    ["Young Professionals", "Senior Executives", "Students", "General Public"]
                )
        
        if st.button("🔬 Analyze Message", type="primary"):
            if analysis_text and st.session_state.model_loaded:
                # Basic analysis
                basic_analysis = analyze_communication_style(analysis_text)
                
                # Advanced analysis using Granite
                analysis_prompt = f"""
                Perform a detailed communication analysis of this text:
                
                Text: {analysis_text}
                Analysis Type: {analysis_type}
                
                Please provide:
                1. Tone analysis (professional, casual, friendly, aggressive, etc.)
                2. Sentiment analysis (positive, negative, neutral with intensity)
                3. Formality level and appropriateness
                4. Clarity and readability assessment
                5. Potential audience reception
                6. Communication effectiveness score (1-10)
                {f"7. Specific recommendations for improvement" if include_suggestions else ""}
                {f"8. Suitability for {comparison_demographic}" if compare_demographics else ""}
                """
                
                with st.spinner("🤖 Performing deep analysis..."):
                    detailed_analysis = generate_response(analysis_prompt, max_tokens=400)
                
                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📊 Detailed Analysis")
                    st.success(detailed_analysis)
                
                with col2:
                    st.markdown("### 📈 Quick Metrics")
                    
                    # Create gauge charts
                    formality_score = {"formal": 8, "neutral": 5, "informal": 2}.get(basic_analysis['formality'], 5)
                    complexity_score = {"high": 8, "medium": 5, "low": 2}.get(basic_analysis['complexity'], 5)
                    
                    # Formality gauge
                    fig_formality = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = formality_score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Formality Level"},
                        gauge = {
                            'axis': {'range': [None, 10]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 3], 'color': "lightgray"},
                                {'range': [3, 7], 'color': "gray"},
                                {'range': [7, 10], 'color': "lightgreen"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 8}}))
                    fig_formality.update_layout(height=250)
                    st.plotly_chart(fig_formality, use_container_width=True)
                    
                    # Word count and readability metrics
                    word_count = len(analysis_text.split())
                    sentence_count = len([s for s in analysis_text.split('.') if s.strip()])
                    avg_words_per_sentence = word_count / max(sentence_count, 1)
                    
                    st.metric("Word Count", word_count)
                    st.metric("Sentences", sentence_count)
                    st.metric("Avg Words/Sentence", f"{avg_words_per_sentence:.1f}")
                
                # Store analysis
                st.session_state.communication_analytics.append({
                    'text': analysis_text[:100] + "..." if len(analysis_text) > 100 else analysis_text,
                    'analysis': detailed_analysis,
                    'metrics': basic_analysis,
                    'timestamp': datetime.now()
                })

if __name__ == "__main__":
    main()