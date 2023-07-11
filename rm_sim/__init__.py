from common import Task
import bisect


class RMSim:
    def __init__(self, tasks : list[Task]) -> None:
        self.tasks : list[Task] = tasks
        self.waiting_tasks : list[Task] = []
        for task in tasks:
            bisect.insort(self.waiting_tasks, task, key=lambda x: -1 * x.priority)
        self.sleeping_tasks : list[Task] = []
        self.executing_task : Task = None
        self.idle_time_chart = []
        self.time = 0
        self.sim_end = 0

    def execute_task(self):
        # Inserção da próxima tarefa como executando
        
        self.executing_task = self.waiting_tasks.pop(0)
        # Teste para saber se existem tarefas dormindo
        if (len(self.sleeping_tasks) > 0):
            while self.sleeping_tasks[0].next_start <= self.executing_task.remaining_time:
                if self.sleeping_tasks[0].priority > self.executing_task.priority:
                    print(f'{self.executing_task} executed for {self.sleeping_tasks[0].next_start - self.time} time units')
                    self.executing_task.execute(self.time, self.sleeping_tasks[0].next_start - self.time)
                    self.time += self.sleeping_tasks[0].next_start - self.time
                    self.wake_up_task()
                    bisect.insort(self.waiting_tasks, self.executing_task, key=lambda x: -1 * x.priority)
                    return
                else:
                    self.wake_up_task()
        print(f'{self.executing_task} executed for {self.executing_task.remaining_time} time units')
        executed = self.executing_task.remaining_time
        self.executing_task.execute(self.time, self.executing_task.remaining_time)
        bisect.insort(self.sleeping_tasks, self.executing_task, key=lambda x: -1 * x.priority)
        self.time += executed

    def wake_up_task(self) -> None:
        self.sleeping_tasks[0].start_task()
        bisect.insort(self.waiting_tasks, self.sleeping_tasks.pop(0), key=lambda x: -1 * x.priority)

    def insert_idle_time(self, time, idle_time):
        self.idle_time_chart.append([time, idle_time])


    def simulate(self, time : int) -> None:
        self.sim_end = time
        while self.time <= self.sim_end:
            print(f'Waiting tasks: {self.waiting_tasks}')
            print(f'Sleeping tasks: {self.sleeping_tasks}')
            print(f'Time: {self.time}')
            if len(self.waiting_tasks) == 0 and len(self.sleeping_tasks) > 0:
                self.time = self.sleeping_tasks[0].next_start
                while self.sleeping_tasks[0].next_start == self.time:
                    self.sleeping_tasks[0].start_task()
                    bisect.insort(self.waiting_tasks, self.sleeping_tasks.pop(0), key=lambda x: -1 * x.priority)
            self.execute_task()