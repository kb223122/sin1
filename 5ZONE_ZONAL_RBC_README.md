# 5-Zone Zonal Rule-Based Controller

This repository contains a comprehensive rule-based controller for the 5-zone zonal environment in Sinergym, implementing individual zone control based on occupancy, season, and comfort requirements.

## Files Overview

### 1. `5zone_zonal_rbc.py` - Complete Implementation
- **Purpose**: Full-featured rule-based controller with comprehensive logging and visualization
- **Features**:
  - Individual zone control based on occupancy and season
  - Detailed logging of all observations and actions
  - Monthly energy consumption analysis
  - Comfort violation tracking
  - Multiple visualization plots
  - Zone-specific performance metrics

### 2. `5zone_simple_rbc.py` - Simplified Version
- **Purpose**: Streamlined version focusing on core control logic
- **Features**:
  - Basic zone-wise control logic
  - Simple console output
  - Essential performance metrics
  - Easy to understand and modify

### 3. `register_5zone_zonal.py` - Environment Registration
- **Purpose**: Register your custom 5-zone zonal environment with Sinergym
- **Usage**: Run this script before using the environment

### 4. `test_5zone_environment.py` - Testing Script
- **Purpose**: Verify that your environment works correctly
- **Features**:
  - Environment creation test
  - Observation structure validation
  - Zone control testing
  - Action space verification

## Control Logic

### Zone-Wise Control Strategy

The controller implements the following logic for each zone:

1. **Occupancy Detection**: Check if zone is occupied (occupancy > 0.1)
2. **Season Determination**: Summer (months 6-9) vs Winter (other months)
3. **Setpoint Selection**:
   - **Occupied + Summer**: Heating 23°C, Cooling 26°C
   - **Occupied + Winter**: Heating 20°C, Cooling 23.5°C
   - **Unoccupied**: Heating 12°C, Cooling 30°C (energy saving)

4. **Fine-Tuning**: Adjust setpoints based on current temperature
   - If zone is too hot in summer: lower cooling setpoint
   - If zone is too cold in winter: raise heating setpoint

### Action Space

The environment uses a 10-dimensional action space:
- `action[0]`: Space1 heating setpoint
- `action[1]`: Space1 cooling setpoint
- `action[2]`: Space2 heating setpoint
- `action[3]`: Space2 cooling setpoint
- ... and so on for all 5 zones

## Usage Instructions

### 1. Environment Setup

First, make sure your custom environment is properly configured:

```bash
# Place your YAML config file in the correct location
# The config should define:
# - id_base: 5zone-zonal
# - building_file: 5ZoneAutoDXVAV000.epJSON
# - Individual zone observations and actions
```

### 2. Register Environment

```bash
python register_5zone_zonal.py
```

### 3. Test Environment

```bash
python test_5zone_environment.py
```

### 4. Run Controller

**Complete version:**
```bash
python 5zone_zonal_rbc.py
```

**Simplified version:**
```bash
python 5zone_simple_rbc.py
```

## Output Files

### Complete Version (`5zone_zonal_rbc.py`)
- `5zone_zonal_rbc_results.csv`: Detailed simulation results
- `zone_temperatures.png`: Zone temperature plots
- `energy_analysis.png`: Energy consumption analysis
- `occupancy_analysis.png`: Occupancy patterns

### Simplified Version (`5zone_simple_rbc.py`)
- `5zone_simple_rbc_results.csv`: Basic simulation results
- Console output with zone status

## Key Features

### 1. Zone-Specific Control
- Each zone is controlled independently
- Occupancy-based setpoint selection
- Seasonal comfort range adaptation

### 2. Energy Efficiency
- Wide setpoint range when unoccupied
- Fine-tuning based on current conditions
- Comfort violation tracking

### 3. Comprehensive Logging
- All observations and actions recorded
- Zone-specific performance metrics
- Monthly energy consumption analysis

### 4. Visualization
- Temperature trends over time
- Energy consumption patterns
- Occupancy analysis
- Comfort violation tracking

## Customization

### Modify Comfort Ranges
Edit the comfort ranges in the controller:

```python
WINTER_COMFORT_RANGE = (20.0, 23.5)  # Heating: 20°C, Cooling: 23.5°C
SUMMER_COMFORT_RANGE = (23.0, 26.0)  # Heating: 23°C, Cooling: 26°C
UNOCCUPIED_RANGE = (12.0, 30.0)      # Wide range when unoccupied
```

### Adjust Occupancy Thresholds
Modify the occupancy detection threshold:

```python
def is_zone_occupied(self, zone, occupancy):
    return occupancy > 0.1  # Adjust this threshold
```

### Add Zone-Specific Logic
Implement different control strategies per zone:

```python
def calculate_zone_setpoints(self, zone, zone_data, env_data):
    # Add zone-specific logic here
    if zone == 'space1':
        # Special logic for space1
        pass
    elif zone == 'space2':
        # Special logic for space2
        pass
    # ... etc
```

## Troubleshooting

### Common Issues

1. **Environment not found**: Make sure to run `register_5zone_zonal.py` first
2. **Observation index errors**: Check that your YAML config matches the expected variable names
3. **Action space errors**: Verify that your action space has 10 dimensions (5 zones × 2 setpoints)

### Debug Mode

Enable detailed logging by modifying the print frequency:

```python
# Print every step instead of every 100 steps
if step % 1 == 0:  # Changed from 100 to 1
    print_zone_status(...)
```

## Performance Metrics

The controller tracks several key performance indicators:

- **Energy Consumption**: Total HVAC electricity usage
- **Comfort Violations**: Number of zones outside comfort range
- **Zone Performance**: Individual zone temperature control
- **Occupancy Patterns**: Zone utilization over time

## Next Steps

1. **Tune Parameters**: Adjust comfort ranges and thresholds based on your requirements
2. **Add Advanced Logic**: Implement more sophisticated control strategies
3. **Compare with RL**: Use this as a baseline for reinforcement learning algorithms
4. **Extend to More Zones**: Adapt the logic for buildings with more zones

## Dependencies

- Python 3.7+
- Sinergym
- Gymnasium
- NumPy
- Pandas
- Matplotlib

## License

This code is provided as-is for educational and research purposes. Please ensure you have the proper licenses for Sinergym and EnergyPlus.