# Sinergym Observation vs Action Timing - Simple Explanation

## 🎯 **Short Answer**

**Observation at Step N shows the state AFTER the action from Step N was applied.**

**Example for 10-step simulation:**
- **Step 0 (reset)**: Get initial observation (no action yet)
- **Step 1**: Apply action → Get observation showing result of Step 1 action
- **Step 2**: Apply action → Get observation showing result of Step 2 action
- **Step N**: Apply action → Get observation showing result of Step N action

---

## 📊 **Detailed Flow**

### **Step 0 - Reset (Initial State)**

```python
obs, info = env.reset()
```

**What happens:**
1. EnergyPlus simulation starts
2. Warmup period runs (builds initial conditions)
3. **First timestep** is simulated WITHOUT any action
4. Observation = Current state at end of first timestep (before any action)

**Observation contains:**
- Initial indoor temperatures (from warmup)
- Initial outdoor weather
- Initial HVAC state
- **NO ACTION has been applied yet**

---

### **Step 1 - First Action**

```python
obs, reward, done, truncated, info = env.step(action_1)
```

**What happens (in order):**

1. **Action Queued**: `action_1` is put into `act_queue`
2. **EnergyPlus Callback** (`_process_action`):
   - Gets `action_1` from queue
   - **Applies it to EnergyPlus actuators** (sets setpoints)
3. **EnergyPlus Runs Timestep**:
   - Simulates building physics for 15 minutes
   - HVAC responds to the setpoints from `action_1`
   - Indoor temperature changes based on HVAC operation
4. **EnergyPlus Callback** (`_collect_obs_and_info`):
   - Collects observations from **end of this timestep**
   - These observations **reflect the changes from `action_1`**
5. **Python `step()` function**:
   - Gets observation from queue
   - Returns it to you

**Result**: `obs` at Step 1 shows the state **after** `action_1` was applied.

---

### **Step 2 - Second Action**

```python
obs, reward, done, truncated, info = env.step(action_2)
```

**What happens:**

1. **Action Queued**: `action_2` is put into `act_queue`
2. **EnergyPlus Callback** (`_process_action`):
   - Gets `action_2` from queue
   - **Applies it to EnergyPlus actuators** (updates setpoints)
3. **EnergyPlus Runs Timestep**:
   - Simulates building physics for next 15 minutes
   - HVAC responds to NEW setpoints from `action_2`
   - Indoor temperature changes based on NEW HVAC operation
4. **EnergyPlus Callback** (`_collect_obs_and_info`):
   - Collects observations from **end of this timestep**
   - These observations **reflect the changes from `action_2`**
5. **Python `step()` function**:
   - Gets observation from queue
   - Returns it to you

**Result**: `obs` at Step 2 shows the state **after** `action_2` was applied.

---

## 🔄 **Key Insight: One Timestep Delay**

**Important**: There is a **1-timestep delay** between action and visible effect!

```
Step 1: Apply action_1 → Simulation runs → Observation at Step 1 shows result
Step 2: Apply action_2 → Simulation runs → Observation at Step 2 shows result
```

**But this is NOT what you might think!**

- ✅ **Observation at Step N** = State after action from Step N
- ❌ **Observation at Step N** ≠ State before action from Step N

**Why?** Because the action is applied **at the START** of the timestep, and the observation is collected **at the END** of that same timestep.

---

## 📝 **Concrete Example**

### **Scenario: Heating a Cold Room**

**Initial State (Step 0 - Reset):**
```
Indoor Temp: 15°C
Outdoor Temp: 2°C
HVAC Setpoints: Default (maybe 12°C, 30°C)
Action Applied: None
```

**Step 1: Apply Heating Setpoint (20°C, 23.5°C)**
```python
action_1 = [20.0, 23.5]  # Heating setpoint for all zones
obs, reward, done, info = env.step(action_1)
```

**What happens inside:**
1. Action `[20.0, 23.5]` is queued
2. EnergyPlus applies setpoints: Heating = 20°C, Cooling = 23.5°C
3. EnergyPlus simulates 15 minutes:
   - HVAC starts heating (because 15°C < 20°C)
   - Indoor temp slowly increases: 15°C → 15.5°C
4. Observation collected shows:
   ```
   Indoor Temp: 15.5°C  ← CHANGED! (shows effect of action_1)
   HVAC Power: 800W     ← Heating running
   Setpoints: 20.0, 23.5 ← Reflected in observation
   ```

**Observation at Step 1 shows the RESULT of action_1!**

---

**Step 2: Keep Same Setpoints**
```python
action_2 = [20.0, 23.5]  # Same as before
obs, reward, done, info = env.step(action_2)
```

**What happens inside:**
1. Action `[20.0, 23.5]` is queued (same values)
2. EnergyPlus applies setpoints (same as before)
3. EnergyPlus simulates next 15 minutes:
   - HVAC continues heating (because 15.5°C < 20°C)
   - Indoor temp continues increasing: 15.5°C → 16.0°C
4. Observation collected shows:
   ```
   Indoor Temp: 16.0°C  ← CHANGED! (shows effect of action_2)
   HVAC Power: 850W     ← Still heating
   Setpoints: 20.0, 23.5
   ```

**Observation at Step 2 shows the RESULT of action_2!**

---

## 🎭 **What About "Random" Initial Observations?**

### **Step 0 (Reset) - NOT Random!**

When you call `env.reset()`, the observation is **NOT random**. It comes from:

1. **EnergyPlus Warmup**: 
   - EnergyPlus runs several days of simulation to build realistic initial conditions
   - Warmup stabilizes temperatures, HVAC states, building thermal mass
   - This ensures the building starts in a realistic state (not at arbitrary temperatures)

2. **First Timestep**:
   - After warmup, EnergyPlus runs the **first actual timestep**
   - During this timestep, **NO ACTION is applied** (action queue is empty)
   - The building state evolves based on:
     - Weather conditions
     - Default HVAC setpoints (from epJSON schedules)
     - Building physics (heat loss, solar gain, etc.)

3. **Observation**:
   - Collected at end of first timestep
   - Shows realistic initial state (e.g., indoor temp based on outdoor weather)
   - **NOT random** - based on physics simulation

**Example Reset Observation:**
```
Month: 1 (January)
Day: 1
Hour: 0 (midnight)
Outdoor Temp: 2.5°C
Indoor Temp: 16.2°C  ← Realistic value from warmup + first timestep
HVAC Setpoints: 12°C, 30°C  ← Default schedule values
HVAC Power: 150W  ← Fan running, minimal heating
```

This is **deterministic** (same weather file → same initial observation) unless you use stochastic weather.

---

## 🔍 **Code Evidence from Sinergym**

### **Reset Function** (`eplus_env.py` line 258-356):

```python
def reset(self, seed=None, options=None):
    # ... initialization ...
    
    # Start EnergyPlus simulation
    self.energyplus_simulator.start(...)
    
    # Wait for warmup
    if not self.energyplus_simulator.warmup_complete:
        self.energyplus_simulator.warmup_queue.get()
    
    # Wait for FIRST observation (after first timestep, NO ACTION)
    obs = self.obs_queue.get(timeout=10)
    
    return obs, info
```

**Key Point**: Reset returns observation from **first timestep** (no action applied yet).

---

### **Step Function** (`eplus_env.py` line 361-447):

```python
def step(self, action):
    # Put action in queue
    self.act_queue.put(action, timeout=2)
    
    # Wait for observation (from NEXT timestep, which used THIS action)
    obs = self.obs_queue.get(timeout=2)
    
    # Calculate reward based on observation
    reward = self.reward_fn(obs)
    
    return obs, reward, done, truncated, info
```

**Key Point**: 
- Action is queued
- Observation is collected **after** timestep that used that action
- Observation **reflects** the action's effect

---

### **EnergyPlus Callbacks** (`eplus.py`):

**Callback 1 - Process Action** (line 436-465):
```python
def _process_action(self, state_argument):
    # Get action from queue
    next_action = self.act_queue.get()
    
    # Apply action to actuators
    for i, (_, act_handle) in enumerate(self.actuator_handlers.items()):
        self.exchange.set_actuator_value(
            state=state_argument,
            actuator_handle=act_handle,
            actuator_value=next_action[i],  # ← ACTION APPLIED
        )
```

**When called**: At end of timestep N, **applies action for timestep N+1**.

**Callback 2 - Collect Observation** (line 382-434):
```python
def _collect_obs_and_info(self, state_argument):
    # Collect all observations from current timestep
    self.next_obs = {
        # Time variables
        'month': self.exchange.month(state_argument),
        'hour': self.exchange.hour(state_argument),
        # ... other variables ...
    }
    
    # Put observation in queue
    self.obs_queue.put(self.next_obs)
```

**When called**: At end of timestep N, **collects state from timestep N**.

---

## 📋 **Summary Table**

| Step | Action Applied | Observation Shows | Notes |
|------|---------------|-------------------|-------|
| **0 (reset)** | None (default schedules) | State after warmup + first timestep | Initial conditions |
| **1** | `action_1` | State after `action_1` was applied | Temperature changed by action_1 |
| **2** | `action_2` | State after `action_2` was applied | Temperature changed by action_2 |
| **N** | `action_N` | State after `action_N` was applied | Temperature changed by action_N |

---

## ✅ **Clear Answer to Your Questions**

### **Q1: Does observation at Step 2 show the effect of action from Step 2?**

**YES!** ✅

Observation at Step 2 shows the state **after** action from Step 2 was applied and simulated.

---

### **Q2: Or does observation at Step 2 already show the changed temp from action applied in Step 2?**

**YES!** ✅ (Same answer)

The observation at Step 2 **already includes** the temperature changes from action applied in Step 2.

---

### **Q3: What happens at first step? Random observations?**

**NO!** ❌ Not random.

At first step (reset):
1. EnergyPlus runs warmup (builds realistic initial state)
2. First timestep runs with **default schedules** (no action)
3. Observation = realistic initial state based on:
   - Weather
   - Building physics
   - Default HVAC schedules
   - Warmup results

**It's deterministic** (same weather → same initial state), not random.

---

## 🎯 **Practical Example for Your RBC Code**

```python
# Step 0: Reset
obs, info = env.reset()
# obs['air_temperature_space1'] = 16.8°C  ← Initial state (no action)

# Step 1: Apply winter setpoints (20°C, 23.5°C)
action = [20.0, 23.5, 20.0, 23.5, 20.0, 23.5, 20.0, 23.5, 20.0, 23.5]
obs, reward, done, info = env.step(action)
# obs['air_temperature_space1'] = 17.2°C  ← CHANGED! Shows effect of action

# Step 2: Keep same setpoints
obs, reward, done, info = env.step(action)
# obs['air_temperature_space1'] = 17.6°C  ← CHANGED AGAIN! Shows effect of action at step 2

# Step 3: Apply different setpoints
action2 = [22.0, 25.0, 22.0, 25.0, 22.0, 25.0, 22.0, 25.0, 22.0, 25.0]
obs, reward, done, info = env.step(action2)
# obs['air_temperature_space1'] = 17.8°C  ← CHANGED! Shows effect of action2
```

**Each observation shows the result of the action applied in that same step!**
