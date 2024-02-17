#   Omar Alshafei
#   Hung Tran
#   Marc Palacio
#   Gavin Cruz
#   Natalya McKay

import sys

def fifo_scheduler(processes, runTime):
    print(f"{len(processes)} processes")
    print(f"Using First-Come First-Served")

    curTime = 0
    isProcessRunning = False

    originalProcesses = processes[:]

    processes.sort(key=lambda x: x.arrivalTime)
    queue = []

    while curTime < runTime:
        for proc in processes:
            if proc.arrivalTime == curTime:
                queue.append(proc)
                print(f"Time {curTime} : {proc.name} arrived")
                
        if queue:
            if queue[0].remainingTime == 0:
                    print(f"Time {curTime} : {queue[0].name} finished")
                    queue[0].completionTime = curTime
                    queue[0].turnaround = curTime - queue[0].arrivalTime
                    queue.pop(0)
                    isProcessRunning = False
        
        if isProcessRunning == False:
            if queue:
                queue[0].startTime = curTime
                queue[0].waitTime = curTime - queue[0].arrivalTime
                queue[0].responseTime = curTime - queue[0].arrivalTime
                print(f"Time {curTime} : {queue[0].name} selected (burst   {queue[0].burstTime})")
                isProcessRunning = True

        if queue:            
            queue[0].remainingTime -=  1

        if not queue:
            print(f"Time {curTime} : Idle")

        curTime += 1

    print(f"Finished at time {curTime}\n")

    for process in originalProcesses:
        print(f"{process.name} wait Time\t{process.waitTime} turnaround\t{process.turnaround} response\t{process.responseTime}")

# Pre-emptive SJF Scheduling Algorithm Implementation
def preemptive_sjf(runTime, processes):
    finishedProcesses = []
    prevProc = None

    for curTime in range(runTime):
        validProcs = [p for p in processes if p.arrivalTime <= curTime]
        if not validProcs:
            print(f"Time {curTime} : Idle")
            continue

        for process in processes:
            if process.arrivalTime == curTime:
                print(f"Time {curTime} : {process.name} arrived")

        # ChatGPT; edited
        shortestProcess = min(validProcs, key=lambda p: p.burstTime)

        if shortestProcess.responseTime == -1:
            shortestProcess.responseTime = curTime - shortestProcess.arrivalTime

        if prevProc is None or (shortestProcess != prevProc and shortestProcess.burstTime < prevProc.burstTime):
            if shortestProcess.responseTime == -1:
                shortestProcess.responseTime = curTime - shortestProcess.arrivalTime
            print(f"Time {curTime} : {shortestProcess.name} selected (burst {shortestProcess.burstTime})")

        for process in processes:
            if process != shortestProcess and process.arrivalTime <= curTime:
                process.waitTime += 1

        shortestProcess.burstTime -= 1

        if shortestProcess.burstTime <= 0:
            finishedProcesses.append(shortestProcess)
            processes.remove(shortestProcess)
            shortestProcess.turnaroundTime = curTime + 1 - shortestProcess.arrivalTime
            print(f"Time {curTime + 1} : {shortestProcess.name} finished")
            shortestProcess = None

        prevProc = shortestProcess

    print(f"Finished at time {runTime}\n")

    finishedProcesses.sort(key=lambda x : x.name)
    for process in finishedProcesses:
        print(f"{process.name} wait Time\t{process.waitTime} turnaround\t{process.turnaroundTime} response\t{process.responseTime}")

# function which implements the round-robin CPU scheduling algorithm
def round_robin_scheduler(processes, runTime, quantum):
    # initialize an empty queue and list to hold finished processes
    queue = []
    finishedProcesses = []
    # initialize quantum remainder, current processes, and current time
    quantumRemainder = 0
    curProcesses = None
    curTime = 0

    # loop until the total runtime is reached
    while runTime > curTime:
        # check for processes arriving at current time and add them to the queue
        for process in processes:
            if process.arrivalTime == curTime:
                queue.append(process)
                print(f"Time {curTime} : {process.name} arrived")

        # given from chatgpt and refactored and edited
        if curProcesses is not None:
            if curProcesses.remainingTime == 0:
                print(f"Time {curTime} : {curProcesses.name} finished")
                finishedProcesses.append(curProcesses)
                curProcesses.turnaround = curTime - curProcesses.arrivalTime
                curProcesses.waitTime = curProcesses.turnaround - curProcesses.burstTime
                quantumRemainder = 0
                curProcesses = None
            elif quantumRemainder == 0:
                queue.append(curProcesses)


        # given from chatgpt and refactored and edited
        if queue and quantumRemainder == 0:
            quantumRemainder = quantum
            curProcesses = queue.pop(0)
            if curProcesses.responseTime == -1:
                curProcesses.responseTime = curTime - curProcesses.arrivalTime
            print(f"Time {curTime} : {curProcesses.name} selected (burst {curProcesses.remainingTime})")
        # handle idle time if no processes in queue
        elif len(queue) == 0 and quantumRemainder == 0:
            print(f"Time {curTime} : Idle")
            curTime += 1
            continue

        # given from chatgpt
        curProcesses.remainingTime -= 1
        curTime += 1
        quantumRemainder -= 1

    # print finished time and process details
    print(f"Finished at time   {curTime}\n")

    finishedProcesses.sort(key=lambda x : x.name)
    for process in finishedProcesses:
        print(f"{process.name} wait\t{process.waitTime} turnaround\t{process.turnaround} response\t{process.responseTime}")

            
class Process:
    def __init__(self, name, arrivalTime, burstTime):
        self.name = name
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remainingTime = burstTime
        self.completionTime = 0
        self.startTime = -1
        self.waitTime = 0
        self.responseTime = -1
        self.turnaround = 0


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

        if not process_count: 
            print("Error: Missing parameter processcount")
            exit(1)
        if not run_for:
            print("Error: Missing parameter runfor")
            exit(1)
        if not use_algorithm:
            print("Error: Missing parameter use")
            exit(1)
        if use_algorithm == 'rr' and not quantum:
            print("Error: Missing quantum parameter when use is 'rr'")
            exit(1)

        return processes, use_algorithm, quantum, run_for

    except (IOError, ValueError, IndexError) as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    input_filename = 'c10-fcfs.in'
    processes, algorithm, quantum, runTime = read_input_file(input_filename)

    if algorithm == 'fcfs':
        fifo_scheduler(processes, runTime)
    elif algorithm == 'sjf':
        preemptive_sjf(runTime, processes)
    elif algorithm == 'rr':
        print(f"{len(processes)} processes\nUsing Round-Robin\nQuantum {quantum}\n")
        round_robin_scheduler(processes, runTime, quantum)
    else:
        print(f"Error: Invalid algorithm - {algorithm}") ## human added

if __name__ == "__main__":
    main()
