import sys




# FIFO Scheduling Algorithm Implementation
def fifo_scheduler(processes):
    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival)

    current_time = 0
    for process in processes:
        if process.arrival > current_time:
            print(f"Time {current_time} : Idle")
            current_time = process.arrival
        print(f"Time {current_time} : {process.name} selected (burst {process.burst})")
        current_time += process.burst
        print(f"Time {current_time} : {process.name} finished")

# Pre-emptive SJF Scheduling Algorithm Implementation
def sjf_scheduler(processes):
    current_time = 0
    while processes:
        ready_processes = [p for p in processes if p.arrival <= current_time]
        if not ready_processes:
            print(f"Time {current_time} : Idle")
            current_time += 1
            continue

        shortest_process = min(ready_processes, key=lambda x: x.burst)
        processes.remove(shortest_process)
        print(f"Time {current_time} : {shortest_process.name} selected (burst {shortest_process.burst})")
        current_time += shortest_process.burst
        print(f"Time {current_time} : {shortest_process.name} finished")

# Round Robin Scheduling Algorithm Implementation

    print(f"Finished at time {current_time}")  # To match the last "Idle" in the provided output

def round_robin_scheduler(processes, quantum):
    current_time = 0
    quantum_used = 0

    while processes:
        ready_processes = [p for p in processes if p.arrival <= current_time]
        if not ready_processes:
            print(f"Time {current_time} : Idle")
            current_time += 1
            continue

        for process in ready_processes:
            if process.arrival == current_time and process.status == "Not Started":
                print(f"Time {current_time} : {process.name} arrived")    
            if process.status == "Not Started": 
                print(f"Time {current_time} : {process.name} selected (burst {process.burst})")
                process.status = "Running"
            else:
                print(f"Time {current_time} : {process.name} selected (burst {process.burst})")

            time_slice = min(quantum, process.burst)
            process.burst -= time_slice
            for x in range(time_slice):
                for proc in processes:
                        if proc.arrival == current_time and proc != process:
                            print(f"Time {current_time} : {proc.name} arrived")
                            proc.status = "Running"
                            ready_processes.append(proc)
                current_time += 1
            #quantum_used = time_slice

            if process.burst == 0:
                print(f"Time {current_time} : {process.name} finished")
                process.status = "Finished"
                processes.remove(process)

        #if quantum_used < quantum:
            #print(f"Time {current_time} : Idle")
            #current_time += 1
        

    print(f"Finished at time {current_time}")  # To match the last "Idle" in the provided output


class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.status = "Not Started"

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
    """
    # Check command-line arguments
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".in"):
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)
    """
    input_filename = 'c5-rr.in'
    processes, algorithm, quantum, runTime = read_input_file(input_filename)

    if algorithm == 'fcfs':
        fifo_scheduler(processes, runTime)
    elif algorithm == 'sjf':
        sjf_scheduler(processes, runTime)
    elif algorithm == 'rr':
        print(f"{len(processes)} processes\nUsing Round-Robin\nQuantum {quantum}")
        round_robin_scheduler(processes, quantum)

    # Implement other output generation and error checking logic here
    # Write results to output file

if __name__ == "__main__":
    main()