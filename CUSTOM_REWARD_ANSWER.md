# ✅ ANSWER: Where to Put Your Custom Reward Function

## 🎯 Direct Answer

After checking **all** the documentation and code, here's where to put your custom reward function:

---

## 📍 **TWO OPTIONS** (Both work perfectly!)

### **Option 1: Add to `sinergym/utils/rewards.py` (RECOMMENDED)**

**File Location:** `/workspace/sinergym/utils/rewards.py`

**What to do:**
1. Open the file
2. Scroll to the end
3. Add your custom reward class

**Example:**
```python
class MyCustomReward(BaseReward):
    def __init__(self, temperature_variables, energy_variables, ...):
        super().__init__()
        # Your initialization
    
    def __call__(self, obs_dict):
        # Your reward calculation
        return reward, reward_terms
```

**Use in YAML:**
```yaml
reward: sinergym.utils.rewards:MyCustomReward
```

**✅ Advantages:**
- Easy to use (same as LinearReward)
- Follows Sinergym structure
- No need for file paths

---

### **Option 2: Create Separate File**

**File Location:** Anywhere! e.g., `/workspace/my_rewards.py`

**What to do:**
1. Create a new Python file
2. Import BaseReward: `from sinergym.utils.rewards import BaseReward`
3. Define your class (same structure as Option 1)

**Use in YAML:**
```yaml
reward: /workspace/my_rewards.py:MyCustomReward
```

**✅ Advantages:**
- Keeps Sinergym code clean
- Easy to share/modify
- Good for experiments

---

## 📝 How Sinergym Loads Rewards

### **The Loading Process:**

1. **In YAML config:**
   ```yaml
   reward: sinergym.utils.rewards:LinearReward
   ```

2. **Sinergym reads this line and:**
   - Uses `import_from_path()` function (in `sinergym/utils/common.py`)
   - Dynamically imports your reward class
   - Creates instance with `reward_kwargs`

3. **During environment steps:**
   - Calls your reward: `reward, terms = reward_fn(obs_dict)`

### **Both formats work:**
- `sinergym.utils.rewards:MyReward` (module path)
- `/path/to/file.py:MyReward` (file path)

---

## 🔍 Where I Found This Information

### **Files Checked:**

1. ✅ `/workspace/sinergym/utils/rewards.py`
   - Contains all reward classes (LinearReward, ExpReward, etc.)
   - All inherit from BaseReward
   - Line 11: BaseReward definition

2. ✅ `/workspace/sinergym/envs/eplus_env.py`
   - Line 16: `from sinergym.utils.rewards import *`
   - Line 240: `self.reward_fn = reward(**reward_kwargs)`
   - Line 426: `reward, rw_terms = self.reward_fn(obs)`

3. ✅ `/workspace/sinergym/utils/common.py`
   - Line 34: `def import_from_path(dotted_or_file_path: str)`
   - Supports both module and file paths

4. ✅ `/workspace/sinergym/__init__.py`
   - Line 97: Example of reward import
   - Shows how rewards are loaded in environment registration

5. ✅ YAML configuration files in `/workspace/sinergym/data/default_configuration/`
   - All use: `reward: sinergym.utils.rewards:LinearReward`
   - Shows standard format

---

## 📚 Complete Guide Files Created

I've created comprehensive documentation for you:

| File | Purpose |
|------|---------|
| **[HOW_TO_ADD_CUSTOM_REWARD.md](HOW_TO_ADD_CUSTOM_REWARD.md)** | 📖 Complete guide with detailed examples |
| **[my_custom_reward_template.py](my_custom_reward_template.py)** | 🎯 Ready-to-use template (copy & modify) |
| **[CUSTOM_REWARD_QUICK_GUIDE.md](CUSTOM_REWARD_QUICK_GUIDE.md)** | ⚡ Quick reference card |

---

## 🚀 Quick Start

### **Step 1: Copy the Template**
```bash
cp /workspace/my_custom_reward_template.py /workspace/my_reward.py
```

### **Step 2: Modify Your Reward Logic**
Edit the `__call__` method in `my_reward.py`:
```python
def __call__(self, obs_dict):
    # YOUR CUSTOM REWARD LOGIC HERE
    energy = sum(obs_dict[v] for v in self.energy_names)
    temps = [obs_dict[v] for v in self.temp_names]
    
    # Calculate your reward
    reward = ...  # Your formula
    
    return reward, {'energy': energy, 'temps': temps}
```

### **Step 3: Use in YAML**
```yaml
reward: /workspace/my_reward.py:MyCustomReward
reward_kwargs:
  temperature_variables: [air_temperature]
  energy_variables: [HVAC_electricity_demand_rate]
  range_comfort_winter: [20.0, 23.5]
  range_comfort_summer: [23.0, 26.0]
```

### **Step 4: Test It**
```bash
python3 /workspace/my_reward.py  # Test standalone
```

Or use it:
```python
import gymnasium as gym
env = gym.make('Eplus-5zone-hot-continuous-v1')  # Uses your reward!
```

---

## ✅ Requirements for Your Custom Reward

Your class MUST:

1. **Inherit from BaseReward**
   ```python
   from sinergym.utils.rewards import BaseReward
   
   class MyReward(BaseReward):
   ```

2. **Call super().__init__() in __init__**
   ```python
   def __init__(self, ...):
       super().__init__()
   ```

3. **Implement __call__ method**
   ```python
   def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
       # Calculate reward
       return reward_value, reward_terms_dict
   ```

4. **Return (float, dict)**
   - First: reward value (float)
   - Second: reward terms (dict) for logging

---

## 🎓 How It Works

### **Current Reward Classes in Sinergym:**

All in `/workspace/sinergym/utils/rewards.py`:
- `BaseReward` (base class)
- `LinearReward` (standard linear penalty)
- `EnergyCostLinearReward` (with energy cost)
- `ExpReward` (exponential penalty)
- `HourlyLinearReward` (time-dependent)
- `NormalizedLinearReward` (normalized)
- `MultiZoneReward` (multi-zone)

**Your custom reward works the exact same way!**

---

## 💡 Best Practice

**For production/permanent rewards:**
- ✅ Use Option 1 (add to `rewards.py`)
- Easier maintenance
- Follows project structure

**For experiments/testing:**
- ✅ Use Option 2 (separate file)
- Keeps Sinergym clean
- Easy to share

---

## 🎯 Example: Adding to rewards.py

Open `/workspace/sinergym/utils/rewards.py` and add at the end:

```python
# ... existing code ...
# (after MultiZoneReward class)

class MyCustomReward(BaseReward):
    """
    My custom reward with quadratic penalty.
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
        
        self.logger.info('MyCustomReward initialized.')
    
    def __call__(self, obs_dict: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        # Energy penalty
        energy = sum(obs_dict[v] for v in self.energy_names)
        energy_penalty = -energy
        
        # Temperature penalty (quadratic)
        current_dt = datetime(YEAR, int(obs_dict['month']), int(obs_dict['day_of_month']))
        summer_start_date = datetime(YEAR, *self.summer_start)
        summer_final_date = datetime(YEAR, *self.summer_final)
        
        temp_range = (
            self.range_comfort_summer
            if summer_start_date <= current_dt <= summer_final_date
            else self.range_comfort_winter
        )
        
        temps = [obs_dict[v] for v in self.temp_names]
        violations = [max(temp_range[0] - T, 0, T - temp_range[1]) for T in temps]
        
        # QUADRATIC PENALTY
        total_violation = sum(v ** 2 for v in violations)
        comfort_penalty = -total_violation
        
        # Calculate reward
        energy_term = self.lambda_energy * self.W_energy * energy_penalty
        comfort_term = self.lambda_temp * (1 - self.W_energy) * comfort_penalty
        reward = energy_term + comfort_term
        
        return reward, {
            'energy_term': energy_term,
            'comfort_term': comfort_term,
            'total_power': energy,
            'total_violation': total_violation,
        }
```

Then use it:
```yaml
reward: sinergym.utils.rewards:MyCustomReward
```

**Done! 🎉**

---

## 📊 Summary Table

| Aspect | Option 1 (rewards.py) | Option 2 (Separate File) |
|--------|----------------------|-------------------------|
| **Location** | `/workspace/sinergym/utils/rewards.py` | Any path (e.g., `/workspace/my_rewards.py`) |
| **YAML Reference** | `sinergym.utils.rewards:MyReward` | `/path/to/file.py:MyReward` |
| **Import in Python** | `from sinergym.utils.rewards import MyReward` | `from my_rewards import MyReward` |
| **Best For** | Production, permanent rewards | Experiments, testing |
| **Maintenance** | Part of Sinergym | Independent |

---

## ✅ Final Answer

**Where to put your custom reward:**

1. ✅ **`/workspace/sinergym/utils/rewards.py`** (add at the end)
   - OR -
2. ✅ **Any separate Python file** (e.g., `/workspace/my_rewards.py`)

**Both work exactly like `LinearReward` and other built-in rewards!**

**Three requirements:**
1. Inherit from `BaseReward`
2. Implement `__init__` (call `super().__init__()`)
3. Implement `__call__` (return `(reward, terms_dict)`)

**Reference the complete guide:** [HOW_TO_ADD_CUSTOM_REWARD.md](HOW_TO_ADD_CUSTOM_REWARD.md)

**Use the template:** [my_custom_reward_template.py](my_custom_reward_template.py)

---

**That's it! Your custom reward will work just like LinearReward! 🚀**
