class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.response_time = None

def parse_input(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    params = {}
    processes = []

    for line in lines:
        parts = line.split()
        if parts[0] == 'processcount':
            params['process_count'] = int(parts[1])
        elif parts[0] == 'runfor':
            params['run_for'] = int(parts[1])
        elif parts[0] == 'use':
            params['algorithm'] = parts[1]
            if params['algorithm'] == 'rr':
                if len(parts) < 3:
                    print("Error: Missing quantum parameter when use is 'rr'")
                    exit(1)
                params['quantum'] = int(parts[2])
        elif parts[0] == 'process':
            name = parts[2]
            arrival_time = int(parts[4])
            burst_time = int(parts[6])
            processes.append(Process(name, arrival_time, burst_time))

    return params, processes

def scheduler_fcfs(processes, run_for):
    timeline = []
    current_time = 0

    for process in processes:
        if process.arrival_time > current_time:
            timeline.append((current_time, 'Idle'))
            current_time = process.arrival_time
        timeline.append((current_time, process.name + ' selected (burst ' + str(process.burst_time) + ')'))
        process.start_time = current_time
        process.end_time = current_time + process.burst_time
        current_time = process.end_time
        timeline.append((current_time, process.name + ' finished'))
    
    if current_time < run_for:
        timeline.append((current_time, 'Idle'))
        current_time = run_for
    
    return timeline

def scheduler_sjf(processes, run_for):
    timeline = []
    current_time = 0
    remaining_processes = processes.copy()

    while current_time < run_for and remaining_processes:
        ready_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
        if ready_processes:
            shortest_job = min(ready_processes, key=lambda x: x.remaining_time)
            timeline.append((current_time, shortest_job.name + ' selected (burst ' + str(shortest_job.remaining_time) + ')'))
            if shortest_job.start_time is None:
                shortest_job.start_time = current_time
                shortest_job.response_time = current_time - shortest_job.arrival_time
            execute_time = min(shortest_job.remaining_time, run_for - current_time)
            shortest_job.remaining_time -= execute_time
            current_time += execute_time
            if shortest_job.remaining_time == 0:
                shortest_job.end_time = current_time
                timeline.append((current_time, shortest_job.name + ' finished'))
                remaining_processes.remove(shortest_job)
        else:
            timeline.append((current_time, 'Idle'))
            current_time += 1
    
    if current_time < run_for:
        timeline.append((current_time, 'Idle'))
        current_time = run_for
    
    return timeline

def scheduler_rr(processes, run_for, quantum):
    timeline = []
    current_time = 0
    remaining_processes = processes.copy()

    while current_time < run_for and remaining_processes:
        ready_processes = [p for p in remaining_processes if p.arrival_time <= current_time]
        if ready_processes:
            for process in ready_processes:
                timeline.append((current_time, process.name + ' selected (burst ' + str(min(quantum, process.remaining_time)) + ')'))
                if process.start_time is None:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                execute_time = min(quantum, process.remaining_time, run_for - current_time)
                process.remaining_time -= execute_time
                current_time += execute_time
                if process.remaining_time == 0:
                    process.end_time = current_time
                    timeline.append((current_time, process.name + ' finished'))
                    remaining_processes.remove(process)
                    break
        else:
            timeline.append((current_time, 'Idle'))
            current_time += 1
    
    if current_time < run_for:
        timeline.append((current_time, 'Idle'))
        current_time = run_for
    
    return timeline

def calculate_metrics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    finished_processes = [p for p in processes if p.end_time is not None]

    for process in finished_processes:
        total_turnaround_time += process.end_time - process.arrival_time
        total_waiting_time += process.start_time - process.arrival_time
        total_response_time += process.response_time

    avg_turnaround_time = total_turnaround_time / len(finished_processes)
    avg_waiting_time = total_waiting_time / len(finished_processes)
    avg_response_time = total_response_time / len(finished_processes)

    return avg_turnaround_time, avg_waiting_time, avg_response_time

def main(input_file):
    params, processes = parse_input(input_file)

    if params['algorithm'] == 'fcfs':
        timeline = scheduler_fcfs(processes, params['run_for'])
    elif params['algorithm'] == 'sjf':
        timeline = scheduler_sjf(processes, params['run_for'])
    elif params['algorithm'] == 'rr':
        timeline = scheduler_rr(processes, params['run_for'], params['quantum'])

    avg_turnaround_time, avg_waiting_time, avg_response_time = calculate_metrics(processes)

    with open(input_file[:-3] + 'out', 'w') as f:
        f.write(str(len(processes)) + ' processes\n')
        f.write('Using preemptive ' + params['algorithm'].upper() + '\n')
        if params['algorithm'] == 'rr':
            f.write('Quantum: ' + str(params['quantum']) + '\n')
        for time, event in timeline:
            f.write('Time ' + str(time).rjust(4) + ' : ' + event + '\n')
        f.write('Finished at time ' + str(params['run_for']) + '\n\n')
        f.write('Average turnaround time: {:.2f}\n'.format(avg_turnaround_time))
        f.write('Average waiting time: {:.2f}\n'.format(avg_waiting_time))
        f.write('Average response time: {:.2f}\n'.format(avg_response_time))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        exit(1)
    main(sys.argv[1])
