# -----------------------------
# Call Center Simulation - Case Study
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
SIM_TIME = 480  # 8 hours in minutes

# Create folder for charts
os.makedirs("charts", exist_ok=True)

# -----------------------------
# Scenario Setup
# -----------------------------
SCENARIOS = {
    "Base Case": {"num_agents": 3, "service_time": 5, "arrival_rate": 3},
    "More Agents": {"num_agents": 5, "service_time": 5, "arrival_rate": 3},
    "Faster Service": {"num_agents": 3, "service_time": 4, "arrival_rate": 3},
}

# -----------------------------
# Metrics Storage
# -----------------------------
results = {}

# -----------------------------
# Call Process
# -----------------------------
def call_process(env, agents, service_time, metrics):
    arrival_time = env.now
    with agents.request() as request:
        yield request
        wait_time = env.now - arrival_time
        metrics['wait_times'].append(wait_time)
        metrics['agent_busy_time'] += service_time
        yield env.timeout(random.expovariate(1.0 / service_time))
        metrics['calls_handled'] += 1

# -----------------------------
# Call Arrival Process
# -----------------------------
def call_arrivals(env, agents, service_time, arrival_rate, metrics):
    call_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_rate))
        call_id += 1
        env.process(call_process(env, agents, service_time, metrics))

# -----------------------------
# Queue Length Tracker
# -----------------------------
def track_queue(env, agents, metrics):
    while True:
        metrics['queue_lengths'].append(len(agents.queue))
        yield env.timeout(1)

# -----------------------------
# Run Simulation
# -----------------------------
for scenario_name, params in SCENARIOS.items():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=params["num_agents"])

    metrics = {
        "wait_times": [],
        "agent_busy_time": 0,
        "calls_handled": 0,
        "queue_lengths": []
    }

    env.process(call_arrivals(env, agents, params['service_time'], params['arrival_rate'], metrics))
    env.process(track_queue(env, agents, metrics))
    env.run(until=SIM_TIME)

    avg_wait = np.mean(metrics['wait_times']) if metrics['wait_times'] else 0
    utilization = metrics['agent_busy_time'] / (SIM_TIME * params['num_agents'])
    avg_queue = np.mean(metrics['queue_lengths']) if metrics['queue_lengths'] else 0

    results[scenario_name] = {
        "Average Wait Time": round(avg_wait, 2),
        "Agent Utilization": round(utilization, 2),
        "Calls Handled": metrics['calls_handled'],
        "Average Queue Length": round(avg_queue, 2)
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
avg_waits = [results[s]['Average Wait Time'] for s in scenarios]
utilization = [results[s]['Agent Utilization'] for s in scenarios]
calls_handled = [results[s]['Calls Handled'] for s in scenarios]
avg_queue = [results[s]['Average Queue Length'] for s in scenarios]

plt.figure(figsize=(16,4))

plt.subplot(1,4,1)
plt.bar(scenarios, avg_waits, color='skyblue')
plt.ylabel('Minutes')
plt.title('Average Wait Time')

plt.subplot(1,4,2)
plt.bar(scenarios, utilization, color='lightgreen')
plt.ylabel('Utilization')
plt.title('Agent Utilization')

plt.subplot(1,4,3)
plt.bar(scenarios, calls_handled, color='salmon')
plt.ylabel('Calls Handled')
plt.title('Call Throughput')

plt.subplot(1,4,4)
plt.bar(scenarios, avg_queue, color='violet')
plt.ylabel('Queue Length')
plt.title('Average Queue Length')

plt.tight_layout()
plt.savefig("charts/call_center_results.png")
plt.show()
