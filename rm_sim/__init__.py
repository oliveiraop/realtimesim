from common import Task
import bisect
from typing import List, Union


class RMSim:
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks: list[Task] = tasks
        self.waiting_tasks: list[Task] = []
        for task in tasks:
            bisect.insort(self.waiting_tasks, task, key=lambda x: -1 * x.priority)
        self.sleeping_tasks: list[Task] = []
        self.executing_task: Task = None
        self.idle_time_chart = []
        self.time = 0
        self.sim_end = 0
        self.insort_method = lambda x: -1 * x.priority
        self.sleep_insort_method = lambda x: x.next_start

    def is_schedulable(self) -> bool:
        U = 0
        for task in self.tasks:
            U += task.execution_time / task.period
        Ulub = len(self.tasks) * (2 ** (1 / len(self.tasks)) - 1)
        print(Ulub, U)
        if U > 1:
            return False
        if U <= Ulub:
            return True
        return None

    def get_task_to_interrupt(self) -> Task:
        for task in self.sleeping_tasks:
            if task.next_start < (self.time + self.executing_task.remaining_time):
                return task
        return None

    def get_first_task_to_wake_up(self) -> Union[Task, int]:
        for idx, task in enumerate(self.sleeping_tasks):
            if task.next_start == self.time:
                return task, idx
        return [None, None]

    # verifica se alguma task deve ser acordada
    def check_interruption(self) -> bool:
        interrupted = False
        for task in self.sleeping_tasks:
            if task.next_start < (self.time + self.executing_task.remaining_time):
                interrupted = True
                break
        return interrupted

    def execute_task(self):
        # Inserção da próxima tarefa como executando
        self.executing_task = self.waiting_tasks.pop(0)
        print(f"Task{self.executing_task.number} is executing")

        # Teste para saber se existem tarefas dormindo
        while (len(self.sleeping_tasks) > 0) and (self.check_interruption()):
            if self.check_priority():
                task_to_interrupt = self.get_task_to_interrupt()
                executed = task_to_interrupt.next_start - self.time
                print(
                    f"{self.executing_task} executed for {executed} time units remaining: {self.executing_task.remaining_time - executed}"
                )
                self.executing_task.execute(self.time, executed)
                self.time += executed
                if self.executing_task.executed:
                    self.sleeping_tasks.append(self.executing_task)
                    self.executing_task = None
                    self.wake_up_task()
                    return
                self.wake_up_task()
                bisect.insort(
                    self.waiting_tasks, self.executing_task, key=self.sleep_insort_method
                )
                return
            else:
                self.wake_up_task()

        # Execução da tarefa sem interrupção
        print(
            f"{self.executing_task} executed for {self.executing_task.remaining_time} time units"
        )
        executed = self.executing_task.remaining_time
        self.executing_task.execute(self.time, self.executing_task.remaining_time)
        bisect.insort(self.sleeping_tasks, self.executing_task, key=self.sleep_insort_method)
        self.time += executed
        self.executing_task = None

    def check_priority(self) -> bool:
        for task in self.sleeping_tasks:
            if task.next_start < (self.time + self.executing_task.remaining_time):
                if task.priority > self.executing_task.priority:
                    return True
        return False

    def wake_up_task(self) -> None:
        task_to_wake_up, idx = self.get_first_task_to_wake_up()
        if task_to_wake_up is not None:
            task_to_wake_up.start_task()
            bisect.insort(
                self.waiting_tasks, self.sleeping_tasks.pop(idx), key=self.insort_method
            )
            return
        self.sleeping_tasks[0].start_task()
        bisect.insort(
            self.waiting_tasks, self.sleeping_tasks.pop(0), key=self.insort_method
        )

    def insert_idle_time(self, time, idle_time):
        self.idle_time_chart.append([time, idle_time])

    def simulate(self, time: float) -> None:
        self.sim_end = time
        while self.time < self.sim_end:
            print(f"Waiting tasks: {self.waiting_tasks}")
            print(f"Sleeping tasks: {self.sleeping_tasks}")
            print(f"Time: {self.time}")
            if len(self.waiting_tasks) == 0 and len(self.sleeping_tasks) > 0:
                self.time = self.sleeping_tasks[0].next_start
                while (len(self.sleeping_tasks) > 0) and self.sleeping_tasks[
                    0
                ].next_start == self.time:
                    self.sleeping_tasks[0].start_task()
                    bisect.insort(
                        self.waiting_tasks,
                        self.sleeping_tasks.pop(0),
                        key=self.insort_method,
                    )
            self.execute_task()


class EDFSim:
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks: list[Task] = tasks
        self.waiting_tasks: list[Task] = []
        self.insort_method = lambda x: x.next_deadline
        for task in tasks:
            bisect.insort(self.waiting_tasks, task, key=self.insort_method)
        self.sleeping_tasks: list[Task] = []
        self.executing_task: Task = None
        self.idle_time_chart = []
        self.time = 0
        self.sim_end = 0

    def is_schedulable(self) -> bool:
        return (
            True
            if sum([task.execution_time / task.period for task in self.tasks]) <= 1
            else False
        )

    def execute_task(self):
        # Inserção da próxima tarefa como executando

        self.executing_task = self.waiting_tasks.pop(0)
        # Teste para saber se existem tarefas dormindo
        while (len(self.sleeping_tasks) > 0) and (
            (self.sleeping_tasks[0].next_start)
            < (self.time + self.executing_task.remaining_time)
        ):
            if self.check_priority():
                executed = self.sleeping_tasks[0].next_start - self.time
                print(
                    f"{self.executing_task} executed for {executed} time units remaining: {self.executing_task.remaining_time - executed} with deadline {self.executing_task.next_deadline}"
                )
                self.executing_task.execute(
                    self.time, self.sleeping_tasks[0].next_start - self.time
                )
                self.time += self.sleeping_tasks[0].next_start - self.time
                self.wake_up_task()
                bisect.insort(
                    self.waiting_tasks, self.executing_task, key=self.insort_method
                )
                return
            else:
                self.wake_up_task()
        print(
            f"{self.executing_task} executed for {self.executing_task.remaining_time} time units"
        )
        executed = self.executing_task.remaining_time
        self.executing_task.execute(self.time, self.executing_task.remaining_time)
        bisect.insort(self.sleeping_tasks, self.executing_task, key=self.insort_method)
        self.time += executed
        self.executing_task = None

    def check_priority(self) -> bool:
        if self.sleeping_tasks[0].next_deadline < self.executing_task.next_deadline:
            print(
                f"{self.sleeping_tasks[0]} has deadline {self.sleeping_tasks[0].next_deadline} and {self.executing_task} has deadline {self.executing_task.next_deadline}"
            )
            return True
        else:
            return False

    def wake_up_task(self) -> None:
        self.sleeping_tasks[0].start_task()
        bisect.insort(
            self.waiting_tasks, self.sleeping_tasks.pop(0), key=self.insort_method
        )

    def insert_idle_time(self, time, idle_time):
        self.idle_time_chart.append([time, idle_time])

    def simulate(self, time: float) -> None:
        self.sim_end = time
        i = 0
        while self.time <= self.sim_end:
            i += 1
            print(f"Iteration {i}")
            print(f"Waiting tasks: {self.waiting_tasks}")
            print(f"Sleeping tasks: {self.sleeping_tasks}")
            print(f"Time: {self.time}")
            if len(self.waiting_tasks) == 0 and len(self.sleeping_tasks) > 0:
                self.time = self.sleeping_tasks[0].next_start
                while (len(self.sleeping_tasks) > 0) and self.sleeping_tasks[
                    0
                ].next_start == self.time:
                    self.sleeping_tasks[0].start_task()
                    bisect.insort(
                        self.waiting_tasks,
                        self.sleeping_tasks.pop(0),
                        key=self.insort_method,
                    )
            self.execute_task()
