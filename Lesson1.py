import simpy
import numpy as np
import pandas as pd


# Input data
customers = [1, 2, 3, 4]
arrival_times = [7, 11, 16, 23]
service_times = [4, 6, 5, 4]


# Output tracking lists
start_service = []
end_service = []
waiting_times = []
time_in_system = []


# Single queue process
def customer(env, name, arrival_time, service_time, server):
    yield env.timeout(arrival_time - env.now)  # Wait trigger until arrival time
    arrival = env.now


    # Request the server (1 queue)
    with server.request() as req:
        yield req
        start = env.now
        start_service.append(start)
        waiting_times.append(start - arrival) # Time customer wait in queue for ith customer = Arrival time ofth customer - Time service begin of th customer


        yield env.timeout(service_time)
        end = env.now # set the end to until when the service time is completed
        end_service.append(end) # add the end time to the results array
        time_in_system.append(end - arrival) # Time customer spends in system = Time service ends of th customer - Arrival time ofth customer


        print(f"Customer {name} | Arrival: {arrival} | Start: {start} | End: {end} | Wait: {start - arrival}")


# Create environment
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)


# Initialize lists
start_service.clear()
end_service.clear()
waiting_times.clear()
time_in_system.clear()


# Start processes
for i in range(len(customers)):
    env.process(customer(env, customers[i], arrival_times[i], service_times[i], server))


# Run simulation
env.run()


# Build adjacency matrix
n = len(customers)
adj_matrix = np.zeros((n, n), dtype=int)


for i in range(n):
    for j in range(n):
        # If customer i finishes before customer j starts → adjacency = 1
        if end_service[i] <= start_service[j]:
            adj_matrix[i][j] = 1


# Create results table
df = pd.DataFrame({
    "Customer": customers,
    "Arrival Time": arrival_times,
    "Service Time": service_times,
    "Service Start": start_service,
    "Service End": end_service,
    "Waiting Time": waiting_times,
    "Time in System": time_in_system
})


print("\n=== Customer Service Table ===")
print(df)
print("\n=== Adjacency Matrix ===")
print(adj_matrix)
