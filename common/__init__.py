

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

    def __repr__(self) -> str:
        return f"Task{self.number}"
    
    def execute(self, start_time, execution_time: int) -> bool:
        self.remaining_time -= execution_time
        if self.remaining_time == 0:
            self.executed = True
        self.execution_gantt(start_time, execution_time)
    
    def start_task(self) -> None:
        self.next_start += self.period
        self.next_deadline += self.period
        self.remaining_time = self.execution_time
        self.executed = False

    def execution_gantt(self, start_time: int, execution: int) -> str:
        self.execution_chart.append([start_time, execution])