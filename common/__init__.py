

class Task:
    def __init__(self, number, period, execution_time, priority=0) -> None:
        self.number = number
        self.period = period
        self.next_start : float = 0
        self.next_deadline : float = period
        self.execution_time : float = execution_time
        self.remaining_time : float = execution_time
        self.executed = False
        self.priority = priority
        self.execution_chart = []
        self.execution_endings = []

    def __repr__(self) -> str:
        return f"Task{self.number}"
    
    def execute(self, start_time, execution_time: float) -> bool:
        self.remaining_time -= execution_time
        if start_time + self.remaining_time > self.next_deadline:
            print(f"task{self.number} failed to execute at {start_time + execution_time}, deadline was {self.next_deadline}")
        if self.remaining_time <= 0:
            self.next_start += self.period
            self.next_deadline += self.period
            self.executed = True
            self.execution_endings.append(start_time + execution_time)
        if (execution_time > 0):
            self.execution_gantt(start_time, execution_time)
    
    def start_task(self) -> None:
        print(f"Wake up task{self.number}, next deadline is {self.next_deadline}")
        self.remaining_time = self.execution_time
        self.executed = False

    def execution_gantt(self, start_time: float, execution: float) -> str:
        self.execution_chart.append([start_time, execution])