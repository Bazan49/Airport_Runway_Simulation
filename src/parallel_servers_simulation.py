from collections import deque
import math
import random

class ParallelServersSimulation:

    """
    Simulates a multi-server queueing system with identical parallel servers,
    a single FIFO queue, and a finite time horizon.

    Parameters
    ----------
    server_num : int
        Number of servers.
    total_time : float
        Time horizon (T). After T no new arrivals are generated, but the system
        continues serving until it empties.
    arrival_generator : function
        Function that generates inter-arrival times (time between consecutive arrivals).
    service_time_generator : function
        Function that generates service times.
    """

    def __init__(self, server_num, total_time, arrival_generator, service_time_generator):

        self.server_num = server_num
        self.T = total_time
        self.arrival_generator = arrival_generator
        self.service_time_generator = service_time_generator
        self.initialize()
        
    def initialize(self):
        """Set initial state and schedule the first arrival."""

        # System clock
        self.t = 0 
        # Next arrival time (schedule first arrival)
        self.ta = self.generate_arrival()
        # Next departure times for each server (inf if idle)
        self.td = [math.inf] * self.server_num 

        # Counters
        self.arrival_count = 0 
        self.departure_counts = [0] * self.server_num 
        self.arrival_times = [] # arrival times[i] -> arrival time of customer i + 1
        self.departure_times =  [{} for _ in range(self.server_num)]  # per server: {customer_id: departure_time}
        self.idle_times = [0] * self.server_num  # total idle time per server
        self.last_idle_start = [0] * self.server_num   # time of last idle start for each server

        # State variables
        self.n = 0 # customers in system (queue + servers)
        self.queue = deque()  # FIFO queue of customer IDs
        self.server_customers = [0] * self.server_num # server_customers[i] -> 0 = idle, otherwise customer i being served
        
    def run(self):
        """Run the simulation until the system is empty after time T."""

        while True:
            # Termination condition: system empty and no future arrivals within horizon
            if(self.n == 0 and self.ta > self.T): 
                break

            # Next departure is the earliest among all servers
            next_departure_time = min(self.td)

            if(self.ta <= next_departure_time):
                if(self.ta <= self.T):
                    self.process_arrival()
                else:
                    self.ta = math.inf # cancel further arrivals

            else: 
                # Next event is a departure
                server_index = self.td.index(next_departure_time)
                self.process_departure(server_index)

        # Update idle times for servers that are idle at the end of the simulation
        for i in range(self.server_num):
            self.idle_times[i] += self.T - self.last_idle_start[i]

        return self.arrival_times, self.departure_times, self.idle_times

    def process_arrival(self):
        """Process a customer arrival."""

        # Advance clock to the arrival instant
        self.t = self.ta

        # Schedule next arrival
        interarrival = self.generate_arrival()
        self.ta = self.t + interarrival

        # Record arrival
        self.arrival_count += 1
        customer_id = self.arrival_count
        self.arrival_times.append(self.t)
        self.n += 1

        idle_servers = [i for i in range(self.server_num) if self.server_customers[i] == 0]
        if len(idle_servers) == 0: # all servers busy -> join the queue
            self.queue.append(customer_id)
        else:
            i = random.choice(idle_servers) # pick a random idle server
            self.idle_times[i] += self.t - self.last_idle_start[i]  # update idle time
            self.server_customers[i] = customer_id
            service_time = self.generate_service_time()
            self.td[i] = self.t + service_time # schedule departure
            
    def process_departure(self, server_index):
        """Process a service completion on a given server."""

        # Advance clock to the departure instant
        self.t = self.td[server_index]

        # Record departure
        customer_id = self.server_customers[server_index]
        self.departure_counts[server_index] += 1
        self.departure_times[server_index][customer_id] = self.t 
        self.n -= 1

        # Check the queue for waiting customers
        if len(self.queue) > 0: 
            next_client = self.queue.popleft()
            self.server_customers[server_index] = next_client
            service_time = self.generate_service_time()
            self.td[server_index] = self.t + service_time
        else: 
            # Server becomes idle
            self.server_customers[server_index] = 0
            self.last_idle_start[server_index] = self.t
            self.td[server_index] = math.inf

    def generate_service_time(self):
        return self.service_time_generator()

    def generate_arrival(self):
        return self.arrival_generator()
