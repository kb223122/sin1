#!/usr/bin/env python3
"""
5-Zone Zonal Rule-Based Controller for Sinergym
Implements individual zone control based on occupancy, season, and comfort requirements
"""

import os
import numpy as np
import pandas as pd
import gymnasium as gym
import matplotlib.pyplot as plt
import sinergym
from datetime import datetime

# -------------------------------
# Try to import logger wrappers
# -------------------------------
LoggerWrapper = None
CSVWrapper = None
try:
    from sinergym.utils.wrappers import LoggerWrapper as _LoggerWrapper
    LoggerWrapper = _LoggerWrapper
except Exception:
    pass

# CSV wrapper names vary across versions — try several
if CSVWrapper is None:
    try:
        from sinergym.utils.wrappers import CSVLogger as _CSVWrapper
        CSVWrapper = _CSVWrapper
    except Exception:
        pass
if CSVWrapper is None:
    try:
        from sinergym.utils.wrappers import CSVLoggerWrapper as _CSVWrapper
        CSVWrapper = _CSVWrapper
    except Exception:
        pass
if CSVWrapper is None:
    try:
        from sinergym.utils.wrappers import LoggerCSV as _CSVWrapper
        CSVWrapper = _CSVWrapper
    except Exception:
        pass

# ==========================================
# Experiment / output paths
# ==========================================
EXP_NAME = "5zone_zonal_rbc"
OUT_DIR = os.path.join(".", EXP_NAME)
os.makedirs(OUT_DIR, exist_ok=True)

# Building configuration
building_config = {
    "timesteps_per_hour": 4, 
    "runperiod": (1, 1, 1991, 31, 12, 1991)
}

# Seed
SEED = 0
np.random.seed(SEED)

# ==========================================
# Initialize environment with your custom config
# ==========================================
env = gym.make(
    'Eplus-5zone-zonal-hot-continuous-v1',  # Your custom environment ID
    building_config=building_config,
)

# Attach wrappers if available
if LoggerWrapper is not None:
    try:
        env = LoggerWrapper(env, log_dir=OUT_DIR)
        print("[INFO] LoggerWrapper attached.")
    except TypeError:
        env = LoggerWrapper(env)
        print("[INFO] LoggerWrapper attached (default args).")
    except Exception as e:
        print(f"[WARN] Could not attach LoggerWrapper: {e}")

if CSVWrapper is not None:
    try:
        env = CSVWrapper(env, log_dir=OUT_DIR)
        print("[INFO] CSV logger wrapper attached.")
    except TypeError:
        env = CSVWrapper(env)
        print("[INFO] CSV logger wrapper attached (default args).")
    except Exception as e:
        print(f"[WARN] Could not attach CSV logger wrapper: {e}")
else:
    print("[WARN] No CSV wrapper found; we will still export our own CSV and plots.")

# ==========================================
# Observation mapping for 5-zone environment
# ==========================================
def get_observation_mapping():
    """Get observation variable names from environment"""
    obs_vars = env.get_wrapper_attr('observation_variables')
    return {i: name for i, name in enumerate(obs_vars)}

# ==========================================
# Comfort ranges and control parameters
# ==========================================
WINTER_COMFORT_RANGE = (20.0, 23.5)
SUMMER_COMFORT_RANGE = (23.0, 26.0)
UNOCCUPIED_RANGE = (12.0, 30.0)  # Wide range when unoccupied

SUMMER_MONTHS = [6, 7, 8, 9]
WINTER_MONTHS = [1, 2, 3, 4, 5, 10, 11, 12]

# Zone-specific parameters
ZONES = ['space1', 'space2', 'space3', 'space4', 'space5']
ZONE_NAMES = ['SPACE1-1', 'SPACE2-1', 'SPACE3-1', 'SPACE4-1', 'SPACE5-1']

# ==========================================
# Rule-Based Controller Class
# ==========================================
class ZonalRBCController:
    def __init__(self, env):
        self.env = env
        self.obs_vars = env.get_wrapper_attr('observation_variables')
        self.action_vars = env.get_wrapper_attr('action_variables')
        
        # Create mapping for easy access
        self.var_map = {name: i for i, name in enumerate(self.obs_vars)}
        
        # Zone-specific comfort ranges (can be customized per zone)
        self.zone_comfort_ranges = {
            'space1': {'winter': (20.0, 23.5), 'summer': (23.0, 26.0)},
            'space2': {'winter': (20.0, 23.5), 'summer': (23.0, 26.0)},
            'space3': {'winter': (20.0, 23.5), 'summer': (23.0, 26.0)},
            'space4': {'winter': (20.0, 23.5), 'summer': (23.0, 26.0)},
            'space5': {'winter': (20.0, 23.5), 'summer': (23.0, 26.0)}
        }
        
        # Zone-specific occupancy thresholds
        self.zone_occupancy_thresholds = {
            'space1': 0.1,
            'space2': 0.1,
            'space3': 0.1,
            'space4': 0.1,
            'space5': 0.1
        }
    
    def get_zone_data(self, observation):
        """Extract zone-specific data from observation"""
        zone_data = {}
        
        for i, zone in enumerate(ZONES):
            zone_data[zone] = {
                'temperature': observation[self.var_map[f'air_temperature_{zone}']],
                'humidity': observation[self.var_map[f'air_humidity_{zone}']],
                'occupancy': observation[self.var_map[f'air_occ_{zone}']],
                'heating_setpoint': observation[self.var_map[f'htg_setpoint_{zone}']],
                'cooling_setpoint': observation[self.var_map[f'clg_setpoint_{zone}']],
                'sensible_heating_rate': observation[self.var_map[f'sensible_htg_rate_{zone}']],
                'sensible_cooling_rate': observation[self.var_map[f'sensible_clg_rate_{zone}']],
                'damper_position': observation[self.var_map[f'damper_position_{zone}']],
                'lights_power': observation[self.var_map[f'lights_power_{zone}']],
                'equipment_power': observation[self.var_map[f'equipment_power_{zone}']]
            }
        
        return zone_data
    
    def get_environmental_data(self, observation):
        """Extract environmental data from observation"""
        return {
            'month': int(observation[self.var_map['month']]),
            'day': int(observation[self.var_map['day_of_month']]),
            'hour': int(observation[self.var_map['hour']]),
            'outdoor_temp': observation[self.var_map['outdoor_temperature']],
            'outdoor_humidity': observation[self.var_map['outdoor_humidity']],
            'wind_speed': observation[self.var_map['wind_speed']],
            'solar_diffuse': observation[self.var_map['diffuse_solar_radiation']],
            'solar_direct': observation[self.var_map['direct_solar_radiation']]
        }
    
    def determine_season(self, month):
        """Determine season based on month"""
        if month in SUMMER_MONTHS:
            return 'summer'
        else:
            return 'winter'
    
    def is_zone_occupied(self, zone, occupancy):
        """Check if zone is occupied based on threshold"""
        return occupancy > self.zone_occupancy_thresholds[zone]
    
    def calculate_zone_setpoints(self, zone, zone_data, env_data):
        """Calculate heating and cooling setpoints for a specific zone"""
        temp = zone_data['temperature']
        occupancy = zone_data['occupancy']
        season = self.determine_season(env_data['month'])
        
        # Get comfort range for this zone and season
        comfort_range = self.zone_comfort_ranges[zone][season]
        
        if self.is_zone_occupied(zone, occupancy):
            # Zone is occupied - use comfort range
            heating_setpoint = comfort_range[0]
            cooling_setpoint = comfort_range[1]
        else:
            # Zone is unoccupied - use wide range to save energy
            heating_setpoint = UNOCCUPIED_RANGE[0]
            cooling_setpoint = UNOCCUPIED_RANGE[1]
        
        # Additional logic for fine-tuning based on current conditions
        if season == 'summer':
            # In summer, if zone is getting too hot, lower cooling setpoint slightly
            if temp > comfort_range[1] + 1.0:
                cooling_setpoint = max(comfort_range[0], temp - 2.0)
        else:
            # In winter, if zone is getting too cold, raise heating setpoint slightly
            if temp < comfort_range[0] - 1.0:
                heating_setpoint = min(comfort_range[1], temp + 2.0)
        
        return heating_setpoint, cooling_setpoint
    
    def act(self, observation):
        """Generate action for all zones"""
        zone_data = self.get_zone_data(observation)
        env_data = self.get_environmental_data(observation)
        
        action = np.zeros(10, dtype=np.float32)  # 10 actions: 5 zones × 2 setpoints each
        
        for i, zone in enumerate(ZONES):
            heating_sp, cooling_sp = self.calculate_zone_setpoints(
                zone, zone_data[zone], env_data
            )
            
            # Store in action array (heating first, then cooling for each zone)
            action[i*2] = heating_sp      # Heating setpoint
            action[i*2 + 1] = cooling_sp  # Cooling setpoint
        
        # Clip actions to valid range
        action = np.clip(action, env.action_space.low, env.action_space.high)
        
        return action

# ==========================================
# Initialize controller
# ==========================================
controller = ZonalRBCController(env)

# ==========================================
# Storage for logging
# ==========================================
obs_mapping = get_observation_mapping()
results = {name: [] for name in obs_mapping.values()}
results.update({
    f"Action_Heating_{zone}": [] for zone in ZONES
})
results.update({
    f"Action_Cooling_{zone}": [] for zone in ZONES
})
results.update({
    "Reward": [],
    "Total_Energy": [],
    "Comfort_Violations": []
})

# ==========================================
# Run simulation
# ==========================================
state, info = env.reset()
terminated = truncated = False
step = 0

print("="*100)
print("5-ZONE ZONAL RULE-BASED CONTROLLER SIMULATION")
print("="*100)
print(f"Environment: {env.get_wrapper_attr('name')}")
print(f"Observation space: {env.observation_space.shape}")
print(f"Action space: {env.action_space.shape}")
print(f"Total variables: {len(obs_mapping)}")
print("="*100)

while not (terminated or truncated):
    # Get action from controller
    action = controller.act(state)
    
    # Step environment
    next_state, reward, terminated, truncated, info = env.step(action)
    
    # Extract zone data for logging
    zone_data = controller.get_zone_data(state)
    env_data = controller.get_environmental_data(state)
    
    # Log all observations
    for idx, name in obs_mapping.items():
        results[name].append(float(state[idx]) if idx not in (0, 1, 2) else int(state[idx]))
    
    # Log actions for each zone
    for i, zone in enumerate(ZONES):
        results[f"Action_Heating_{zone}"].append(float(action[i*2]))
        results[f"Action_Cooling_{zone}"].append(float(action[i*2 + 1]))
    
    # Log reward and energy
    results["Reward"].append(float(reward))
    results["Total_Energy"].append(float(state[obs_mapping['HVAC_electricity_demand_rate']]))
    
    # Calculate comfort violations
    comfort_violations = 0
    for zone in ZONES:
        temp = zone_data[zone]['temperature']
        occupancy = zone_data[zone]['occupancy']
        season = controller.determine_season(env_data['month'])
        
        if controller.is_zone_occupied(zone, occupancy):
            comfort_range = controller.zone_comfort_ranges[zone][season]
            if temp < comfort_range[0] or temp > comfort_range[1]:
                comfort_violations += 1
    
    results["Comfort_Violations"].append(comfort_violations)
    
    # Console output
    if step % 100 == 0 or step < 10:  # Print every 100 steps or first 10 steps
        print(f"\nStep {step+1} | {env_data['month']:02d}/{env_data['day']:02d} {env_data['hour']:02d}:00 | "
              f"Outdoor: {env_data['outdoor_temp']:.1f}°C")
        
        for i, zone in enumerate(ZONES):
            zone_info = zone_data[zone]
            occupied = "OCC" if controller.is_zone_occupied(zone, zone_info['occupancy']) else "UNOCC"
            season = controller.determine_season(env_data['month'])
            comfort_range = controller.zone_comfort_ranges[zone][season]
            
            print(f"  {zone.upper()}: {zone_info['temperature']:.1f}°C "
                  f"(H:{action[i*2]:.1f}, C:{action[i*2+1]:.1f}) "
                  f"[{comfort_range[0]:.1f}-{comfort_range[1]:.1f}] {occupied} "
                  f"Occ:{zone_info['occupancy']:.1f}")
        
        print(f"  HVAC Demand: {state[obs_mapping['HVAC_electricity_demand_rate']]:.1f}W | "
              f"Reward: {reward:.4f} | Violations: {comfort_violations}/5")
    
    # Advance state
    state = next_state
    step += 1

env.close()

# ==========================================
# Save results to CSV
# ==========================================
df = pd.DataFrame(results)
csv_path = os.path.join(OUT_DIR, f"{EXP_NAME}_results.csv")
df.to_csv(csv_path, index=False)
print(f"\n[INFO] Saved detailed results CSV: {csv_path}")

# ==========================================
# Create summary statistics
# ==========================================
print("\n" + "="*100)
print("SIMULATION SUMMARY")
print("="*100)

# Overall statistics
total_steps = len(df)
total_energy = df['HVAC_electricity_demand_rate'].sum()
avg_reward = df['Reward'].mean()
total_violations = df['Comfort_Violations'].sum()

print(f"Total simulation steps: {total_steps}")
print(f"Total energy consumption: {total_energy:.2f} Wh")
print(f"Average reward: {avg_reward:.4f}")
print(f"Total comfort violations: {total_violations}")

# Zone-specific statistics
print("\nZone-specific performance:")
for zone in ZONES:
    temp_col = f'air_temperature_{zone}'
    htg_col = f'Action_Heating_{zone}'
    clg_col = f'Action_Cooling_{zone}'
    
    avg_temp = df[temp_col].mean()
    temp_std = df[temp_col].std()
    avg_htg_sp = df[htg_col].mean()
    avg_clg_sp = df[clg_col].mean()
    
    print(f"  {zone.upper()}: Avg Temp {avg_temp:.2f}±{temp_std:.2f}°C, "
          f"Avg Setpoints H:{avg_htg_sp:.1f}°C C:{avg_clg_sp:.1f}°C")

# Monthly analysis
monthly_stats = df.groupby('month').agg({
    'HVAC_electricity_demand_rate': ['mean', 'sum'],
    'Reward': 'mean',
    'Comfort_Violations': 'sum'
}).round(2)

print(f"\nMonthly energy consumption (kWh):")
for month in range(1, 13):
    if month in monthly_stats.index:
        monthly_energy = monthly_stats.loc[month, ('HVAC_electricity_demand_rate', 'sum')] / 1000
        monthly_violations = monthly_stats.loc[month, ('Comfort_Violations', 'sum')]
        print(f"  Month {month:2d}: {monthly_energy:8.2f} kWh, {monthly_violations:3d} violations")

# ==========================================
# Create visualizations
# ==========================================
print(f"\n[INFO] Creating visualizations...")

# 1. Zone temperatures over time
plt.figure(figsize=(15, 10))

# Plot outdoor temperature
plt.subplot(3, 2, 1)
plt.plot(df['outdoor_temperature'], label='Outdoor', color='blue', alpha=0.7)
plt.title('Outdoor Temperature')
plt.ylabel('Temperature (°C)')
plt.grid(True, alpha=0.3)

# Plot zone temperatures
plt.subplot(3, 2, 2)
colors = ['red', 'green', 'blue', 'orange', 'purple']
for i, zone in enumerate(ZONES):
    plt.plot(df[f'air_temperature_{zone}'], 
             label=f'{zone.upper()}', color=colors[i], alpha=0.7)
plt.title('Zone Air Temperatures')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot setpoints for each zone
for i, zone in enumerate(ZONES):
    plt.subplot(3, 2, i+3)
    plt.plot(df[f'Action_Heating_{zone}'], label=f'Heating SP', color='red', alpha=0.7)
    plt.plot(df[f'Action_Cooling_{zone}'], label=f'Cooling SP', color='blue', alpha=0.7)
    plt.plot(df[f'air_temperature_{zone}'], label=f'Actual Temp', color='black', alpha=0.5)
    plt.title(f'{zone.upper()} Setpoints vs Temperature')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'zone_temperatures.png'), dpi=150, bbox_inches='tight')
plt.close()

# 2. Energy consumption analysis
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(df['HVAC_electricity_demand_rate'])
plt.title('HVAC Electricity Demand Rate')
plt.ylabel('Power (W)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
monthly_energy = df.groupby('month')['HVAC_electricity_demand_rate'].sum() / 1000
plt.bar(monthly_energy.index, monthly_energy.values)
plt.title('Monthly Energy Consumption')
plt.xlabel('Month')
plt.ylabel('Energy (kWh)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
plt.plot(df['Reward'])
plt.title('Reward Over Time')
plt.ylabel('Reward')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
plt.plot(df['Comfort_Violations'])
plt.title('Comfort Violations Over Time')
plt.ylabel('Number of Violations')
plt.xlabel('Time Steps')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'energy_analysis.png'), dpi=150, bbox_inches='tight')
plt.close()

# 3. Zone occupancy analysis
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
for i, zone in enumerate(ZONES):
    plt.plot(df[f'air_occ_{zone}'], label=f'{zone.upper()}', color=colors[i], alpha=0.7)
plt.title('Zone Occupancy Over Time')
plt.ylabel('Occupant Count')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
occupancy_summary = []
for zone in ZONES:
    occupied_steps = (df[f'air_occ_{zone}'] > 0.1).sum()
    total_steps = len(df)
    occupancy_percentage = (occupied_steps / total_steps) * 100
    occupancy_summary.append(occupancy_percentage)

plt.bar(ZONES, occupancy_summary)
plt.title('Zone Occupancy Percentage')
plt.ylabel('Occupancy (%)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'occupancy_analysis.png'), dpi=150, bbox_inches='tight')
plt.close()

print(f"[DONE] All results and visualizations saved in: {OUT_DIR}")
print("="*100)