
# Call Center Simulation

## 1. Overview

This project simulates a **call center system** using Python and `SimPy`.
The main goal is to analyze how different setups affect:

* Average wait time of calls
* Agent utilization
* Total calls handled

This helps understand how changing agents or service speed impacts call center performance.



## 2. Requirements

* Python 3.x
* Packages:

  * `simpy`
  * `numpy`
  * `matplotlib`

Install packages using:

```bash
pip install simpy numpy matplotlib
```



## 3. How to Run

1. Save the code as `call_center_sim.py`.
2. Open terminal/command prompt in the file's folder.
3. Run the script:

```bash
python call_center_sim.py
```

4. Output:

   * **Console:** Shows average wait time, agent utilization, and calls handled for each scenario.
   * **Plot:** Displays bar charts comparing all scenarios:

     * Average Wait Time
     * Agent Utilization
     * Call Throughput



## 4. Simulation Setup

* **Simulation Time:** 480 minutes
* **Random Seed:** 42 (for reproducibility)
* **Scenarios:**

| Scenario       | Agents | Service Time (min) | Arrival Rate (min) |
| -------------- | ------ | ------------------ | ------------------ |
| Base Case      | 3      | 4                  | 2                  |
| More Agents    | 5      | 4                  | 2                  |
| Faster Service | 3      | 3                  | 2                  |

* You can modify `SCENARIOS` to add new configurations.



## 5. Simulation Workflow

1. **Define Scenarios**

   * Specify number of agents, service time, and call arrival rate.

2. **Initialize Environment**

   * Set up `simpy.Environment()` and agent resources.
   * Initialize metrics for wait times, calls handled, and agent busy time.

3. **Call Arrivals**

   * Calls arrive randomly using an exponential distribution.
   * Each call requests an available agent.

4. **Call Handling**

   * When an agent is available, process the call with random service time.
   * Record wait time and agent busy time.
   * Increment the number of calls handled.

5. **Run Simulation**

   * Repeat the process until simulation time ends.
   * Compute metrics: average wait time, agent utilization, calls handled.

6. **Analyze & Visualize**

   * Print metrics to console.
   * Plot bar charts for easy comparison of scenarios.



## 6. Output

**Console Example:**

```
Simulation Results:

Base Case:
  Average Wait Time (min): 2.45
  Agent Utilization: 0.81
  Calls Handled: 120

More Agents:
  Average Wait Time (min): 1.12
  Agent Utilization: 0.65
  Calls Handled: 125
```

**Visualization:**

* Three bar charts showing comparison of:

  1. Average Wait Time
  2. Agent Utilization
  3. Call Throughput



## 7. Customization

* Change number of agents, service time, or arrival rate in `SCENARIOS`.
* Adjust `SIM_TIME` for longer or shorter simulations.
* Modify `RANDOM_SEED` for different random behavior.



## 8. Workflow Diagram

**Step-by-step process:**

```
Define Scenarios
        ↓
Initialize Simulation
        ↓
Generate Call Arrivals
        ↓
Assign Agent to Call
        ↓
Process Call (Service)
        ↓
Record Metrics
        ↓
Repeat for All Calls & Scenarios
        ↓
Analyze & Visualize Results
```



