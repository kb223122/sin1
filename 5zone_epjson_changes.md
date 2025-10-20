# Required epJSON Changes for True 5-Zone Control

## 1. Add Individual Zone Setpoint Schedules

Add these new schedule objects to the epJSON:

```json
"Schedule:Compact": {
  "HTG-SETP-SCH-SPACE1": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 21.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "CLG-SETP-SCH-SPACE1": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 24.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "HTG-SETP-SCH-SPACE2": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 21.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "CLG-SETP-SCH-SPACE2": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 24.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "HTG-SETP-SCH-SPACE3": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 21.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "CLG-SETP-SCH-SPACE3": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 24.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "HTG-SETP-SCH-SPACE4": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 21.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "CLG-SETP-SCH-SPACE4": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 24.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "HTG-SETP-SCH-SPACE5": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 21.0}
    ],
    "schedule_type_limits_name": "Temperature"
  },
  "CLG-SETP-SCH-SPACE5": {
    "data": [
      {"field": "Through: 12/31"},
      {"field": "For: AllDays"},
      {"field": "Until: 24:00"},
      {"field": 24.0}
    ],
    "schedule_type_limits_name": "Temperature"
  }
}
```

## 2. Update Thermostat Setpoints

Modify the existing thermostat setpoint objects:

```json
"ThermostatSetpoint:SingleCooling": {
  "CoolingSetpoint": {
    "setpoint_temperature_schedule_name": "Clg-SetP-Sch"
  },
  "CoolingSetpoint-SPACE1": {
    "setpoint_temperature_schedule_name": "CLG-SETP-SCH-SPACE1"
  },
  "CoolingSetpoint-SPACE2": {
    "setpoint_temperature_schedule_name": "CLG-SETP-SCH-SPACE2"
  },
  "CoolingSetpoint-SPACE3": {
    "setpoint_temperature_schedule_name": "CLG-SETP-SCH-SPACE3"
  },
  "CoolingSetpoint-SPACE4": {
    "setpoint_temperature_schedule_name": "CLG-SETP-SCH-SPACE4"
  },
  "CoolingSetpoint-SPACE5": {
    "setpoint_temperature_schedule_name": "CLG-SETP-SCH-SPACE5"
  }
},
"ThermostatSetpoint:SingleHeating": {
  "HeatingSetpoint": {
    "setpoint_temperature_schedule_name": "Htg-SetP-Sch"
  },
  "HeatingSetpoint-SPACE1": {
    "setpoint_temperature_schedule_name": "HTG-SETP-SCH-SPACE1"
  },
  "HeatingSetpoint-SPACE2": {
    "setpoint_temperature_schedule_name": "HTG-SETP-SCH-SPACE2"
  },
  "HeatingSetpoint-SPACE3": {
    "setpoint_temperature_schedule_name": "HTG-SETP-SCH-SPACE3"
  },
  "HeatingSetpoint-SPACE4": {
    "setpoint_temperature_schedule_name": "HTG-SETP-SCH-SPACE4"
  },
  "HeatingSetpoint-SPACE5": {
    "setpoint_temperature_schedule_name": "HTG-SETP-SCH-SPACE5"
  }
}
```

## 3. Update Zone Control Thermostats

Modify each zone's thermostat control:

```json
"ZoneControl:Thermostat": {
  "SPACE1-1 Control": {
    "control_1_name": "CoolingSetpoint-SPACE1",
    "control_1_object_type": "ThermostatSetpoint:SingleCooling",
    "control_2_name": "HeatingSetpoint-SPACE1",
    "control_2_object_type": "ThermostatSetpoint:SingleHeating",
    "control_3_name": "DualSetPoint",
    "control_3_object_type": "ThermostatSetpoint:DualSetpoint",
    "control_type_schedule_name": "Zone Control Type Sched",
    "zone_or_zonelist_name": "SPACE1-1"
  },
  "SPACE2-1 Control": {
    "control_1_name": "CoolingSetpoint-SPACE2",
    "control_1_object_type": "ThermostatSetpoint:SingleCooling",
    "control_2_name": "HeatingSetpoint-SPACE2",
    "control_2_object_type": "ThermostatSetpoint:SingleHeating",
    "control_3_name": "DualSetPoint",
    "control_3_object_type": "ThermostatSetpoint:DualSetpoint",
    "control_type_schedule_name": "Zone Control Type Sched",
    "zone_or_zonelist_name": "SPACE2-1"
  },
  "SPACE3-1 Control": {
    "control_1_name": "CoolingSetpoint-SPACE3",
    "control_1_object_type": "ThermostatSetpoint:SingleCooling",
    "control_2_name": "HeatingSetpoint-SPACE3",
    "control_2_object_type": "ThermostatSetpoint:SingleHeating",
    "control_3_name": "DualSetPoint",
    "control_3_object_type": "ThermostatSetpoint:DualSetpoint",
    "control_type_schedule_name": "Zone Control Type Sched",
    "zone_or_zonelist_name": "SPACE3-1"
  },
  "SPACE4-1 Control": {
    "control_1_name": "CoolingSetpoint-SPACE4",
    "control_1_object_type": "ThermostatSetpoint:SingleCooling",
    "control_2_name": "HeatingSetpoint-SPACE4",
    "control_2_object_type": "ThermostatSetpoint:SingleHeating",
    "control_3_name": "DualSetPoint",
    "control_3_object_type": "ThermostatSetpoint:DualSetpoint",
    "control_type_schedule_name": "Zone Control Type Sched",
    "zone_or_zonelist_name": "SPACE4-1"
  },
  "SPACE5-1 Control": {
    "control_1_name": "CoolingSetpoint-SPACE5",
    "control_1_object_type": "ThermostatSetpoint:SingleCooling",
    "control_2_name": "HeatingSetpoint-SPACE5",
    "control_2_object_type": "ThermostatSetpoint:SingleHeating",
    "control_3_name": "DualSetPoint",
    "control_3_object_type": "ThermostatSetpoint:DualSetpoint",
    "control_type_schedule_name": "Zone Control Type Sched",
    "zone_or_zonelist_name": "SPACE5-1"
  }
}
```