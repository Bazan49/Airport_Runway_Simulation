import random
from rv_generators import generate_exponential, generate_normal
from parallel_servers_simulation import ParallelServersSimulation
import math

def arrival_generator():
    """Generate the inter‑arrival time for an aircraft at the airport.

    The time between consecutive arrivals follows an exponential distribution
    with a mean of 20 minutes.

    """
    return generate_exponential(1/20)

def service_time_generator():
    """Generate the total time an aircraft occupies a runway.

    The runway occupancy is the sum of the following sequential activities:
    1. Refuelling – exponential, mean 30 minutes (starts at landing).
    2. Landing and take‑off – normal, mean 10 minutes, std 5 minutes.
    3. Cargo loading/unloading – occurs with probability 0.5;
       if it occurs, its duration is exponential with mean 30 minutes.
    4. Repair due to breakdown – occurs with probability 0.1 (just before
       take‑off); if it occurs, its duration is exponential with mean 15 minutes.

    All activities are performed one after another, so the total occupancy
    time is the sum of their independent durations.

    """
    # 1. Refuelling (always performed)
    refuel_time = generate_exponential(1/30)

    # 2. Landing and take‑off
    landing_takeoff_time = generate_normal(10,5)

    # 3. Cargo loading/unloading (50 % probability)
    cargo_time = 0.0
    if random.random() < 0.5:
        cargo_time = generate_exponential(1/30)

    # 4. Repair due to breakdown (10 % probability)
    repair_time = 0.0
    if random.random() < 0.1:
        repair_time = generate_exponential(1/15)

    return refuel_time + landing_takeoff_time + cargo_time + repair_time

def simulate_airport():
    """Run the airport runway simulation with multiple replications."""
    one_week = 10080          # total minutes in a week
    desired_precision = 10.0  # desired standard error (minutes)
    num_servers = 5           # number of parallel runways
    max_replications = 5000

    # Store idle times for each runway across replications
    idle_data = [[] for _ in range(num_servers)]
    # Store arrival counts for each replication 
    arrival_counts = []

    n = 0                     # number of completed replications
    while n < max_replications:
        sim = ParallelServersSimulation(
            server_num=num_servers,
            total_time=one_week,
            arrival_generator=arrival_generator,
            service_time_generator=service_time_generator
        )
        arrival_times, _, idle_times = sim.run()
        num_arrivals = len(arrival_times)
        arrival_counts.append(num_arrivals)

        for i in range(num_servers):
            idle_data[i].append(idle_times[i])

        n += 1

        # Check precision every 10 replications
        if n % 10 == 0:
            std_errors = []
            for i in range(num_servers):
                sample = idle_data[i]
                mean = sum(sample) / n
                # sample variance
                variance = sum((x - mean) ** 2 for x in sample) / (n - 1)
                std_err = math.sqrt(variance) / math.sqrt(n)
                std_errors.append(std_err)

            max_error = max(std_errors)

            if max_error < desired_precision:
                print(f"Precision reached after {n} replications.")
                break
    else:
        print(f"Maximum number of replications ({max_replications}) reached without achieving the desired precision.")

    # Print final results
    print("\nFinal results:")
    print(f"\nAverage number of arrivals per week: {sum(arrival_counts) / n:.1f}")
    print("\nIdle time statistics for each runway:")
    for i in range(num_servers):
        sample = idle_data[i]
        mean = sum(sample) / n
        variance = sum((x - mean) ** 2 for x in sample) / (n - 1)
        std_dev = math.sqrt(variance)
        std_err = std_dev / math.sqrt(n)
        print(f"Runway {i+1}: mean = {mean:.1f} min, std_dev = {std_dev:.1f} min, std_err = {std_err:.1f} min")

if __name__ == "__main__":
    simulate_airport()