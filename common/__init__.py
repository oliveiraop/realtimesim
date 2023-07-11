

class Task:
    def __init__(self, period, execution_time, priority=0) -> None:
        self.period = period
        self.next_start = period
        self.next_deadline = period
        self.execution_time = execution_time
        self.remaining_time = execution_time
        self.executed = False
        self.priority = priority
        self.execution_chart = []

    def __repr__(self) -> str:
        return f"Task(period={self.period}, execution_time={self.execution_time}" + (f", priority={self.priority})" if self.priority > 0 else "")
    
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