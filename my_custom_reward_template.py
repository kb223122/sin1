"""
Template for creating custom reward functions in Sinergym.

INSTRUCTIONS:
1. Copy this file to your preferred location
2. Rename the class and customize the reward logic
3. Use it in YAML config or Python code

Example usage in YAML:
    reward: /workspace/my_custom_reward_template.py:MyCustomReward
    reward_kwargs:
      temperature_variables: [air_temperature]
      energy_variables: [HVAC_electricity_demand_rate]
      # ... other parameters

Example usage in Python:
    from my_custom_reward_template import MyCustomReward
    env = gym.make('Eplus-5zone-hot-continuous-v1',
                   reward=MyCustomReward,
                   reward_kwargs={...})
"""

from datetime import datetime
from typing import Any, Dict, List, Tuple
from sinergym.utils.rewards import BaseReward
from sinergym.utils.constants import YEAR


class MyCustomReward(BaseReward):
    """
    Custom reward function template.
    
    Modify this class to implement your own reward logic.
    
    This example implements a reward similar to LinearReward but with
    a customizable penalty factor.
    """

    def __init__(
        self,
        temperature_variables: List[str],
        energy_variables: List[str],
        range_comfort_winter: Tuple[float, float],
        range_comfort_summer: Tuple[float, float],
        summer_start: Tuple[int, int] = (6, 1),
        summer_final: Tuple[int, int] = (9, 30),
        energy_weight: float = 0.5,
        lambda_energy: float = 1.0,
        lambda_temperature: float = 1.0,
        # ADD YOUR CUSTOM PARAMETERS HERE
        custom_penalty_factor: float = 1.0,
    ):
        """
        Initialize custom reward function.
        
        Args:
            temperature_variables (List[str]): Names of temperature observation variables
            energy_variables (List[str]): Names of energy observation variables
            range_comfort_winter (Tuple[float,float]): Winter comfort range (min, max) in °C
            range_comfort_summer (Tuple[float,float]): Summer comfort range (min, max) in °C
            summer_start (Tuple[int,int]): Summer start date (month, day)
            summer_final (Tuple[int,int]): Summer end date (month, day)
            energy_weight (float): Weight for energy term (0-1)
            lambda_energy (float): Scaling factor for energy
            lambda_temperature (float): Scaling factor for temperature
            custom_penalty_factor (float): Your custom parameter
        """
        
        super().__init__()
        
        # Store standard parameters
        self.temp_names = temperature_variables
        self.energy_names = energy_variables
        self.range_comfort_winter = range_comfort_winter
        self.range_comfort_summer = range_comfort_summer
        self.summer_start = summer_start
        self.summer_final = summer_final
        self.W_energy = energy_weight
        self.lambda_energy = lambda_energy
        self.lambda_temp = lambda_temperature
        
        # Store your custom parameters
        self.custom_penalty_factor = custom_penalty_factor
        
        self.logger.info('MyCustomReward initialized.')
        self.logger.info(f'  Temperature variables: {self.temp_names}')
        self.logger.info(f'  Energy variables: {self.energy_names}')
        self.logger.info(f'  Energy weight: {self.W_energy}')
        self.logger.info(f'  Custom penalty factor: {self.custom_penalty_factor}')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate reward value based on current observation.
        
        This method is called at every timestep with the current observations.
        
        Args:
            obs_dict (Dict[str, Any]): Dictionary with observation variable names as keys
                                       and their current values
                Example: {
                    'month': 6,
                    'day_of_month': 15,
                    'hour': 14,
                    'outdoor_temperature': 28.5,
                    'air_temperature': 23.2,
                    'HVAC_electricity_demand_rate': 5000.0,
                    ...
                }
        
        Returns:
            Tuple[float, Dict[str, Any]]: 
                - reward (float): The calculated reward value
                - reward_terms (dict): Dictionary with reward components for logging/debugging
        """
        
        # ============================================================================
        # STEP 1: Calculate Energy Consumption
        # ============================================================================
        energy_values = [obs_dict[v] for v in self.energy_names]
        total_energy = sum(energy_values)
        energy_penalty = -total_energy  # Negative because we want to minimize
        
        # ============================================================================
        # STEP 2: Determine Current Season and Comfort Range
        # ============================================================================
        current_dt = datetime(
            YEAR, int(obs_dict['month']), int(obs_dict['day_of_month'])
        )
        summer_start_date = datetime(YEAR, *self.summer_start)
        summer_final_date = datetime(YEAR, *self.summer_final)
        
        # Select comfort range based on season
        if summer_start_date <= current_dt <= summer_final_date:
            temp_range = self.range_comfort_summer
            season = 'summer'
        else:
            temp_range = self.range_comfort_winter
            season = 'winter'
        
        # ============================================================================
        # STEP 3: Calculate Temperature Violations
        # ============================================================================
        temp_values = [obs_dict[v] for v in self.temp_names]
        
        # Calculate violation for each temperature zone
        # Violation is positive when outside comfort range, 0 when inside
        temp_violations = []
        for T in temp_values:
            if T < temp_range[0]:
                violation = temp_range[0] - T  # Too cold
            elif T > temp_range[1]:
                violation = T - temp_range[1]  # Too hot
            else:
                violation = 0.0  # Within comfort range
            temp_violations.append(violation)
        
        total_temp_violation = sum(temp_violations)
        comfort_penalty = -total_temp_violation  # Negative because it's a penalty
        
        # ============================================================================
        # STEP 4: CUSTOMIZE YOUR REWARD LOGIC HERE
        # ============================================================================
        
        # Standard linear terms
        energy_term = self.lambda_energy * self.W_energy * energy_penalty
        comfort_term = self.lambda_temp * (1 - self.W_energy) * comfort_penalty
        
        # YOUR CUSTOM LOGIC:
        # Example: Add a custom penalty that increases with violation severity
        if total_temp_violation > 0:
            custom_penalty = -self.custom_penalty_factor * (total_temp_violation ** 1.5)
        else:
            custom_penalty = 0.0
        
        # Calculate final reward
        reward = energy_term + comfort_term + custom_penalty
        
        # ============================================================================
        # STEP 5: Return Reward and Components
        # ============================================================================
        
        # Return reward terms for logging/debugging
        reward_terms = {
            # Main components
            'reward': reward,
            'energy_term': energy_term,
            'comfort_term': comfort_term,
            'custom_penalty': custom_penalty,
            
            # Raw penalties
            'energy_penalty': energy_penalty,
            'comfort_penalty': comfort_penalty,
            
            # Raw values
            'total_power_demand': total_energy,
            'total_temperature_violation': total_temp_violation,
            'mean_temperature': sum(temp_values) / len(temp_values) if temp_values else 0,
            
            # Configuration
            'reward_weight': self.W_energy,
            'season': season,
            'comfort_range_min': temp_range[0],
            'comfort_range_max': temp_range[1],
            
            # Custom
            'custom_penalty_factor': self.custom_penalty_factor,
        }
        
        return reward, reward_terms


# ============================================================================
# EXAMPLE: Another Custom Reward with Different Logic
# ============================================================================

class ExponentialPenaltyReward(BaseReward):
    """
    Reward with exponential penalty for large violations.
    
    This penalizes large temperature violations more severely than small ones.
    """

    def __init__(
        self,
        temperature_variables: List[str],
        energy_variables: List[str],
        range_comfort_winter: Tuple[float, float],
        range_comfort_summer: Tuple[float, float],
        summer_start: Tuple[int, int] = (6, 1),
        summer_final: Tuple[int, int] = (9, 30),
        energy_weight: float = 0.5,
        lambda_energy: float = 1.0,
        lambda_temperature: float = 1.0,
        penalty_exponent: float = 2.0,  # Custom parameter
    ):
        super().__init__()
        
        self.temp_names = temperature_variables
        self.energy_names = energy_variables
        self.range_comfort_winter = range_comfort_winter
        self.range_comfort_summer = range_comfort_summer
        self.summer_start = summer_start
        self.summer_final = summer_final
        self.W_energy = energy_weight
        self.lambda_energy = lambda_energy
        self.lambda_temp = lambda_temperature
        self.penalty_exponent = penalty_exponent
        
        self.logger.info(f'ExponentialPenaltyReward initialized (exponent={penalty_exponent}).')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate reward with exponential temperature penalty."""
        
        # Energy
        energy_values = [obs_dict[v] for v in self.energy_names]
        total_energy = sum(energy_values)
        energy_penalty = -total_energy
        
        # Temperature violations
        current_dt = datetime(
            YEAR, int(obs_dict['month']), int(obs_dict['day_of_month'])
        )
        summer_start_date = datetime(YEAR, *self.summer_start)
        summer_final_date = datetime(YEAR, *self.summer_final)
        
        temp_range = (
            self.range_comfort_summer
            if summer_start_date <= current_dt <= summer_final_date
            else self.range_comfort_winter
        )
        
        temp_values = [obs_dict[v] for v in self.temp_names]
        temp_violations = [
            max(temp_range[0] - T, 0, T - temp_range[1]) 
            for T in temp_values
        ]
        
        # Exponential penalty
        total_exponential_violation = sum(v ** self.penalty_exponent for v in temp_violations)
        comfort_penalty = -total_exponential_violation
        
        # Reward
        energy_term = self.lambda_energy * self.W_energy * energy_penalty
        comfort_term = self.lambda_temp * (1 - self.W_energy) * comfort_penalty
        reward = energy_term + comfort_term
        
        reward_terms = {
            'reward': reward,
            'energy_term': energy_term,
            'comfort_term': comfort_term,
            'energy_penalty': energy_penalty,
            'comfort_penalty': comfort_penalty,
            'total_power_demand': total_energy,
            'total_exponential_violation': total_exponential_violation,
            'penalty_exponent': self.penalty_exponent,
        }
        
        return reward, reward_terms


# ============================================================================
# TESTING YOUR REWARD
# ============================================================================

if __name__ == "__main__":
    """
    Test your reward function with sample observations.
    
    Run this file directly to test:
        python3 my_custom_reward_template.py
    """
    
    print("="*80)
    print("TESTING CUSTOM REWARD FUNCTIONS")
    print("="*80)
    
    # Create reward instance
    reward_fn = MyCustomReward(
        temperature_variables=['air_temperature'],
        energy_variables=['HVAC_electricity_demand_rate'],
        range_comfort_winter=(20.0, 23.5),
        range_comfort_summer=(23.0, 26.0),
        energy_weight=0.5,
        lambda_energy=1.0e-4,
        lambda_temperature=1.0,
        custom_penalty_factor=2.0,
    )
    
    # Test cases
    test_cases = [
        {
            'name': 'Comfortable + Low Energy',
            'obs': {
                'month': 6,
                'day_of_month': 15,
                'air_temperature': 24.0,  # Within summer range [23, 26]
                'HVAC_electricity_demand_rate': 1000.0,
            }
        },
        {
            'name': 'Too Hot + High Energy',
            'obs': {
                'month': 6,
                'day_of_month': 15,
                'air_temperature': 28.0,  # Above summer range
                'HVAC_electricity_demand_rate': 5000.0,
            }
        },
        {
            'name': 'Too Cold + Medium Energy',
            'obs': {
                'month': 1,
                'day_of_month': 15,
                'air_temperature': 18.0,  # Below winter range [20, 23.5]
                'HVAC_electricity_demand_rate': 3000.0,
            }
        },
    ]
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print("-" * 80)
        reward, terms = reward_fn(test['obs'])
        print(f"  Observation: {test['obs']}")
        print(f"  Reward: {reward:.4f}")
        print(f"  Energy Term: {terms['energy_term']:.4f}")
        print(f"  Comfort Term: {terms['comfort_term']:.4f}")
        print(f"  Custom Penalty: {terms['custom_penalty']:.4f}")
        print(f"  Temperature Violation: {terms['total_temperature_violation']:.2f}°C")
    
    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80)
