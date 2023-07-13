

class Task:
    def __init__(self, number, period, execution_time, priority=0) -> None:
        self.number = number
        self.period = period
        self.next_start : int = period
        self.next_deadline : int = period
        self.execution_time : int = execution_time
        self.remaining_time : int = execution_time
        self.executed = False
        self.priority = priority
        self.execution_chart = []
        self.execution_endings = []

    def __repr__(self) -> str:
        return f"Task{self.number}"
    
    def execute(self, start_time, execution_time: int) -> bool:
        self.remaining_time -= execution_time
        if self.remaining_time <= 0:
            if start_time + execution_time > self.next_deadline:
                print(f"task{self.number} failed to execute at {start_time + execution_time}, deadline was {self.next_deadline}")
            self.executed = True
            self.execution_endings.append(start_time + execution_time)
        self.execution_gantt(start_time, execution_time)
    
    def start_task(self) -> None:
        self.next_start += self.period
        self.next_deadline += self.period
        print(f"next deadline for task{self.number} is {self.next_deadline}")
        self.remaining_time = self.execution_time
        self.executed = False

    def execution_gantt(self, start_time: int, execution: int) -> str:
        self.execution_chart.append([start_time, execution])