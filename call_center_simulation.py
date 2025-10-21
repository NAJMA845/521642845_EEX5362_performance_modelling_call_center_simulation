# -----------------------------
# Call Center Simulation
# -----------------------------

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# Simulation Parameters
# -----------------------------
RANDOM_SEED = 42
SIM_TIME = 480  # Total time in minutes (8 hours)

# Create charts folder if it doesn't exist
if not os.path.exists("charts"):
    os.makedirs("charts")

# Define three realistic scenarios
SCENARIOS = {
    "Base Case": {"num_agents": 3, "service_time": 5, "arrival_rate": 3},  # 1 call every 3 min
    "More Agents": {"num_agents": 5, "service_time": 5, "arrival_rate": 3},
    "Faster Service": {"num_agents": 3, "service_time": 4, "arrival_rate": 3},
}

# -----------------------------
# Metrics Storage
# -----------------------------
results = {}

# -----------------------------
# Define Call Process
# -----------------------------
def call_process(env, name, agents, service_time, metrics):
    arrival_time = env.now
    with agents.request() as request:
        yield request
        wait_time = env.now - arrival_time
        metrics['wait_times'].append(wait_time)
        metrics['agent_busy_time'] += service_time
        yield env.timeout(random.expovariate(1.0 / service_time))
        metrics['calls_handled'] += 1

# -----------------------------
# Define Call Arrival Process
# -----------------------------
def call_arrivals(env, agents, service_time, arrival_rate, metrics):
    call_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_rate))
        call_id += 1
        env.process(call_process(env, f"Call {call_id}", agents, service_time, metrics))

# -----------------------------
# Run Simulation for Each Scenario
# -----------------------------
for scenario_name, params in SCENARIOS.items():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=params["num_agents"])

    metrics = {
        "wait_times": [],
        "agent_busy_time": 0,
        "calls_handled": 0
    }

    env.process(call_arrivals(env, agents, params['service_time'], params['arrival_rate'], metrics))
    env.run(until=SIM_TIME)

    avg_wait = np.mean(metrics['wait_times']) if metrics['wait_times'] else 0
    utilization = metrics['agent_busy_time'] / (SIM_TIME * params['num_agents'])

    results[scenario_name] = {
        "Average Wait Time (min)": round(avg_wait, 2),
        "Agent Utilization": round(utilization, 2),
        "Calls Handled": metrics['calls_handled']
    }

# -----------------------------
# Display Results
# -----------------------------
print("Simulation Results:")
for scenario, metrics in results.items():
    print(f"\n{scenario}:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

# -----------------------------
# Visualization
# -----------------------------
scenarios = list(results.keys())
avg_waits = [results[s]['Average Wait Time (min)'] for s in scenarios]
utilization = [results[s]['Agent Utilization'] for s in scenarios]
calls_handled = [results[s]['Calls Handled'] for s in scenarios]

plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.bar(scenarios, avg_waits, color='skyblue')
plt.ylabel('Minutes')
plt.title('Average Wait Time')
plt.savefig("charts/avg_wait_time.png")

plt.subplot(1,3,2)
plt.bar(scenarios, utilization, color='lightgreen')
plt.ylabel('Utilization')
plt.title('Agent Utilization')
plt.savefig("charts/agent_utilization.png")

plt.subplot(1,3,3)
plt.bar(scenarios, calls_handled, color='salmon')
plt.ylabel('Calls Handled')
plt.title('Call Throughput')
plt.savefig("charts/calls_handled.png")

plt.tight_layout()
plt.show()
