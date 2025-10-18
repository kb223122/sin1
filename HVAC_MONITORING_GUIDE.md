# HVAC Component Monitoring Guide for Sinergym 5Zone Environment

## Overview

This guide explains the modifications made to enable comprehensive HVAC component monitoring in the Sinergym 5Zone environment. The modifications allow you to track and print the status and power consumption of all HVAC components at each simulation step.

## Modified Files

### 1. `sinergym/data/buildings/5ZoneAutoDXVAV.epJSON`

**Added Output:Variable section** with the following HVAC component variables:

#### Supply Fan Monitoring
- `Fan Electricity Rate` - Real-time power consumption (W)
- `Fan Air Mass Flow Rate` - Air flow rate (kg/s)
- `Fan Rise in Air Temperature` - Temperature increase (°C)
- `Fan Heat Gain to Air` - Heat added to air (W)

#### Main Cooling Coil Monitoring
- `Cooling Coil Total Cooling Rate` - Total cooling capacity (W)
- `Cooling Coil Sensible Cooling Rate` - Sensible cooling (W)
- `Cooling Coil Latent Cooling Rate` - Latent cooling (W)
- `Cooling Coil Electricity Rate` - Power consumption (W)
- `Cooling Coil Runtime Fraction` - Operating fraction (0-1)
- `Cooling Coil Basin Heater Electricity Rate` - Basin heater power (W)

#### Main Heating Coil Monitoring
- `Heating Coil Heating Rate` - Heating capacity (W)
- `Heating Coil Electricity Rate` - Power consumption (W)

#### VAV Terminal Monitoring (All 5 Zones)
- `Zone Air Terminal VAV Damper Position` - Damper position (0-1)
- `Zone Air Terminal Sensible Heating Rate` - Zone heating (W)
- `Zone Air Terminal Sensible Cooling Rate` - Zone cooling (W)

#### Air System Status
- `Air System Outdoor Air Economizer Status` - Economizer status
- `Air System Outdoor Air Flow Fraction` - Outdoor air fraction (0-1)
- `Air System Outdoor Air Mass Flow Rate` - Outdoor air flow (kg/s)
- `Air System Mixed Air Mass Flow Rate` - Mixed air flow (kg/s)

#### System Node Temperatures
- `System Node Temperature` - Supply air temperature (°C)
- `System Node Mass Flow Rate` - Supply air flow (kg/s)
- `System Node Temperature Mixed` - Mixed air temperature (°C)
- `System Node Temperature Cooling` - Cooling coil outlet (°C)
- `System Node Temperature Heating` - Heating coil outlet (°C)

**Added Output:Meter section** with energy consumption meters for all components.

### 2. `sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml`

**Updated variables section** to include all new HVAC monitoring variables with descriptive names:

```yaml
variables:
  # Supply Fan
  Fan Electricity Rate:
    variable_names: fan_electricity_rate
    keys: Supply Fan 1
  
  # Main Cooling Coil
  Cooling Coil Total Cooling Rate:
    variable_names: cooling_coil_total_rate
    keys: Main Cooling Coil 1
  
  # ... (and many more)
```

**Updated meters section** to include energy consumption tracking:

```yaml
meters:
  Fan Electricity Energy: fan_electricity_energy
  Cooling Coil Total Cooling Energy: cooling_coil_total_energy
  # ... (and many more)
```

## Usage Examples

### Basic Monitoring

```python
import gymnasium as gym
import sinergym

# Create environment
env = gym.make('Eplus-5zone-v1')
obs, info = env.reset()

# Access HVAC data
fan_power = obs['fan_electricity_rate']
cooling_power = obs['cooling_coil_electricity_rate']
heating_power = obs['heating_coil_electricity_rate']

print(f"Fan Power: {fan_power} W")
print(f"Cooling Power: {cooling_power} W")
print(f"Heating Power: {heating_power} W")
```

### Comprehensive Monitoring

Use the provided `hvac_monitoring_example.py` script for detailed monitoring:

```bash
python hvac_monitoring_example.py
```

This script provides:
- Real-time HVAC component status
- Power consumption tracking
- Performance analysis
- Data export capabilities

### Testing Implementation

Use the test script to verify everything works:

```bash
python test_hvac_monitoring.py
```

## Available HVAC Variables

### Power Consumption Variables
- `fan_electricity_rate` - Supply fan power (W)
- `cooling_coil_electricity_rate` - Cooling coil power (W)
- `heating_coil_electricity_rate` - Heating coil power (W)
- `cooling_coil_basin_heater_rate` - Basin heater power (W)
- `HVAC_electricity_demand_rate` - Total HVAC power (W)

### Performance Variables
- `cooling_coil_total_rate` - Total cooling capacity (W)
- `cooling_coil_sensible_rate` - Sensible cooling (W)
- `cooling_coil_latent_rate` - Latent cooling (W)
- `heating_coil_heating_rate` - Heating capacity (W)
- `cooling_coil_runtime_fraction` - Cooling coil runtime (0-1)

### Air Flow Variables
- `fan_air_mass_flow_rate` - Fan air flow (kg/s)
- `outdoor_air_mass_flow_rate` - Outdoor air flow (kg/s)
- `mixed_air_mass_flow_rate` - Mixed air flow (kg/s)
- `supply_air_mass_flow_rate` - Supply air flow (kg/s)

### Temperature Variables
- `supply_air_temp` - Supply air temperature (°C)
- `mixed_air_temp` - Mixed air temperature (°C)
- `cooling_coil_outlet_temp` - Cooling coil outlet (°C)
- `heating_coil_outlet_temp` - Heating coil outlet (°C)

### VAV Terminal Variables (for each zone 1-5)
- `vav_damper_position_X` - Damper position (0-1)
- `vav_heating_rate_X` - Zone heating rate (W)
- `vav_cooling_rate_X` - Zone cooling rate (W)

### System Status Variables
- `outdoor_air_economizer_status` - Economizer status
- `outdoor_air_flow_fraction` - Outdoor air fraction (0-1)

## Energy Consumption Tracking

The implementation includes comprehensive energy tracking through meters:

### Real-time Energy Rates (W)
- Fan electricity rate
- Cooling coil electricity rate
- Heating coil electricity rate
- Basin heater electricity rate

### Cumulative Energy (J)
- Fan electricity energy
- Cooling coil total cooling energy
- Cooling coil sensible cooling energy
- Cooling coil latent cooling energy
- Cooling coil electricity energy
- Heating coil heating energy
- Heating coil electricity energy
- VAV terminal heating/cooling energy for each zone

## Data Analysis

The monitoring system enables various types of analysis:

### Performance Analysis
- Component efficiency tracking
- Runtime fraction analysis
- Load distribution analysis
- Temperature control effectiveness

### Energy Analysis
- Power consumption patterns
- Energy distribution among components
- Peak demand identification
- Energy efficiency trends

### System Health Monitoring
- Component status tracking
- Air flow monitoring
- Temperature control performance
- Economizer operation

## Troubleshooting

### Common Issues

1. **Missing Variables**: Ensure the epJSON file has the correct Output:Variable entries
2. **YAML Configuration**: Verify variable names match between epJSON and YAML files
3. **EnergyPlus Version**: Ensure compatibility with EnergyPlus 24.2.0
4. **File Paths**: Check that modified files are in the correct Sinergym directories

### Verification Steps

1. Run the test script: `python test_hvac_monitoring.py`
2. Check observation space contains expected variables
3. Verify step execution works without errors
4. Confirm data values are reasonable

## Customization

### Adding New Variables

To add monitoring for additional components:

1. Add `Output:Variable` entries to the epJSON file
2. Add corresponding entries to the YAML variables section
3. Update your monitoring script to access the new variables

### Modifying Monitoring Frequency

Change the `reporting_frequency` in the epJSON file:
- `"TimeStep"` - Every simulation timestep
- `"Hourly"` - Every hour
- `"Daily"` - Every day

### Custom Analysis

Extend the monitoring script to include:
- Custom performance metrics
- Advanced data visualization
- Automated reporting
- Integration with external systems

## Performance Considerations

- Monitoring adds computational overhead
- Consider reducing monitoring frequency for large simulations
- Use selective monitoring for specific components when needed
- Monitor memory usage with extensive data collection

## Support

For issues or questions:
1. Check the test script output
2. Verify file modifications are correct
3. Consult EnergyPlus documentation for variable names
4. Review Sinergym documentation for environment configuration