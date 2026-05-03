import random
from rv_generators import generate_exponential, generate_normal, generate_uniform
from parallel_servers_simulation import ParallelServersSimulation

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

def main():
    one_week = 10080  # minutes in a week
    
    sim = ParallelServersSimulation(
        server_num=5,
        total_time=one_week,
        arrival_generator=arrival_generator,
        service_time_generator=service_time_generator
    )
    arrival_times, departure_times, idle_times = sim.run()

    print("Inactivity times for each runway over one week:")
    for i, idle in enumerate(idle_times):
        print(f"  Runway {i+1}: {idle:.2f} min")

if __name__ == "__main__":
    main()