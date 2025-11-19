"""
Recovery Score Calculator
Analyzes Apple Health data to calculate daily recovery and strain scores
"""

import pandas as pd
from datetime import datetime, timedelta
import pytz
import json

def analyze_health_data():
    """
    Analyzes CSV health data and calculates recovery metrics
    
    Returns:
        dict: Recovery score, strain score, and detailed metrics
    """
    
    print("📊 Analyzing your Apple Watch data...\n")
    
    # Load CSV files
    hrv_df = pd.read_csv('hrv.csv')
    rhr_df = pd.read_csv('resting_hr.csv')
    sleep_df = pd.read_csv('sleep.csv')
    cal_df = pd.read_csv('calories.csv')
    
    # Convert dates (timezone-aware)
    hrv_df['date'] = pd.to_datetime(hrv_df['date'], utc=True)
    rhr_df['date'] = pd.to_datetime(rhr_df['date'], utc=True)
    sleep_df['start'] = pd.to_datetime(sleep_df['start'], utc=True)
    sleep_df['end'] = pd.to_datetime(sleep_df['end'], utc=True)
    cal_df['date'] = pd.to_datetime(cal_df['date'], utc=True)
    
    # Time references
    tz = pytz.UTC
    today = datetime.now(tz).date()
    yesterday = today - timedelta(days=1)
    last_30_days = datetime.now(tz) - timedelta(days=30)
    
    print("=" * 50)
    print("TODAY'S METRICS")
    print("=" * 50)
    
    # ========== HRV ANALYSIS ==========
    today_hrv = hrv_df[hrv_df['date'].dt.date == today]
    if len(today_hrv) > 0:
        hrv_value = float(today_hrv['hrv'].iloc[-1])
    else:
        yesterday_hrv = hrv_df[hrv_df['date'].dt.date == yesterday]
        hrv_value = float(yesterday_hrv['hrv'].iloc[-1]) if len(yesterday_hrv) > 0 else 67
    
    hrv_baseline = hrv_df[hrv_df['date'] >= last_30_days]['hrv'].astype(float).mean()
    hrv_vs_baseline_pct = ((hrv_value - hrv_baseline) / hrv_baseline) * 100
    
    print(f"✓ HRV: {hrv_value:.1f} ms")
    print(f"✓ HRV Baseline (30-day): {hrv_baseline:.1f} ms")
    print(f"✓ HRV vs Baseline: {hrv_vs_baseline_pct:+.1f}%")
    
    # ========== RESTING HR ANALYSIS ==========
    today_rhr = rhr_df[rhr_df['date'].dt.date == today]
    if len(today_rhr) > 0:
        rhr_value = float(today_rhr['resting_hr'].iloc[-1])
    else:
        yesterday_rhr = rhr_df[rhr_df['date'].dt.date == yesterday]
        rhr_value = float(yesterday_rhr['resting_hr'].iloc[-1]) if len(yesterday_rhr) > 0 else 58
    
    rhr_baseline = rhr_df[rhr_df['date'] >= last_30_days]['resting_hr'].astype(float).mean()
    rhr_vs_baseline_bpm = rhr_value - rhr_baseline
    
    print(f"✓ Resting HR: {rhr_value:.0f} bpm")
    print(f"✓ RHR Baseline (30-day): {rhr_baseline:.0f} bpm")
    print(f"✓ RHR vs Baseline: {rhr_vs_baseline_bpm:+.0f} bpm")
    
    # ========== SLEEP ANALYSIS ==========
    last_night_sleep = sleep_df[sleep_df['start'].dt.date == yesterday]
    if len(last_night_sleep) > 0:
        sleep_duration = 0
        for _, row in last_night_sleep.iterrows():
            duration = (row['end'] - row['start']).total_seconds() / 3600
            sleep_duration += duration
        # Cap at 12 hours to handle data quality issues
        sleep_hours = min(sleep_duration, 12)
    else:
        sleep_hours = 7.5
    
    sleep_mins = (sleep_hours % 1) * 60
    print(f"✓ Last Night's Sleep: {int(sleep_hours)}h {int(sleep_mins)}m")
    
    # ========== CALORIES ANALYSIS ==========
    today_cal = cal_df[cal_df['date'].dt.date == today]
    calories_burned = today_cal['calories'].astype(float).sum() if len(today_cal) > 0 else 0
    print(f"✓ Active Calories Today: {calories_burned:.0f} kcal")
    
    print("\n" + "=" * 50)
    print("RECOVERY SCORE CALCULATION")
    print("=" * 50)
    
    # ========== RECOVERY SCORE ==========
    # Formula: 40% Sleep + 40% HRV + 20% RHR
    
    # Sleep score (7-9 hours optimal)
    sleep_score = min(100, max(0, (sleep_hours / 8) * 100))
    
    # HRV score (higher than baseline = better)
    hrv_score = min(100, max(0, 50 + (hrv_vs_baseline_pct * 2)))
    
    # RHR score (lower than baseline = better)
    rhr_score = min(100, max(0, 50 - (rhr_vs_baseline_bpm * 5)))
    
    recovery_score = (sleep_score * 0.4) + (hrv_score * 0.4) + (rhr_score * 0.2)
    
    print(f"Recovery Score: {recovery_score:.0f}%")
    print(f"  • Sleep contribution: {sleep_score * 0.4:.0f}")
    print(f"  • HRV contribution: {hrv_score * 0.4:.0f}")
    print(f"  • RHR contribution: {rhr_score * 0.2:.0f}")
    
    # ========== STRAIN SCORE ==========
    strain_score = min(21, (calories_burned / 50))
    print(f"\nStrain Score: {strain_score:.1f}/21")
    
    # ========== STRAIN TARGET ==========
    if recovery_score >= 70:
        strain_target = "15-18"
    elif recovery_score >= 50:
        strain_target = "10-14"
    else:
        strain_target = "6-9"
    print(f"Strain Target: {strain_target}")
    
    # ========== RECOMMENDATION ==========
    if recovery_score >= 70:
        recommendation = "Your body is primed for a hard workout today!"
    elif recovery_score >= 50:
        recommendation = "Moderate activity recommended. Listen to your body."
    else:
        recommendation = "Prioritize rest and recovery today."
    
    print(f"\nRecommendation: {recommendation}")
    
    # Return results as JSON
    results = {
        "recovery_score": round(recovery_score),
        "strain_score": round(strain_score, 1),
        "strain_target": strain_target,
        "recommendation": recommendation,
        "metrics": {
            "sleep": {
                "hours": int(sleep_hours),
                "minutes": int(sleep_mins),
                "total_hours": round(sleep_hours, 1)
            },
            "hrv": {
                "value": round(hrv_value, 1),
                "baseline": round(hrv_baseline, 1),
                "vs_baseline_pct": round(hrv_vs_baseline_pct, 1)
            },
            "resting_hr": {
                "value": round(rhr_value),
                "baseline": round(rhr_baseline),
                "vs_baseline_bpm": round(rhr_vs_baseline_bpm)
            },
            "calories": round(calories_burned)
        }
    }
    
    return results

if __name__ == "__main__":
    # Run analysis and print JSON
    results = analyze_health_data()
    print("\n" + "=" * 50)
    print("JSON OUTPUT")
    print("=" * 50)
    print(json.dumps(results, indent=2))
```
