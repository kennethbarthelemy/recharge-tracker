# Data Processing Scripts

Python scripts for extracting and analyzing Apple Health data.

## Prerequisites
```bash
pip install -r ../requirements.txt
```

## Usage

### Step 1: Export Your Apple Health Data

1. Open **Health app** on iPhone
2. Tap your **profile picture** (top right)
3. Tap **"Export All Health Data"**
4. Save and transfer `export.xml` to this folder

### Step 2: Extract Data to CSV
```bash
python extract_health_data.py
```

**Output:** Creates 4 CSV files:
- `hrv.csv` - Heart Rate Variability data
- `resting_hr.csv` - Resting heart rate data
- `sleep.csv` - Sleep analysis data
- `calories.csv` - Active calories burned

**Note:** By default extracts last 90 days. Edit the script to change duration.

### Step 3: Analyze Recovery Metrics
```bash
python analyze_recovery.py
```

**Output:** Displays:
- Recovery Score (0-100%)
- Strain Score (0-21)
- Personalized strain target
- Daily recommendation
- JSON output for app integration

## How It Works

### Recovery Score Formula (0-100%)

**Components:**
- **40% Sleep** - Based on duration vs 8-hour optimal
- **40% HRV** - Compared to your 30-day baseline
- **20% Resting HR** - Compared to your 30-day baseline

**Interpretation:**
- 70-100%: Ready for intense training
- 50-69%: Moderate activity recommended
- 0-49%: Prioritize rest and recovery

### Strain Score (0-21)

Based on active calories burned throughout the day.
- Roughly: 50 calories = 1 strain point
- Capped at 21 for ultra-endurance activities

### Personalized Targets

Your recommended strain range adjusts based on recovery:
- High recovery (70-100%) → Target: 15-18
- Moderate recovery (50-69%) → Target: 10-14
- Low recovery (0-49%) → Target: 6-9

## Example Output
```json
{
  "recovery_score": 60,
  "strain_score": 10.7,
  "strain_target": "10-14",
  "recommendation": "Moderate activity recommended. Listen to your body.",
  "metrics": {
    "sleep": {
      "hours": 7,
      "minutes": 30
    },
    "hrv": {
      "value": 44.0,
      "baseline": 49.5,
      "vs_baseline_pct": -11.1
    },
    "resting_hr": {
      "value": 63,
      "baseline": 62,
      "vs_baseline_bpm": 1
    },
    "calories": 533
  }
}
```

## Technical Notes

- Uses timezone-aware datetime handling (UTC)
- 30-day rolling baselines for personalization
- Sleep data capped at 12 hours to handle export inconsistencies
- Efficient XML parsing for large files (2GB+)

## Privacy Note

**Do not commit your actual health data files (`export.xml`, CSV files) to GitHub!**  
These contain sensitive personal health information.
```

