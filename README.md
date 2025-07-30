# 🐋 BluWale

A gamified water tracking app helping UK households reduce water consumption through interactive dashboards, points systems, and personalized tips.

## 🚀 Quick Start

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**

   ```bash
   streamlit run main.py
   ```

3. **Open Browser**
   Navigate to `http://localhost:8501`

## 🎯 Demo Script (30 seconds)

**"Meet BluWale - helping reduce household water consumption"**

1. **Dashboard**: Show meter, input 280L usage, highlight 20% savings
2. **Points**: "You earned 138 points today! Unlock rewards"
3. **Tips**: "Personalized suggestions based on your usage"
4. **Impact**: "Join 1000+ UK households saving water daily"

## ✨ Core Features

### 📊 Dashboard

- **Interactive Water Gauge**: Circular plotly gauge with color zones (green/yellow/red)
- **UK Comparison**: Real-time comparison to UK average (349L daily)
- **Points Calculation**: 2 points per litre saved below average
- **Usage Input**: Slider for daily consumption (0-500L)

### 🏆 Points & Rewards

- **Points Display**: Large animated points counter
- **Progress Bars**: Visual progress to next reward tier
- **Achievement Badges**: 4 unlockable achievements
- **Reward Tiers**: £5 vouchers, shower heads, smart meters

### 💡 Water Tips

- **Personalized Tips**: Context-aware suggestions based on usage
- **Quick Actions**: "Mark as Done" buttons with bonus points
- **Savings Calculator**: Daily/weekly/monthly impact metrics
- **Environmental Impact**: Bucket equivalents saved

## 🎨 Design Features

- **Water Theme**: Blue gradient headers and water-themed colors
- **Responsive Layout**: Wide layout with sidebar navigation
- **Interactive Elements**: Hover effects and smooth transitions
- **Mobile Friendly**: Optimized for all screen sizes

## 📊 UK Water Data

- **Average Daily Usage**: 349 litres
- **Shower Usage**: 62L per use
- **Toilet Flush**: 33L per use
- **Washing Machine**: 50L per cycle

## 🎮 Gamification System

### Points Calculation

- **Base Points**: 2 points per litre saved below UK average
- **Bonus Points**: 10 points for completing tips
- **Demo Points**: +50 points button for testing

### Achievement Tiers

- 🎯 **First Drop**: Started tracking (1 day)
- ⭐ **Water Saver**: 100 points earned
- 🏆 **Eco Champion**: 500 points earned
- 📅 **Week Warrior**: 7 days of tracking

### Reward Tiers

- **50 Points**: £5 Water Bill Discount Voucher
- **100 Points**: Free Water-Saving Shower Head
- **500 Points**: £25 Home Improvement Voucher
- **1000 Points**: Free Smart Water Meter Installation

## 🛠 Technical Stack

- **Frontend**: Streamlit 1.28.0
- **Visualization**: Plotly 5.17.0
- **Data Processing**: Pandas 2.1.0
- **Styling**: Custom CSS with water theme

## 📁 Project Structure

```
water_wise/
├── main.py                 # Main Streamlit app (All-in-one)
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🎯 Success Criteria

✅ **Functional**: App runs without errors  
✅ **Visual**: Clean, water-themed design  
✅ **Interactive**: Gauge responds to input changes  
✅ **Gamified**: Points system working  
✅ **Relevant**: UK-specific data and context

## 🚀 Development Timeline

**Phase 1: Foundation (0-20 min)** ✅

- Streamlit app structure with navigation
- Basic CSS styling and water theme

**Phase 2: Core Dashboard (20-50 min)** ✅

- Interactive water gauge with plotly
- UK comparison and points calculation

**Phase 3: Gamification (50-75 min)** ✅

- Points system with achievements
- Personalized tips and rewards

**Phase 4: Polish & Demo Prep (75-90 min)** ✅

- Final UI polish and demo data
- Complete feature testing

## 🌟 Demo Highlights

1. **Start with Dashboard**: Show 280L usage (20% below UK average)
2. **Navigate to Points**: Display 138 points earned today
3. **Show Tips Page**: Personalized suggestions for 280L usage
4. **Demonstrate Interactivity**: Adjust slider to see real-time changes
5. **Highlight Impact**: "Saving 69L daily = 7 buckets of water!"

## 📈 Impact Metrics

- **Daily Savings**: Up to 200L per household
- **Weekly Impact**: 1400L saved per week
- **Monthly Savings**: 6000L per month
- **Environmental**: Equivalent to filling 60 buckets daily

---

_Built with ❤️ for UK water conservation_
