# 🎁 How to Add Your Own Custom Reward Function in Sinergym

## 📋 Summary

After checking all the code and documentation, here's where to put your custom reward function:

### ✅ **Two Options:**

1. **Option 1 (Recommended for permanent rewards):** Add to `/workspace/sinergym/utils/rewards.py`
2. **Option 2 (Recommended for custom/experimental rewards):** Create a separate Python file

Both options work exactly the same way!

---

## 🎯 Option 1: Add to `sinergym/utils/rewards.py` (Recommended)

### **Where to add it:**
File: `/workspace/sinergym/utils/rewards.py`

### **Step-by-Step:**

#### 1. Open the rewards file
```bash
# File location:
/workspace/sinergym/utils/rewards.py
```

#### 2. Add your custom reward class at the end of the file

```python
class MyCustomReward(BaseReward):
    """
    My custom reward function.
    
    This is where you describe what your reward does.
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
        # Add your custom parameters here
        my_custom_param: float = 1.0,
    ):
        """
        Initialize your custom reward function.
        
        Args:
            temperature_variables (List[str]): Temperature variable names
            energy_variables (List[str]): Energy variable names
            range_comfort_winter (Tuple[float,float]): Winter comfort range
            range_comfort_summer (Tuple[float,float]): Summer comfort range
            summer_start (Tuple[int,int]): Summer start (month, day)
            summer_final (Tuple[int,int]): Summer end (month, day)
            energy_weight (float): Weight for energy term
            lambda_energy (float): Energy scaling factor
            lambda_temperature (float): Temperature scaling factor
            my_custom_param (float): Your custom parameter
        """
        
        super().__init__()
        
        # Store parameters
        self.temp_names = temperature_variables
        self.energy_names = energy_variables
        self.range_comfort_winter = range_comfort_winter
        self.range_comfort_summer = range_comfort_summer
        self.summer_start = summer_start
        self.summer_final = summer_final
        self.W_energy = energy_weight
        self.lambda_energy = lambda_energy
        self.lambda_temp = lambda_temperature
        
        # Your custom parameter
        self.my_custom_param = my_custom_param
        
        self.logger.info('MyCustomReward function initialized.')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate the reward function value.
        
        Args:
            obs_dict (Dict[str, Any]): Dictionary with observation variables
            
        Returns:
            Tuple[float, Dict[str, Any]]: Reward value and reward terms dict
        """
        
        # 1. Calculate energy consumption
        energy_values = [obs_dict[v] for v in self.energy_names]
        total_energy = sum(energy_values)
        energy_penalty = -total_energy
        
        # 2. Calculate temperature violation
        # Determine current season
        current_dt = datetime(
            YEAR, int(obs_dict['month']), int(obs_dict['day_of_month'])
        )
        summer_start_date = datetime(YEAR, *self.summer_start)
        summer_final_date = datetime(YEAR, *self.summer_final)
        
        # Get comfort range for current season
        temp_range = (
            self.range_comfort_summer
            if summer_start_date <= current_dt <= summer_final_date
            else self.range_comfort_winter
        )
        
        # Calculate violations
        temp_values = [obs_dict[v] for v in self.temp_names]
        temp_violations = [
            max(temp_range[0] - T, 0, T - temp_range[1]) 
            for T in temp_values
        ]
        total_temp_violation = sum(temp_violations)
        comfort_penalty = -total_temp_violation
        
        # 3. Calculate YOUR CUSTOM reward formula
        # This is where you implement your custom logic!
        energy_term = self.lambda_energy * self.W_energy * energy_penalty
        comfort_term = self.lambda_temp * (1 - self.W_energy) * comfort_penalty
        
        # Example: Add a custom penalty
        custom_penalty = -self.my_custom_param * (total_temp_violation ** 2)
        
        # Final reward
        reward = energy_term + comfort_term + custom_penalty
        
        # 4. Return reward and components (for logging/debugging)
        reward_terms = {
            'energy_term': energy_term,
            'comfort_term': comfort_term,
            'custom_penalty': custom_penalty,
            'energy_penalty': energy_penalty,
            'comfort_penalty': comfort_penalty,
            'total_power_demand': total_energy,
            'total_temperature_violation': total_temp_violation,
            'reward_weight': self.W_energy,
        }
        
        return reward, reward_terms
```

#### 3. That's it! Your reward is ready to use!

---

## 🎯 Option 2: Create a Separate File (For Custom/Experimental Rewards)

### **Where to create it:**
Anywhere you want! For example: `/workspace/my_custom_rewards.py`

### **Step-by-Step:**

#### 1. Create a new Python file
```bash
# Create your file:
touch /workspace/my_custom_rewards.py
```

#### 2. Add the necessary imports and your reward class

```python
"""My custom reward functions for Sinergym."""

from datetime import datetime
from typing import Any, Dict, List, Tuple

from sinergym.utils.rewards import BaseReward
from sinergym.utils.constants import YEAR

class MyCustomReward(BaseReward):
    """
    My custom reward function.
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
        my_custom_param: float = 1.0,
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
        self.my_custom_param = my_custom_param
        
        self.logger.info('MyCustomReward initialized.')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate reward."""
        
        # Your reward calculation logic here
        # (Same as Option 1)
        
        energy_values = [obs_dict[v] for v in self.energy_names]
        total_energy = sum(energy_values)
        
        # ... your reward calculation ...
        
        reward = 0.0  # Your reward formula
        reward_terms = {}  # Your reward components
        
        return reward, reward_terms
```

---

## 📝 How to Use Your Custom Reward in YAML Configuration

### **Option 1: If added to `rewards.py`**

Edit your YAML file (e.g., `/workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml`):

```yaml
# Change the reward line:
reward: sinergym.utils.rewards:MyCustomReward

# Add your reward parameters:
reward_kwargs:
  temperature_variables:
    - air_temperature
  energy_variables:
    - HVAC_electricity_demand_rate
  range_comfort_winter:
    - 20.0
    - 23.5
  range_comfort_summer:
    - 23.0
    - 26.0
  summer_start:
    - 6
    - 1
  summer_final:
    - 9
    - 30
  energy_weight: 0.5
  lambda_energy: 1.0e-4
  lambda_temperature: 1.0
  my_custom_param: 2.0  # Your custom parameter!
```

### **Option 2: If in a separate file**

```yaml
# Use the full file path:
reward: /workspace/my_custom_rewards.py:MyCustomReward

# Add your reward parameters:
reward_kwargs:
  temperature_variables:
    - air_temperature
  energy_variables:
    - HVAC_electricity_demand_rate
  # ... (same as above)
  my_custom_param: 2.0
```

---

## 🚀 How to Use Your Custom Reward in Python Code

### **Method 1: Through YAML (Recommended)**

```python
import gymnasium as gym
import sinergym

# If you modified the YAML file, just create the environment
env = gym.make('Eplus-5zone-hot-continuous-v1')
# It will automatically use your custom reward!

obs, info = env.reset()
# Your custom reward is now being used!
```

### **Method 2: Directly in Python (Without YAML)**

```python
import gymnasium as gym
from my_custom_rewards import MyCustomReward  # If Option 2
# OR
from sinergym.utils.rewards import MyCustomReward  # If Option 1

# Create environment with custom reward
env = gym.make(
    'Eplus-5zone-hot-continuous-v1',
    reward=MyCustomReward,
    reward_kwargs={
        'temperature_variables': ['air_temperature'],
        'energy_variables': ['HVAC_electricity_demand_rate'],
        'range_comfort_winter': (20.0, 23.5),
        'range_comfort_summer': (23.0, 26.0),
        'energy_weight': 0.5,
        'lambda_energy': 1.0e-4,
        'lambda_temperature': 1.0,
        'my_custom_param': 2.0,
    }
)

obs, info = env.reset()
```

---

## 📚 Complete Example: Custom Reward with Quadratic Penalty

Here's a complete example of a custom reward that penalizes temperature violations quadratically:

```python
class QuadraticPenaltyReward(BaseReward):
    """
    Reward with quadratic penalty for temperature violations.
    
    Formula: R = -W * λ_E * power - (1-W) * λ_T * (ΣT_violations²)
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
        
        self.logger.info('QuadraticPenaltyReward initialized.')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate reward with quadratic temperature penalty."""
        
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
        
        # Quadratic penalty
        total_quadratic_violation = sum(v ** 2 for v in temp_violations)
        comfort_penalty = -total_quadratic_violation
        
        # Reward calculation
        energy_term = self.lambda_energy * self.W_energy * energy_penalty
        comfort_term = self.lambda_temp * (1 - self.W_energy) * comfort_penalty
        reward = energy_term + comfort_term
        
        reward_terms = {
            'energy_term': energy_term,
            'comfort_term': comfort_term,
            'energy_penalty': energy_penalty,
            'comfort_penalty': comfort_penalty,
            'total_power_demand': total_energy,
            'total_quadratic_violation': total_quadratic_violation,
            'reward_weight': self.W_energy,
        }
        
        return reward, reward_terms
```

---

## ✅ Requirements for Your Custom Reward Class

Your custom reward class MUST:

1. **Inherit from `BaseReward`**
   ```python
   class MyReward(BaseReward):
   ```

2. **Implement `__init__` method**
   - Call `super().__init__()`
   - Store your parameters

3. **Implement `__call__` method**
   - Signature: `def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:`
   - Takes `obs_dict` with observation variable names as keys
   - Returns `(reward_value, reward_terms_dict)`

4. **Return format**
   ```python
   return reward_value, {
       'term1': value1,
       'term2': value2,
       # ... any terms you want to track
   }
   ```

---

## 🔍 How Sinergym Loads Your Reward

### **Behind the scenes:**

1. Sinergym reads your YAML config
2. Finds the `reward:` line (e.g., `sinergym.utils.rewards:MyCustomReward`)
3. Uses `import_from_path()` function to import your class
4. Creates an instance: `reward_fn = MyCustomReward(**reward_kwargs)`
5. Calls it each step: `reward, terms = reward_fn(obs_dict)`

### **The `import_from_path()` function supports:**

- **Module path:** `sinergym.utils.rewards:MyCustomReward`
- **File path:** `/path/to/my_rewards.py:MyCustomReward`

Both work exactly the same!

---

## 📁 File Structure Summary

```
/workspace/
├── sinergym/
│   ├── utils/
│   │   ├── rewards.py          ← Option 1: Add your class here
│   │   └── common.py           (contains import_from_path)
│   ├── data/
│   │   └── default_configuration/
│   │       └── *.yaml          ← Update YAML to use your reward
│   └── envs/
│       └── eplus_env.py        (uses reward in line 240)
└── my_custom_rewards.py        ← Option 2: Or create here
```

---

## 🎯 Recommendation

**For permanent/production rewards:**
- ✅ Use **Option 1** (add to `rewards.py`)
- Easier to maintain
- Follows Sinergym structure
- Can be imported easily

**For experimental/temporary rewards:**
- ✅ Use **Option 2** (separate file)
- Keeps Sinergym clean
- Easy to modify without touching Sinergym code
- Can be shared independently

---

## 🚀 Quick Start Template

Copy this template to get started:

```python
from datetime import datetime
from typing import Any, Dict, List, Tuple
from sinergym.utils.rewards import BaseReward
from sinergym.utils.constants import YEAR

class MyReward(BaseReward):
    """Your reward description."""

    def __init__(
        self,
        temperature_variables: List[str],
        energy_variables: List[str],
        range_comfort_winter: Tuple[float, float],
        range_comfort_summer: Tuple[float, float],
        # Add your parameters here
    ):
        super().__init__()
        # Store parameters
        self.temp_names = temperature_variables
        self.energy_names = energy_variables
        # ... store other params
        
        self.logger.info('MyReward initialized.')

    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate reward."""
        
        # 1. Get energy values
        energy = sum(obs_dict[v] for v in self.energy_names)
        
        # 2. Get temperature values
        temps = [obs_dict[v] for v in self.temp_names]
        
        # 3. YOUR REWARD LOGIC HERE
        reward = 0.0  # Calculate your reward
        
        # 4. Return reward and terms
        return reward, {
            'energy': energy,
            'temps': temps,
            # Add any terms you want to track
        }
```

---

## ✅ Summary

**Where to put your custom reward:**

1. ✅ **Option 1:** `/workspace/sinergym/utils/rewards.py` (add at the end)
2. ✅ **Option 2:** `/workspace/my_custom_rewards.py` (or any path you want)

**How to use it:**

1. ✅ In YAML: `reward: sinergym.utils.rewards:MyReward` (Option 1)
2. ✅ In YAML: `reward: /path/to/file.py:MyReward` (Option 2)
3. ✅ In Python: Import and pass to `gym.make()`

**Requirements:**
- ✅ Inherit from `BaseReward`
- ✅ Implement `__init__` and `__call__`
- ✅ Return `(float, dict)`

**That's it!** 🎉
