# ⚡ Custom Reward Quick Guide

## 🎯 Where to Put Your Custom Reward Function

### **Option 1: Add to Sinergym (Recommended)**
**File:** `/workspace/sinergym/utils/rewards.py`

Add your class at the end of the file:
```python
class MyCustomReward(BaseReward):
    def __init__(self, ...):
        super().__init__()
        # Your initialization
    
    def __call__(self, obs_dict):
        # Your reward logic
        return reward, reward_terms
```

### **Option 2: Separate File**
**File:** `/workspace/my_custom_rewards.py` (or any path)

```python
from sinergym.utils.rewards import BaseReward

class MyCustomReward(BaseReward):
    # Same as above
```

---

## 📝 How to Use in YAML

### Option 1 (in rewards.py):
```yaml
reward: sinergym.utils.rewards:MyCustomReward
reward_kwargs:
  temperature_variables: [air_temperature]
  energy_variables: [HVAC_electricity_demand_rate]
  # your parameters
```

### Option 2 (separate file):
```yaml
reward: /workspace/my_custom_rewards.py:MyCustomReward
reward_kwargs:
  # same as above
```

---

## 🚀 How to Use in Python

```python
import gymnasium as gym
from my_custom_rewards import MyCustomReward

env = gym.make(
    'Eplus-5zone-hot-continuous-v1',
    reward=MyCustomReward,
    reward_kwargs={
        'temperature_variables': ['air_temperature'],
        'energy_variables': ['HVAC_electricity_demand_rate'],
        'range_comfort_winter': (20.0, 23.5),
        'range_comfort_summer': (23.0, 26.0),
        # your custom parameters
    }
)
```

---

## ✅ Requirements

1. **Inherit from BaseReward:**
   ```python
   class MyReward(BaseReward):
   ```

2. **Implement `__init__`:**
   ```python
   def __init__(self, ...):
       super().__init__()
       # Store parameters
   ```

3. **Implement `__call__`:**
   ```python
   def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
       # Calculate reward
       return reward_value, reward_terms_dict
   ```

---

## 📋 Template Structure

```python
from datetime import datetime
from typing import Any, Dict, List, Tuple
from sinergym.utils.rewards import BaseReward
from sinergym.utils.constants import YEAR

class MyReward(BaseReward):
    
    def __init__(
        self,
        temperature_variables: List[str],
        energy_variables: List[str],
        range_comfort_winter: Tuple[float, float],
        range_comfort_summer: Tuple[float, float],
        # Add your custom parameters
    ):
        super().__init__()
        self.temp_names = temperature_variables
        self.energy_names = energy_variables
        # Store your parameters
        self.logger.info('MyReward initialized.')
    
    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        # 1. Get energy
        energy = sum(obs_dict[v] for v in self.energy_names)
        
        # 2. Get temperatures
        temps = [obs_dict[v] for v in self.temp_names]
        
        # 3. Calculate violations
        # ... your logic ...
        
        # 4. Calculate reward
        reward = 0.0  # Your formula
        
        # 5. Return reward and terms
        return reward, {
            'energy': energy,
            'temps': temps,
            # any terms you want to track
        }
```

---

## 🎓 Available Observation Variables

Your `obs_dict` contains all observation variables:

```python
obs_dict = {
    'month': 6,
    'day_of_month': 15,
    'hour': 14,
    'outdoor_temperature': 28.5,
    'air_temperature': 23.2,
    'HVAC_electricity_demand_rate': 5000.0,
    # ... all other observation variables
}
```

**Access any variable by name:**
```python
temp = obs_dict['air_temperature']
power = obs_dict['HVAC_electricity_demand_rate']
month = obs_dict['month']
```

---

## 📚 Files Created for You

| File | Purpose |
|------|---------|
| **[HOW_TO_ADD_CUSTOM_REWARD.md](HOW_TO_ADD_CUSTOM_REWARD.md)** | Complete guide with examples |
| **[my_custom_reward_template.py](my_custom_reward_template.py)** | Ready-to-use template |
| **[CUSTOM_REWARD_QUICK_GUIDE.md](CUSTOM_REWARD_QUICK_GUIDE.md)** | This quick reference |

---

## 🔧 Testing Your Reward

Run the template file directly:
```bash
python3 my_custom_reward_template.py
```

Or test in your code:
```python
reward_fn = MyCustomReward(...)

# Test with sample observation
obs_dict = {
    'month': 6,
    'day_of_month': 15,
    'air_temperature': 24.0,
    'HVAC_electricity_demand_rate': 1000.0,
}

reward, terms = reward_fn(obs_dict)
print(f"Reward: {reward}")
print(f"Terms: {terms}")
```

---

## 💡 Quick Tips

1. ✅ Always call `super().__init__()` in your `__init__`
2. ✅ Return both reward value AND reward terms dict
3. ✅ Use negative values for penalties
4. ✅ Log important info with `self.logger.info()`
5. ✅ Test your reward before using it in training
6. ✅ Return meaningful reward terms for debugging

---

## 🎯 Summary

**Two options:**
1. Add to `/workspace/sinergym/utils/rewards.py`
2. Create separate file (e.g., `my_custom_rewards.py`)

**Both work the same way!**

**Use in YAML:**
```yaml
reward: sinergym.utils.rewards:MyReward  # Option 1
# OR
reward: /path/to/file.py:MyReward        # Option 2
```

**Use in Python:**
```python
env = gym.make('Eplus-5zone-hot-continuous-v1',
               reward=MyReward,
               reward_kwargs={...})
```

**Done! 🎉**
