# Recovery Score Algorithm

## Overview

ReCharge calculates a daily recovery score (0-100%) to help athletes determine their training readiness. The algorithm analyzes three key physiological markers and compares them to your personal 30-day baseline.

## The Formula
```
Recovery Score = (Sleep × 0.40) + (HRV × 0.40) + (Resting HR × 0.20)
```

### Why These Weights?

- **40% Sleep**: Primary recovery mechanism - your body repairs during sleep
- **40% HRV**: Most sensitive indicator of nervous system recovery
- **20% Resting HR**: Confirms overall cardiovascular recovery

---

## Component 1: Sleep Score (40% weight)

### What We Measure
- **Duration**: Total sleep time from previous night
- **Optimal Range**: 7-9 hours

### Calculation
```python
sleep_score = min(100, max(0, (sleep_hours / 8) * 100))
```

### Examples
| Sleep Duration | Sleep Score | Contribution to Recovery |
|---------------|-------------|-------------------------|
| 8 hours       | 100         | 40 points               |
| 7 hours       | 87.5        | 35 points               |
| 6 hours       | 75          | 30 points               |
| 5 hours       | 62.5        | 25 points               |

### Why Sleep Matters
- Tissue repair and muscle growth occur during deep sleep
- Insufficient sleep impairs performance by 10-30%
- Chronic sleep debt leads to overtraining syndrome

---

## Component 2: HRV Score (40% weight)

### What We Measure
- **Metric**: Heart Rate Variability (SDNN) in milliseconds
- **Baseline**: Your personal 30-day average
- **Comparison**: Today's HRV vs your baseline

### Calculation
```python
hrv_baseline = mean(last_30_days_hrv)
hrv_vs_baseline_pct = ((today_hrv - hrv_baseline) / hrv_baseline) * 100
hrv_score = min(100, max(0, 50 + (hrv_vs_baseline_pct * 2)))
```

### Examples
| Today's HRV | Baseline | % Change | HRV Score | Contribution |
|-------------|----------|----------|-----------|--------------|
| 60 ms       | 50 ms    | +20%     | 90        | 36 points    |
| 50 ms       | 50 ms    | 0%       | 50        | 20 points    |
| 40 ms       | 50 ms    | -20%     | 10        | 4 points     |

### Why HRV Matters
- **High HRV** = Parasympathetic (rest/digest) dominance → Ready to train
- **Low HRV** = Sympathetic (fight/flight) dominance → Need recovery
- HRV drops with:
  - Stress (physical or mental)
  - Illness/inflammation
  - Overtraining
  - Poor sleep
  - Alcohol consumption

### Why Personal Baseline?
HRV varies widely between individuals (20-100+ ms). A "good" HRV for one person might be "low" for another. **Your recovery is about YOUR normal, not population averages.**

---

## Component 3: Resting Heart Rate Score (20% weight)

### What We Measure
- **Metric**: Resting heart rate in beats per minute (bpm)
- **Baseline**: Your personal 30-day average
- **Comparison**: Today's RHR vs your baseline

### Calculation
```python
rhr_baseline = mean(last_30_days_rhr)
rhr_vs_baseline_bpm = today_rhr - rhr_baseline
rhr_score = min(100, max(0, 50 - (rhr_vs_baseline_bpm * 5)))
```

### Examples
| Today's RHR | Baseline | Difference | RHR Score | Contribution |
|-------------|----------|------------|-----------|--------------|
| 55 bpm      | 58 bpm   | -3 bpm     | 65        | 13 points    |
| 58 bpm      | 58 bpm   | 0 bpm      | 50        | 10 points    |
| 63 bpm      | 58 bpm   | +5 bpm     | 25        | 5 points     |

### Why Resting HR Matters
- **Lower than baseline** = Well recovered, cardiovascular system relaxed
- **Higher than baseline** = Body under stress, still recovering
- RHR increases with:
  - Overtraining
  - Dehydration
  - Illness
  - Heat stress
  - Insufficient recovery

### Why Lower Weight (20%)?
RHR is less sensitive than HRV for detecting early fatigue, but serves as a confirming metric.

---

## Interpreting Your Recovery Score

### Score Ranges

| Score   | Status    | Training Recommendation |
|---------|-----------|------------------------|
| 70-100% | **Green** | Ready for high-intensity training, PRs, race efforts |
| 50-69%  | **Yellow** | Moderate training okay, avoid max efforts |
| 0-49%   | **Red**    | Prioritize rest, active recovery only |

### Example Scenarios

**Scenario 1: Great Recovery (85%)**
- Sleep: 8h 15m → 40 points
- HRV: 65ms (baseline 55ms, +18%) → 36 points
- RHR: 54 bpm (baseline 58 bpm, -4 bpm) → 10 points
- **Total: 86%** → Green light for hard training!

**Scenario 2: Moderate Recovery (60%)**
- Sleep: 6h 45m → 34 points
- HRV: 48ms (baseline 55ms, -13%) → 24 points
- RHR: 60 bpm (baseline 58 bpm, +2 bpm) → 10 points
- **Total: 68%** → Stick to moderate intensity

**Scenario 3: Poor Recovery (35%)**
- Sleep: 5h 30m → 28 points
- HRV: 38ms (baseline 55ms, -31%) → 12 points
- RHR: 65 bpm (baseline 58 bpm, +7 bpm) → 15 points
- **Total: 55%** → Take a rest day or light activity only

---

## Strain Score & Target

### Strain Calculation
```python
strain_score = min(21, calories_burned / 50)
```

**Scale**: 0-21 (based on Whoop's scale)
- 0-5: Light day
- 6-10: Moderate activity
- 11-15: Strenuous training
- 16-21: All-out effort

### Dynamic Strain Targets

Your recommended strain adjusts based on recovery:

| Recovery Score | Strain Target | Meaning |
|---------------|---------------|---------|
| 70-100%       | 15-18         | Push hard, you're ready |
| 50-69%        | 10-14         | Moderate training |
| 0-49%         | 6-9           | Active recovery only |

**Example**: If your recovery is 60% and you're at strain 10.7 (target 10-14), you're training appropriately for your recovery state.

---

## Scientific Basis

### Research Support

**HRV & Recovery:**
- Plews et al. (2013): HRV-guided training improved performance vs fixed training plans
- Buchheit (2014): HRV monitoring helps prevent overtraining syndrome

**Sleep & Performance:**
- Mah et al. (2011): Extended sleep improved athletic performance by 5-11%
- Fullagar et al. (2015): Sleep deprivation reduces endurance by 10-30%

**Resting HR:**
- Achten & Jeukendrup (2003): RHR elevation indicates incomplete recovery
- Borresen & Lambert (2008): RHR monitoring helps detect overtraining

### Limitations

1. **Acute illness**: Algorithm can't distinguish between overtraining and sickness
2. **Alcohol**: May artificially suppress HRV without improving recovery
3. **Medications**: Some medications affect HR/HRV independent of recovery
4. **Data quality**: Requires consistent Apple Watch wear during sleep

---

## Future Improvements

**Planned enhancements:**
- Integration of workout load trends (7-day, 28-day strain)
- Sleep stage analysis (deep/REM percentage)
- HRV during sleep vs morning comparison
- Machine learning for personalized weights based on individual response patterns

---

## References

- Buchheit, M. (2014). Monitoring training status with HR measures. *Sports Medicine*
- Plews, D.J., et al. (2013). Training adaptation with HRV-guided training. *International Journal of Sports Physiology and Performance*
- Mah, C.D., et al. (2011). The effects of sleep extension on athletic performance. *Sleep*
- Achten, J., & Jeukendrup, A.E. (2003). Heart rate monitoring. *Sports Medicine*
```
