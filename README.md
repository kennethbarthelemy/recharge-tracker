# ReCharge - Apple Watch Recovery Tracker

> Daily recovery and strain insights using your Apple Watch data - built in 24 hours at [Buildathon Name]

<img width="548" height="970" alt="image" src="https://github.com/user-attachments/assets/0cff3726-9fb0-4caa-b534-e0a1357fb775" />


## 🎯 The Problem

Athletes using Whoop pay $240/year for recovery tracking, but 100M+ people already own Apple Watches with the same sensors. ReCharge delivers the same insights for free.

## 💡 What It Does

- **Recovery Score (0-100%)**: Calculated from HRV, resting heart rate, and sleep quality
- **Daily Strain Score (0-21)**: Tracks training intensity and calorie burn
- **Personalized Targets**: Recommends optimal training intensity based on recovery
- **Real-Time Data**: Uses actual Apple HealthKit data (not mock data)

## 🛠️ Tech Stack

- **Frontend**: Lovable.dev (React)
- **Data Processing**: Python (pandas, xml parsing)
- **Data Source**: Apple HealthKit export (2GB XML → CSV)
- **Analysis**: Custom recovery algorithms based on HRV/sleep/HR metrics

## 📊 My Actual Results

![My Recovery Data](my-data-screenshot.png)

Using my own Apple Watch data:
- Recovery Score: 60% (moderate - HRV down 11% from baseline)
- Strain: 10.7/21 (within recommended range)
- Recommendation: Moderate training intensity

## 🚀 Key Features

1. **Real Data Integration**: Successfully parsed 2GB Apple Health export
2. **Smart Algorithms**: 30-day baseline calculations for personalized insights
3. **Actionable Insights**: Clear daily recommendations (rest/moderate/push hard)
4. **Fast Build**: Fully functional prototype in <24 hours

## 🔮 Next Steps

- [ ] Native iOS app with live HealthKit integration
- [ ] 7-day trend visualization
- [ ] Workout recommendations based on recovery
- [ ] Beta testing with 100+ users

## 📝 What I Learned

- Apple HealthKit data structure and export process
- Real-time health data analysis and baseline calculations
- Rapid prototyping under time constraints
- Product design for health/fitness applications

## 🏆 Built At

[Buildathon Name] - November 2025

---

**Live Demo**: https://rechargenow.lovable.app
**Pitch Deck**: https://www.canva.com/design/DAG4y3TgWzA/N8gIX3ixsgL14_MnA6AWGA/edit?utm_content=DAG4y3TgWzA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
