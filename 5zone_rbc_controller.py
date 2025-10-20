"""
Updated Rule-Based Controller for True 5-Zone Control
"""

import numpy as np
from datetime import datetime
from typing import List, Any
from gymnasium import Env
from sinergym.utils.constants import YEAR


class RBC5ZoneIndividual(object):
    """
    Rule-Based Controller for individual 5-zone control.
    Based on ASHRAE Standard 55-2004: Thermal Environmental Conditions for Human Occupancy.
    """

    def __init__(self, env: Env) -> None:
        """Agent based on static rules for controlling individual 5ZoneAutoDXVAV setpoints.

        Args:
            env (Env): Simulation environment
        """

        self.env = env

        self.observation_variables = env.get_wrapper_attr('observation_variables')
        self.action_variables = env.get_wrapper_attr('action_variables')

        # Individual setpoints for each zone
        self.setpoints_summer = np.array([23.0, 26.0], dtype=np.float32)  # [heating, cooling]
        self.setpoints_winter = np.array([20.0, 23.5], dtype=np.float32)  # [heating, cooling]

    def act(self, observation: List[Any]) -> np.ndarray:
        """Select action based on indoor temperature for all zones.

        Args:
            observation (List[Any]): Perceived observation.

        Returns:
            np.ndarray: Action chosen for all 5 zones (10-dimensional).
        """
        obs_dict = dict(zip(self.observation_variables, observation))
        year = int(obs_dict['year']) if obs_dict.get('year', False) else YEAR
        month = int(obs_dict['month'])
        day = int(obs_dict['day_of_month'])

        summer_start_date = datetime(year, 6, 1)
        summer_final_date = datetime(year, 9, 30)

        current_dt = datetime(year, month, day)

        # Get season comfort range
        if (
            current_dt >= summer_start_date and current_dt <= summer_final_date
        ):
            season_range = self.setpoints_summer
        else:
            season_range = self.setpoints_winter

        # Apply same setpoints to all 5 zones
        # Action format: [htg_zone1, clg_zone1, htg_zone2, clg_zone2, 
        #                 htg_zone3, clg_zone3, htg_zone4, clg_zone4, 
        #                 htg_zone5, clg_zone5]
        action = np.tile(season_range, 5)  # Repeat for all 5 zones
        
        return action


class RBC5ZoneAdaptive(object):
    """
    Adaptive Rule-Based Controller for individual 5-zone control.
    Adjusts setpoints based on individual zone temperatures.
    """

    def __init__(self, env: Env) -> None:
        """Agent with adaptive rules for controlling individual 5ZoneAutoDXVAV setpoints.

        Args:
            env (Env): Simulation environment
        """

        self.env = env
        self.observation_variables = env.get_wrapper_attr('observation_variables')
        self.action_variables = env.get_wrapper_attr('action_variables')

        # Base setpoints
        self.base_heating = 20.0
        self.base_cooling = 26.0
        self.temp_tolerance = 1.0  # Temperature tolerance for adjustments

    def act(self, observation: List[Any]) -> np.ndarray:
        """Select action based on individual zone temperatures.

        Args:
            observation (List[Any]): Perceived observation.

        Returns:
            np.ndarray: Action chosen for all 5 zones (10-dimensional).
        """
        obs_dict = dict(zip(self.observation_variables, observation))
        
        # Get zone temperatures
        zone_temps = [
            obs_dict.get('air_temperature_zone1', 22.0),
            obs_dict.get('air_temperature_zone2', 22.0),
            obs_dict.get('air_temperature_zone3', 22.0),
            obs_dict.get('air_temperature_zone4', 22.0),
            obs_dict.get('air_temperature_zone5', 22.0)
        ]
        
        action = []
        
        for temp in zone_temps:
            # Adaptive heating setpoint
            if temp < 20.0:
                heating_setpoint = self.base_heating + 1.0  # Increase heating
            elif temp > 24.0:
                heating_setpoint = self.base_heating - 1.0  # Decrease heating
            else:
                heating_setpoint = self.base_heating
            
            # Adaptive cooling setpoint
            if temp > 26.0:
                cooling_setpoint = self.base_cooling - 1.0  # Decrease cooling
            elif temp < 22.0:
                cooling_setpoint = self.base_cooling + 1.0  # Increase cooling
            else:
                cooling_setpoint = self.base_cooling
            
            # Clamp values to action space bounds
            heating_setpoint = np.clip(heating_setpoint, 12.0, 23.25)
            cooling_setpoint = np.clip(cooling_setpoint, 23.25, 30.0)
            
            action.extend([heating_setpoint, cooling_setpoint])
        
        return np.array(action, dtype=np.float32)