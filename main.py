import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="BluWale", 
    page_icon="🐋", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/bluwale',
        'Report a bug': "https://github.com/your-repo/bluwale/issues",
        'About': "# BluWale\nA gamified water tracking app for UK households"
    }
)

# UK Water Data
UK_DATA = {
    "average_daily": 349,
    "shower_usage": 62,
    "toilet_flush": 33,
    "washing_machine": 50,
    "tips": [
        "Take 4-minute showers to save 50L daily",
        "Fix dripping taps - saves 15L daily", 
        "Only run dishwasher when full - saves 25L",
        "Use a water butt for garden - saves 100L weekly",
        "Install water-efficient toilet - saves 67L daily",
        "Turn off tap while brushing teeth - saves 12L daily",
        "Use a bucket to wash car instead of hose - saves 300L",
        "Install aerator on taps - saves 50% of flow"
    ]
}

# Initialize session state
if 'daily_usage' not in st.session_state:
    st.session_state.daily_usage = 280  # Demo default
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'days_tracked' not in st.session_state:
    st.session_state.days_tracked = 1
if 'completed_tips' not in st.session_state:
    st.session_state.completed_tips = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

# Custom CSS
st.markdown("""
<style>
    /* Global styles for better visibility */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5, #e8f5e8);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main header with bright gradient */
    .main-header {
        background: linear-gradient(135deg, #2196F3, #00BCD4, #4CAF50);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(33, 150, 243, 0.3);
        font-weight: bold;
        font-size: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Bright metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px solid #e3f2fd;
        font-weight: 500;
        color: #2c3e50;
    }
    
    /* Vibrant points display */
    .points-display {
        background: linear-gradient(135deg, #FFD700, #FFA500, #FF6B6B);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: #2c3e50;
        font-weight: bold;
        font-size: 2.2rem;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        border: 3px solid #FFA500;
    }
    
    /* Colorful tip cards */
    .tip-card {
        background: linear-gradient(135deg, #E3F2FD, #F3E5F5, #E8F5E8);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #2196F3;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);
        font-weight: 500;
        color: #2c3e50;
        transition: all 0.3s ease;
    }
    
    .tip-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.3);
    }
    
    /* Bright achievement badges */
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4CAF50, #8BC34A, #CDDC39);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        margin: 0.4rem;
        border: 3px solid #4CAF50;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #4CAF50, #8BC34A);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: bold;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, #2196F3, #03A9F4);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: bold;
    }
    
    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, #FF9800, #FFC107);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2196F3, #00BCD4);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 10px;
    }
    
    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling - bright and colorful */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff, #f8f9fa, #e3f2fd);
        border-right: 3px solid #2196F3;
    }
    
    /* Additional sidebar brightness */
    .css-1lcbmhc {
        background: linear-gradient(180deg, #ffffff, #f8f9fa, #e3f2fd);
    }
    
    /* Sidebar text styling */
    .css-1lcbmhc p, .css-1lcbmhc h1, .css-1lcbmhc h2, .css-1lcbmhc h3 {
        color: #2c3e50;
        font-weight: 500;
    }
    
    /* Make sidebar even brighter */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #ffffff, #f0f8ff, #e3f2fd) !important;
        box-shadow: inset -2px 0 5px rgba(33, 150, 243, 0.1);
    }
    
    /* Sidebar radio buttons styling */
    .css-1lcbmhc .stRadio > div {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border: 2px solid #e3f2fd;
    }
    
    .css-1lcbmhc .stRadio > div:hover {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
        border-color: #2196F3;
        transform: translateX(2px);
        transition: all 0.3s ease;
    }
    
    /* Sidebar navigation text styling - make text white and visible */
    .css-1lcbmhc .stRadio label {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
    }
    
    .css-1lcbmhc .stRadio label:hover {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9) !important;
    }
    
    /* Ensure all sidebar text elements are white */
    .css-1lcbmhc .stRadio div[data-baseweb="radio"] label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    
    /* Additional sidebar text styling */
    .css-1lcbmhc .stRadio * {
        color: #ffffff !important;
    }
    
    /* Better text contrast */
    h1, h2, h4, h5, h6 {
        color: #2c3e50;
        font-weight: bold;
    }
    
    /* H3 headers - blackish color */
    h3 {
        color: #000000 !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Specific targeting for Streamlit elements */
    .stMarkdown h3 {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* Force black color for all h3 elements */
    h3, .stMarkdown h3, .stText h3 {
        color: #000000 !important;
        font-weight: bold !important;
        background-color: rgba(255,255,255,0.9) !important;
        padding: 5px 10px !important;
        border-radius: 5px !important;
        margin: 10px 0 !important;
        display: inline-block !important;
    }
    
    /* Your Impact section styling */
    .stMarkdown h3:contains("Your Impact"), 
    .stMarkdown h3:contains("📊 Your Impact") {
        color: #000000 !important;
        font-weight: bold !important;
        background-color: rgba(255,255,255,0.95) !important;
        padding: 8px 15px !important;
        border-radius: 8px !important;
        margin: 15px 0 !important;
        display: inline-block !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Metric text styling for better visibility */
    .stMetric {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .stMetric label {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .stMetric div {
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    p {
        color: #34495e;
        font-weight: 500;
    }
    
    /* Strong text emphasis */
    strong {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* Logo styling for sidebar */
    .logo-container {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 3px solid #2196F3;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .logo-whale {
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, #87CEEB, #4682B4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem auto;
        box-shadow: 0 8px 25px rgba(135, 206, 235, 0.4);
        border: 4px solid #4682B4;
        overflow: hidden;
    }
    
    .logo-whale img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 10px;
    }
    
    .logo-text {
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)



def create_water_gauge(usage, uk_average=349):
    """Create interactive water usage gauge"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = usage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Daily Water Usage (Litres)", 'font': {'size': 24, 'color': '#2c3e50', 'family': 'Segoe UI'}},
        delta = {'reference': uk_average, 'font': {'size': 18, 'color': '#e74c3c'}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 2, 'tickcolor': "#2196F3", 'tickfont': {'color': '#2c3e50', 'size': 12}},
            'bar': {'color': "#2196F3"},
            'bgcolor': "#f8f9fa",
            'borderwidth': 3,
            'bordercolor': "#2196F3",
            'steps': [
                {'range': [0, 200], 'color': "#4CAF50"},
                {'range': [200, 350], 'color': "#FFC107"},
                {'range': [350, 500], 'color': "#F44336"}],
            'threshold': {
                'line': {'color': "#E91E63", 'width': 5},
                'thickness': 0.8,
                'value': uk_average}}))
    
    fig.update_layout(
        height=450,
        font={'color': "#2c3e50", 'family': "Segoe UI, sans-serif"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def calculate_points(usage, baseline=349):
    """Calculate points based on water savings"""
    if usage < baseline:
        savings = baseline - usage
        base_points = int(savings * 2)  # 2 points per litre saved
        return base_points
    return 0

def check_achievements(total_points, days_tracked):
    """Check and return achievements"""
    achievements = []
    if days_tracked >= 1:
        achievements.append("🎯 First Drop - Started tracking!")
    if total_points >= 100:
        achievements.append("⭐ Water Saver - 100 points earned!")
    if total_points >= 500:
        achievements.append("🏆 Eco Champion - 500 points earned!")
    if days_tracked >= 7:
        achievements.append("📅 Week Warrior - 7 days of tracking!")
    return achievements

def get_personalized_tips(usage):
    """Get personalized tips based on usage"""
    tips = []
    if usage > 300:
        tips.append("🚿 Reduce shower time to 4 minutes - saves 50L daily")
        tips.append("💧 Fix any dripping taps - saves 15L daily")
    if usage > 250:
        tips.append("🧽 Only run dishwasher when full - saves 25L")
        tips.append("🚰 Turn off tap while brushing teeth - saves 12L daily")
    if usage > 200:
        tips.append("🌱 Use a water butt for garden - saves 100L weekly")
        tips.append("🚽 Install water-efficient toilet - saves 67L daily")
    
    # Always include general tips
    tips.extend([
        "🚗 Use a bucket to wash car instead of hose - saves 300L",
        "🔧 Install aerator on taps - saves 50% of flow"
    ])
    
    return tips[:6]  # Return top 6 tips

def show_dashboard():
    """Dashboard page with water meter and usage tracking"""
    st.markdown('<div class="main-header"><h1>🐋 BluWale Dashboard</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Your Water Usage")
        
        # Usage input
        usage = st.slider(
            "Daily Water Usage (Litres)", 
            min_value=0, 
            max_value=500, 
            value=st.session_state.daily_usage,
            help="Adjust to see how your usage compares to UK average"
        )
        st.session_state.daily_usage = usage
        
        # Update points
        today_points = calculate_points(usage)
        st.session_state.total_points += today_points
        
        # Display gauge
        fig = create_water_gauge(usage)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Today's Stats")
        
        # UK comparison
        uk_avg = UK_DATA["average_daily"]
        if usage < uk_avg:
            savings = uk_avg - usage
            percentage = (savings / uk_avg) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎉 Great Job!</h3>
                <p>You used <strong>{savings}L less</strong> than UK average</p>
                <p>That's <strong>{percentage:.1f}% savings!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            excess = usage - uk_avg
            percentage = (excess / uk_avg) * 100
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚠️ Room for Improvement</h3>
                <p>You used <strong>{excess}L more</strong> than UK average</p>
                <p>That's <strong>{percentage:.1f}% above average</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Points display
        st.markdown(f"""
        <div class="points-display">
            <div>🎯 Today's Points</div>
            <div>{today_points}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("""
        <div class="metric-card">
            <h4>📊 UK Water Facts</h4>
            <p>• Average daily usage: 349L</p>
            <p>• Shower: 62L per use</p>
            <p>• Toilet flush: 33L per use</p>
            <p>• Washing machine: 50L per cycle</p>
        </div>
        """, unsafe_allow_html=True)

def show_rewards():
    """Points and rewards page"""
    st.markdown('<div class="main-header"><h1>🐋 BluWale Rewards</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Your Progress")
        
        # Total points display
        st.markdown(f"""
        <div class="points-display">
            <div>Total Points</div>
            <div>{st.session_state.total_points}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress to next tier
        next_tier = 100
        if st.session_state.total_points >= 100:
            next_tier = 500
        if st.session_state.total_points >= 500:
            next_tier = 1000
            
        progress = min(st.session_state.total_points / next_tier, 1.0)
        st.progress(progress)
        st.write(f"Progress to next tier: {st.session_state.total_points}/{next_tier} points")
        
        # Days tracked
        st.metric("Days Tracked", st.session_state.days_tracked)
    
    with col2:
        st.subheader("🏅 Achievements")
        
        # Check for new achievements
        current_achievements = check_achievements(st.session_state.total_points, st.session_state.days_tracked)
        st.session_state.achievements = current_achievements
        
        for achievement in current_achievements:
            st.markdown(f'<div class="achievement-badge">{achievement}</div>', unsafe_allow_html=True)
        
        st.subheader("🎁 Available Rewards")
        
        # Reward tiers
        if st.session_state.total_points >= 50:
            st.success("✅ £5 Water Bill Discount Voucher")
        if st.session_state.total_points >= 100:
            st.success("✅ Free Water-Saving Shower Head")
        if st.session_state.total_points >= 500:
            st.success("✅ £25 Home Improvement Voucher")
        if st.session_state.total_points >= 1000:
            st.success("✅ Free Smart Water Meter Installation")
        
        # Demo: Add points button
        if st.button("🎯 Add Demo Points (+50)"):
            st.session_state.total_points += 50
            st.rerun()

def show_tips():
    """Water saving tips page"""
    st.markdown('<div class="main-header"><h1>🐋 BluWale Tips</h1></div>', unsafe_allow_html=True)
    
    # Get personalized tips
    tips = get_personalized_tips(st.session_state.daily_usage)
    
    st.subheader(f"🎯 Personalized Tips for {st.session_state.daily_usage}L Daily Usage")
    
    for i, tip in enumerate(tips):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div class="tip-card">
                <h4>{tip}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            tip_id = f"tip_{i}"
            if tip_id not in st.session_state.completed_tips:
                if st.button("✅ Done", key=f"done_{i}"):
                    st.session_state.completed_tips.append(tip_id)
                    st.session_state.total_points += 10  # Bonus points
                    st.rerun()
            else:
                st.success("✅ Completed")
    
    st.subheader("📊 Your Impact")
    
    # Calculate total savings
    uk_avg = UK_DATA["average_daily"]
    daily_savings = max(0, uk_avg - st.session_state.daily_usage)
    weekly_savings = daily_savings * 7
    monthly_savings = daily_savings * 30
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Savings", f"{daily_savings}L")
    with col2:
        st.metric("Weekly Savings", f"{weekly_savings}L")
    with col3:
        st.metric("Monthly Savings", f"{monthly_savings}L")
    
    # Environmental impact
    if daily_savings > 0:
        st.info(f"🌍 You're saving enough water daily to fill {daily_savings//10} buckets! Keep up the great work!")

# Display logo using Streamlit's image function
import os
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.markdown("🐋", help="BluWale Logo")
    st.sidebar.error(f"Logo not found at: {logo_path}")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🏆 Points & Rewards", "💡 Water Tips"],
    index=0
)

# Page routing
if "Dashboard" in page:
    show_dashboard()
elif "Points" in page:
    show_rewards()
else:
    show_tips()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="
    background: linear-gradient(135deg, #E3F2FD, #F3E5F5);
    padding: 1rem;
    border-radius: 10px;
    border: 2px solid #2196F3;
    margin-top: 2rem;
">
<p style="color: #2c3e50; font-weight: bold; margin: 0;">🐋 BluWale</p>
<p style="color: #34495e; margin: 0.5rem 0;">Helping UK households save water daily</p>
<p style="color: #7f8c8d; font-style: italic; margin: 0;">Join 1000+ households already saving water!</p>
</div>
""", unsafe_allow_html=True) 