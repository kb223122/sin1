# Data Recovery Guide - After API Quota Error

## 🔍 **Where Your Data Is Saved**

### **1. Sinergym Automatic Logging** ✅ (Saved during run)

Sinergym's `CSVLogger` saves data **during the simulation**, so you have data up to step 6913!

**Location:**
```bash
# Check workspace path
workspace = env.get_wrapper_attr("workspace_path")
# Usually: ./Eplus-env-<name>/output/Eplus-env-<name>-episode-<num>/
```

**Files to look for:**
- `progress.csv` - Episode summaries (cumulative metrics)
- `monitor/monitor.csv` - Per-step observations, actions, rewards
- `monitor/episode-<num>/monitor.csv` - Per-step data for each episode

### **2. Your Custom CSV** ❌ (NOT saved - only saves at end)

Your `llm_run_step_log_linear_prompted_free.csv` is **only saved at the end** after the while loop completes, so it's **NOT saved** when the crash happened.

### **3. In-Memory Data** ❌ (Lost on crash)

`step_records` list was in memory - **lost when program crashed**.

---

## 📂 **How to Find Your Data**

### **Step 1: Find Workspace Directory**

```python
# Run this to find workspace path
import os
from pathlib import Path

# Default locations
possible_paths = [
    "./Eplus-5zone-hot-continuous-v1/",
    "./results_llm_linear_prompted_free_winter/",
    "./output/",
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"Found: {path}")
        # Look for episode folders
        for item in os.listdir(path):
            if "episode" in item.lower():
                print(f"  Episode folder: {os.path.join(path, item)}")
```

### **Step 2: Check for Sinergym CSV Files**

```bash
# Look for monitor CSV (contains per-step data)
find . -name "monitor.csv" -type f

# Look for progress CSV
find . -name "progress.csv" -type f
```

### **Step 3: Extract Data from Monitor CSV**

The `monitor.csv` contains:
- All observations
- All actions
- All rewards
- Per-step data

You can use this to reconstruct your `step_records`!

---

## 🛠️ **Solution: Add Exception Handling**

Add this to your `main()` function to save data even on crashes:

```python
def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    np.random.seed(SEED)
    env = make_env()
    obs, info = env.reset()

    workspace = env.get_wrapper_attr("workspace_path")
    outdir = workspace if isinstance(workspace, str) and len(workspace) > 0 else RESULTS_DIR
    os.makedirs(outdir, exist_ok=True)

    step_size_s = float(env.get_wrapper_attr("step_size"))
    history_for_prompt: List[Dict[str, Any]] = []
    last_indoor_temp = None
    prev_fc1 = None
    prev_occ1 = None
    step_records: List[StepRecord] = []

    print(f"Sinergym version: {sinergym.__version__}")
    print("Starting full-year LLM control …")
    print(f"Saving outputs to: {outdir}")

    step = 0
    terminated = truncated = False
    start_time = time.time()
    
    # ========== ADDED: Save data periodically ==========
    SAVE_INTERVAL = 100  # Save every 100 steps
    step_log_path = os.path.join(outdir, "llm_run_step_log_linear_prompted_free.csv")
    # ===================================================

    try:  # ========== ADDED: Try-except wrapper ==========
        while not (terminated or truncated):
            features = extract_features(env, obs)
            od = features["obs_dict"]
            # ... rest of your loop code ...
            
            step_records.append(record)
            
            # ========== ADDED: Periodic save ==========
            if step % SAVE_INTERVAL == 0 and step > 0:
                _save_step_records_partial(step_records, step_log_path)
                print(f"[AUTO-SAVE] Saved {len(step_records)} records at step {step}")
            # ==========================================
            
            # ... rest of loop ...
            obs = obs_next
            step += 1

    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Saving data before exit...")
        _save_step_records_partial(step_records, step_log_path)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("[RECOVERY] Saving data before exit...")
        _save_step_records_partial(step_records, step_log_path)
        raise  # Re-raise to see full traceback

    finally:  # ========== ADDED: Always save at end ==========
        try:
            env.close()
            elapsed = time.time() - start_time
            print(f"Run finished. Steps={step} elapsed={elapsed/60:.2f} min")
            
            # Save final data
            _save_step_records_final(step_records, outdir, step_log_path)
            
        except Exception as e:
            print(f"[FINAL SAVE ERROR] {e}")
            # Still try to save partial data
            _save_step_records_partial(step_records, step_log_path)
    # ===================================================


def _save_step_records_partial(step_records: List[StepRecord], step_log_path: str):
    """Save step records incrementally (for crash recovery)"""
    if not step_records:
        return
    try:
        df = pd.DataFrame([r.__dict__ for r in step_records])
        # Save with suffix to avoid overwriting
        partial_path = step_log_path.replace('.csv', '_partial.csv')
        df.to_csv(partial_path, index=False)
        print(f"[PARTIAL SAVE] Saved {len(step_records)} records to {partial_path}")
    except Exception as e:
        print(f"[PARTIAL SAVE ERROR] {e}")


def _save_step_records_final(step_records: List[StepRecord], outdir: str, step_log_path: str):
    """Save final step records with all processing"""
    if not step_records:
        print("[WARNING] No step records to save!")
        return
        
    df = pd.DataFrame([r.__dict__ for r in step_records])
    
    # Expand forecast arrays into columns
    for i in range(OCCUPANCY_FORECAST_HOURS):
        df[f"occ_forecast_percent_{i+1}h"] = df["occ_forecast_percent"].apply(
            lambda lst, ix=i: lst[ix] if len(lst) > ix else np.nan
        )
    for i in range(WEATHER_FORECAST_HOURS):
        df[f"drybulb_forecast_{i+1}h"] = df["weather_forecast_temp"].apply(
            lambda lst, ix=i: lst[ix] if len(lst) > ix else np.nan
        )
    
    # Debug columns
    if "dbg_drybulb_keys" in df.columns:
        for i in range(WEATHER_FORECAST_HOURS):
            df[f"drybulb_key_{i+1}"] = df["dbg_drybulb_keys"].apply(
                lambda lst, ix=i: (lst[ix] if isinstance(lst, list) and len(lst) > ix else "")
            )
    if "align_diff_prev_fc1_vs_current_outdoor" in df.columns:
        df["align_diff_fc1_outdoor"] = df["align_diff_prev_fc1_vs_current_outdoor"]
    if "align_diff_prev_occ1_vs_current_occ" in df.columns:
        df["align_diff_occ1_occ"] = df["align_diff_prev_occ1_vs_current_occ"]
    
    df.drop(columns=["occ_forecast_percent", "weather_forecast_temp", "dbg_drybulb_keys",
                     "align_diff_prev_fc1_vs_current_outdoor", "align_diff_prev_occ1_vs_current_occ"],
            inplace=True, errors="ignore")
    
    df.to_csv(step_log_path, index=False)
    print(f"Saved step log to {step_log_path}")
    
    # Generate monthly stats
    monthly_stats = monthly_agg_and_save(df, outdir)
    print(f"Saved monthly stats to {os.path.join(outdir, 'llm_run_monthly_stats.csv')}")
    plot_monthly_graphs(monthly_stats, outdir)
    print("Monthly plots saved.")
```

---

## 📊 **Recover Data from Sinergym Monitor CSV**

If you find `monitor.csv`, you can extract your data:

```python
import pandas as pd

# Load monitor CSV
monitor_df = pd.read_csv("path/to/monitor.csv")

# Extract key columns
# Monitor CSV has: time_elapsed, observations, actions, rewards, etc.
# You'll need to parse the observation/action columns

print(f"Found {len(monitor_df)} steps in monitor CSV")
print(monitor_df.columns.tolist())
```

---

## 🎯 **Quick Recovery Steps**

1. **Find workspace directory:**
   ```bash
   find . -name "monitor.csv" -o -name "progress.csv"
   ```

2. **Check episode folder:**
   ```bash
   ls -la Eplus-5zone-hot-continuous-v1/output/*/episode-*/
   ```

3. **Extract from monitor CSV** (if found)

4. **Add exception handling** to your code for future runs

---

## ✅ **Summary**

- ✅ **Sinergym monitor.csv**: Saved during run (contains per-step data)
- ❌ **Your custom CSV**: NOT saved (only saves at end)
- ❌ **step_records in memory**: Lost on crash

**Solution:** Add try-except-finally block to save `step_records` periodically and on crashes.
