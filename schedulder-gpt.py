#Omar Alshafei
#Hung Tran

import sys

# recieved from ChatGPT but revised and edited
# FIFO Scheduling Algorithm Implementation
def fifo_scheduler(processes, run_time):
    print(f"{len(processes)} processes")
    print(f"Using First-Come First-Served")

    current_time = 0
    process_currently_running = False

    # recieved from ChatGPT
    # Create a copy of the original processes list
    original_processes_order = processes[:]

    processes.sort(key=lambda x: x.arrival_time)
    queue = []

    while current_time < run_time:
        #   Goes through the list of proccesses and compares
        #   arrival time with the current time
        #   This should be first to ensure since arrivals
        #   have seem to always come first in outputs
        for proc in processes:
            if proc.arrival_time == current_time:
                queue.append(proc)
                print(f"Time {current_time} : {proc.name} arrived")
                
        if queue:
            if queue[0].remaining_time == 0:
                    print(f"Time {current_time} : {queue[0].name} finished")
                    queue[0].completion_time = current_time
                    queue[0].turnaround = current_time - queue[0].arrival_time
                    queue.pop(0)
                    process_currently_running = False
        
        #   Checks if a proccess is running
        #   If not, checks if the queue is empty
        #   If its not, grabs the first element, then
        #   "Selects" it
        if process_currently_running == False:
            if queue:
                queue[0].start_time = current_time
                queue[0].wait = current_time - queue[0].arrival_time
                queue[0].response = current_time - queue[0].arrival_time
                print(f"Time {current_time} : {queue[0].name} selected (burst   {queue[0].burst_time})")
                process_currently_running = True

        #   Checks if the queue is empty
        if queue:            
            #   Subtract one unit of time from the first element
            #   (This element is the one that is currently running)
            queue[0].remaining_time -=  1

        if not queue:
            print(f"Time {current_time} : Idle")

        current_time += 1

    print(f"Finished at time {current_time}\n")

    # recieved from ChatGPT and edited
    for process in original_processes_order:
        print(f"{process.name} wait Time\t{process.wait} turnaround\t{process.turnaround} response\t{process.response}")

# Pre-emptive SJF Scheduling Algorithm Implementation
def preemptive_sjf(total_time, processes):
    current_time = 0
    completed_processes = []
    previous_process = None

    for current_time in range(total_time):
        eligible_processes = [p for p in processes if p.arrival_time <= current_time]
        if not eligible_processes:
            print(f"Time {current_time} : Idle")
            continue

        for p in processes:
            if p.arrival_time == current_time:
                print(f"Time {current_time} : {p.name} arrived")

        shortest_process = min(eligible_processes, key=lambda p: p.burst_time)

        if shortest_process.response_time == -1:
            shortest_process.response_time = current_time - shortest_process.arrival_time

        if previous_process is None or (shortest_process != previous_process and shortest_process.burst_time < previous_process.burst_time):
            if shortest_process.response_time == -1:
                shortest_process.response_time = current_time - shortest_process.arrival_time
            print(f"Time {current_time} : {shortest_process.name} selected (burst {shortest_process.burst_time})")

        for p in processes:
            if p != shortest_process and p.arrival_time <= current_time:
                p.wait_time += 1

        shortest_process.burst_time -= 1

        if shortest_process.burst_time <= 0:
            completed_processes.append(shortest_process)
            processes.remove(shortest_process)
            shortest_process.turnaround_time = current_time + 1 - shortest_process.arrival_time
            print(f"Time {current_time + 1} : {shortest_process.name} finished")
            shortest_process = None

        previous_process = shortest_process

    print(f"Finished at time  {total_time}")

    unfinished_processes = [p for p in processes if p.burst_time > 0]

    if unfinished_processes:
        print("Processes that did not finish:")
        for p in unfinished_processes:
            print(f"{p.name} (burst {p.burst_time})")

def round_robin_scheduler(processes, run_for, quantum):
    current_time = 0
    ready_queue = []  # Initialize ready queue with no processes
    completed_processes = []
    quantum_remainder = 0
    current_process = None

    while current_time < run_for:
        # Check for arrival_times
        for process in processes:
            if process.arrival_time == current_time:
                ready_queue.append(process)
                print(f"Time {current_time} : {process.name} arrived")

        if current_process is not None:
            if current_process.remaining_time == 0:
                print(f"Time {current_time} : {current_process.name} finished")
                completed_processes.append(current_process)
                current_process.turnaround_time = current_time - current_process.arrival_time
                current_process.wait_time = current_process.turnaround_time - current_process.burst_time
                quantum_remainder = 0
                current_process = None
            elif quantum_remainder == 0:
                ready_queue.append(current_process)

        # Select process to execute
        if ready_queue and quantum_remainder == 0:
            quantum_remainder = quantum
            current_process = ready_queue.pop(0)
            if current_process.response_time == -1:
                current_process.response_time = current_time - current_process.arrival_time
            print(f"Time {current_time} : {current_process.name} selected (burst_time {current_process.remaining_time})")
        elif len(ready_queue) == 0 and quantum_remainder == 0:
            print(f"Time {current_time} : Idle")
            current_time += 1
            continue

        current_time += 1
        current_process.remaining_time -= 1
        quantum_remainder -= 1

    print(f"Finished at time   {current_time}\n")

    # Output the completed processes with statistics
    for process in processes:
        if process.turnaround_time > 0:
            print(f"{process.name} wait  {process.wait_time} turnaround  {process.turnaround_time} response  {process.response_time}")

    for process in processes:
        if process.turnaround_time == 0:
            print(f"{process.name} did not finish")


class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.start_time = -1
        self.wait_time = 0
        self.response_time = -1
        self.wait = 0
        self.turnaround = 0
        self.response = 0

def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Parse directives
        process_count = int(lines[0].split()[1])
        run_for = int(lines[1].split()[1])
        use_algorithm = lines[2].split()[1]

        if use_algorithm == 'rr':
            quantum = int(lines[3].split()[1])
            lines = lines[4:]
        else:
            quantum = None
            lines = lines[3:]

        # Parse processes
        processes = []
        for line in lines:
            if line.strip() == 'end':
                break

            parts = line.split()
            if parts[0] == 'process':
                name = parts[2]
                arrival = int(parts[4])
                burst = int(parts[6])
                processes.append(Process(name, arrival, burst))

        return processes, use_algorithm, quantum, run_for

    except (IOError, ValueError, IndexError) as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    input_filename = 'c10-rr.in'
    processes, algorithm, quantum, runTime = read_input_file(input_filename)

    if algorithm == 'fcfs':
        fifo_scheduler(processes, runTime)
    elif algorithm == 'sjf':
        preemptive_sjf(runTime, processes)
    elif algorithm == 'rr':
        print(f"{len(processes)} processes\nUsing Round-Robin\nQuantum {quantum}")
        round_robin_scheduler(processes, runTime, quantum)

if __name__ == "__main__":
    main()

