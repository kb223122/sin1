#!/usr/bin/env python3
"""
Simplified 5-Zone Zonal Rule-Based Controller
Focuses on core control logic with clear zone-wise decision making
"""

import os
import numpy as np
import pandas as pd
import gymnasium as gym
import sinergym

# ==========================================
# Configuration
# ==========================================
EXP_NAME = "5zone_simple_rbc"
OUT_DIR = os.path.join(".", EXP_NAME)
os.makedirs(OUT_DIR, exist_ok=True)

building_config = {
    "timesteps_per_hour": 4, 
    "runperiod": (1, 1, 1991, 31, 12, 1991)
}

# ==========================================
# Initialize environment
# ==========================================
env = gym.make(
    'Eplus-5zone-zonal-hot-continuous-v1',  # Your custom environment
    building_config=building_config,
)

# ==========================================
# Control parameters
# ==========================================
WINTER_COMFORT = (20.0, 23.5)  # Heating: 20°C, Cooling: 23.5°C
SUMMER_COMFORT = (23.0, 26.0)  # Heating: 23°C, Cooling: 26°C
UNOCCUPIED = (12.0, 30.0)      # Wide range when unoccupied

SUMMER_MONTHS = [6, 7, 8, 9]
ZONES = ['space1', 'space2', 'space3', 'space4', 'space5']

# ==========================================
# Simple Rule-Based Controller
# ==========================================
def get_zone_control(observation, zone_idx):
    """
    Get control action for a specific zone based on simple rules
    
    Args:
        observation: Current observation array
        zone_idx: Zone index (0-4 for space1-space5)
    
    Returns:
        tuple: (heating_setpoint, cooling_setpoint)
    """
    # Get observation indices (adjust based on your actual observation structure)
    month_idx = 0  # month
    occupancy_idx = 13 + zone_idx  # air_occ_space1, air_occ_space2, etc.
    temp_idx = 9 + zone_idx  # air_temperature_space1, air_temperature_space2, etc.
    
    # Extract data
    month = int(observation[month_idx])
    occupancy = observation[occupancy_idx]
    current_temp = observation[temp_idx]
    
    # Determine if zone is occupied
    is_occupied = occupancy > 0.1
    
    # Determine season
    is_summer = month in SUMMER_MONTHS
    
    # Apply control logic
    if is_occupied:
        if is_summer:
            # Summer occupied: use summer comfort range
            heating_sp = SUMMER_COMFORT[0]  # 23°C
            cooling_sp = SUMMER_COMFORT[1]  # 26°C
        else:
            # Winter occupied: use winter comfort range
            heating_sp = WINTER_COMFORT[0]  # 20°C
            cooling_sp = WINTER_COMFORT[1]  # 23.5°C
    else:
        # Unoccupied: use wide range to save energy
        heating_sp = UNOCCUPIED[0]  # 12°C
        cooling_sp = UNOCCUPIED[1]  # 30°C
    
    # Fine-tuning based on current temperature
    if is_occupied:
        if is_summer and current_temp > cooling_sp + 1.0:
            # Zone is too hot, lower cooling setpoint
            cooling_sp = max(SUMMER_COMFORT[0], current_temp - 2.0)
        elif not is_summer and current_temp < heating_sp - 1.0:
            # Zone is too cold, raise heating setpoint
            heating_sp = min(WINTER_COMFORT[1], current_temp + 2.0)
    
    return heating_sp, cooling_sp

def print_zone_status(observation, action, step, zone_idx):
    """Print status for a specific zone"""
    month_idx = 0
    occupancy_idx = 13 + zone_idx
    temp_idx = 9 + zone_idx
    
    month = int(observation[month_idx])
    occupancy = observation[occupancy_idx]
    temp = observation[temp_idx]
    heating_sp = action[zone_idx * 2]
    cooling_sp = action[zone_idx * 2 + 1]
    
    occupied = "OCC" if occupancy > 0.1 else "UNOCC"
    season = "SUM" if month in SUMMER_MONTHS else "WIN"
    
    print(f"    {ZONES[zone_idx].upper()}: {temp:.1f}°C "
          f"(H:{heating_sp:.1f}, C:{cooling_sp:.1f}) {occupied} {season}")

# ==========================================
# Main simulation loop
# ==========================================
print("="*80)
print("5-ZONE ZONAL RULE-BASED CONTROLLER - SIMPLIFIED VERSION")
print("="*80)

# Storage for results
results = {
    'step': [],
    'month': [],
    'day': [],
    'hour': [],
    'outdoor_temp': [],
    'reward': [],
    'total_energy': []
}

# Add zone-specific data
for zone in ZONES:
    results.update({
        f'{zone}_temp': [],
        f'{zone}_occupancy': [],
        f'{zone}_heating_sp': [],
        f'{zone}_cooling_sp': []
    })

# Run simulation
state, info = env.reset()
terminated = truncated = False
step = 0

while not (terminated or truncated):
    # Generate action for all zones
    action = np.zeros(10, dtype=np.float32)  # 10 actions total
    
    for zone_idx in range(5):
        heating_sp, cooling_sp = get_zone_control(state, zone_idx)
        action[zone_idx * 2] = heating_sp      # Heating setpoint
        action[zone_idx * 2 + 1] = cooling_sp  # Cooling setpoint
    
    # Clip action to valid range
    action = np.clip(action, env.action_space.low, env.action_space.high)
    
    # Step environment
    next_state, reward, terminated, truncated, info = env.step(action)
    
    # Log data
    results['step'].append(step)
    results['month'].append(int(state[0]))
    results['day'].append(int(state[1]))
    results['hour'].append(int(state[2]))
    results['outdoor_temp'].append(state[3])
    results['reward'].append(reward)
    results['total_energy'].append(state[15])  # HVAC electricity demand rate
    
    # Log zone data
    for zone_idx in range(5):
        zone = ZONES[zone_idx]
        results[f'{zone}_temp'].append(state[9 + zone_idx])
        results[f'{zone}_occupancy'].append(state[13 + zone_idx])
        results[f'{zone}_heating_sp'].append(action[zone_idx * 2])
        results[f'{zone}_cooling_sp'].append(action[zone_idx * 2 + 1])
    
    # Print status every 100 steps or first 10 steps
    if step % 100 == 0 or step < 10:
        print(f"\nStep {step+1} | {int(state[1]):02d}/{int(state[0]):02d} {int(state[2]):02d}:00 | "
              f"Outdoor: {state[3]:.1f}°C | Energy: {state[15]:.1f}W | Reward: {reward:.3f}")
        
        for zone_idx in range(5):
            print_zone_status(state, action, step, zone_idx)
    
    # Advance state
    state = next_state
    step += 1

env.close()

# ==========================================
# Save results and create summary
# ==========================================
df = pd.DataFrame(results)
csv_path = os.path.join(OUT_DIR, f"{EXP_NAME}_results.csv")
df.to_csv(csv_path, index=False)

print(f"\n[INFO] Results saved to: {csv_path}")

# Create summary
print("\n" + "="*80)
print("SIMULATION SUMMARY")
print("="*80)

total_steps = len(df)
total_energy = df['total_energy'].sum() / 1000  # Convert to kWh
avg_reward = df['reward'].mean()

print(f"Total steps: {total_steps}")
print(f"Total energy: {total_energy:.2f} kWh")
print(f"Average reward: {avg_reward:.4f}")

print(f"\nZone performance:")
for zone in ZONES:
    avg_temp = df[f'{zone}_temp'].mean()
    avg_occupancy = df[f'{zone}_occupancy'].mean()
    occupied_steps = (df[f'{zone}_occupancy'] > 0.1).sum()
    occupancy_pct = (occupied_steps / total_steps) * 100
    
    print(f"  {zone.upper()}: Avg temp {avg_temp:.1f}°C, "
          f"Occupancy {occupancy_pct:.1f}% ({occupied_steps}/{total_steps} steps)")

# Monthly energy consumption
print(f"\nMonthly energy consumption (kWh):")
monthly_energy = df.groupby('month')['total_energy'].sum() / 1000
for month in range(1, 13):
    if month in monthly_energy.index:
        print(f"  Month {month:2d}: {monthly_energy[month]:8.2f} kWh")

print(f"\n[DONE] All results saved in: {OUT_DIR}")
print("="*80)