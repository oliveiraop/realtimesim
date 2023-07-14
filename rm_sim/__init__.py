from common import Task
import bisect
from typing import List, Union


class RMSim:
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks: list[Task] = tasks
        self.waiting_tasks: list[Task] = []
        self.insort_method = lambda x: -1 * x.priority
        self.sleep_insort_method = lambda x: x.next_start
        for task in tasks:
            bisect.insort(self.waiting_tasks, task, key=self.insort_method)
        self.sleeping_tasks: list[Task] = []
        self.executing_task: Task = None
        self.idle_time_chart = []
        self.time = 0
        self.sim_end = 0
        

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


    # verifica se alguma task deve ser acordada
    def check_interruption(self) -> bool:
        interrupted = False
        if self.sleeping_tasks[0].next_start < (self.time + self.executing_task.remaining_time):
            interrupted = True
        return interrupted
    
    def executing_waiting_insort(self) -> None:
        bisect.insort(
                    self.waiting_tasks, self.executing_task, key=self.insort_method
                )
        
    def sleep_insort(self) -> None:
        bisect.insort(
                    self.sleeping_tasks, self.executing_task, key=self.sleep_insort_method
                )

    def execute_task(self):
        # Inserção da próxima tarefa como executando
        self.executing_task = self.waiting_tasks.pop(0)
        print(f"Task{self.executing_task.number} is executing")

        # Teste para saber se existem tarefas dormindo
        while (len(self.sleeping_tasks) > 0) and (self.check_interruption()):
            if self.check_priority():
                # Execução parcial da tarefa com interrupção
                task_to_interrupt = self.sleeping_tasks[0]
                executed = task_to_interrupt.next_start - self.time
                print(
                    f"{self.executing_task} executed for {executed} time units remaining: {self.executing_task.remaining_time - executed}"
                )
                self.executing_task.execute(self.time, executed)
                self.time += executed
                self.wake_up_task()
                self.executing_waiting_insort()
                return
            else:
                # Acordar tarefas que iniciam antes do fim da tarefa em execução e tem prioridade menor
                self.wake_up_task()

        # Execução da tarefa sem interrupção
        print(
            f"{self.executing_task} executed for {self.executing_task.remaining_time} time units"
        )
        executed = self.executing_task.remaining_time
        self.executing_task.execute(self.time, self.executing_task.remaining_time)
        self.sleep_insort()
        self.time += executed
        self.executing_task = None

    def check_priority(self) -> bool:
        if self.sleeping_tasks[0].priority > self.executing_task.priority:
            return True
        return False

    def wake_up_task(self) -> None:
        self.sleeping_tasks[0].start_task()
        bisect.insort(
            self.waiting_tasks, self.sleeping_tasks.pop(0), key=self.insort_method
        )
        # Evitar que uma tarefa que seja iniciada no mesmo instante não seja acordada
        while (len(self.sleeping_tasks) > 0) and (
            self.sleeping_tasks[0].next_start <= self.time
        ):
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
            # verifica se não existe tarefas esperando, se não, acorda as que estão dormindo
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
        self.sleep_insort_method = lambda x: x.next_start
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

    def executing_waiting_insort(self) -> None:
        bisect.insort(
                    self.waiting_tasks, self.executing_task, key=self.insort_method
                )
        
    def sleep_insort(self) -> None:
        bisect.insort(
                    self.sleeping_tasks, self.executing_task, key=self.sleep_insort_method
                )

    def execute_task(self):
        # Inserção da próxima tarefa como executando
        self.executing_task = self.waiting_tasks.pop(0)
        print(f"Task{self.executing_task.number} is executing")

        # Teste para saber se existem tarefas dormindo
        while (len(self.sleeping_tasks) > 0) and (self.check_interruption()):
            if self.check_priority():
                # Execução parcial da tarefa com interrupção
                task_to_interrupt = self.sleeping_tasks[0]
                executed = task_to_interrupt.next_start - self.time
                print(
                    f"{self.executing_task} executed for {executed} time units remaining: {self.executing_task.remaining_time - executed}"
                )
                self.executing_task.execute(self.time, executed)
                self.time += executed
                self.wake_up_task()
                self.executing_waiting_insort()
                return
            else:
                # Acordar tarefas que iniciam antes do fim da tarefa em execução e tem prioridade menor
                self.wake_up_task()

        # Execução da tarefa sem interrupção
        print(
            f"{self.executing_task} executed for {self.executing_task.remaining_time} time units"
        )
        executed = self.executing_task.remaining_time
        self.executing_task.execute(self.time, self.executing_task.remaining_time)
        self.sleep_insort()
        self.time += executed
        self.executing_task = None

    def check_priority(self) -> bool:
        if self.sleeping_tasks[0].next_deadline < self.executing_task.next_deadline:
            return True
        return False

    def wake_up_task(self) -> None:
        self.sleeping_tasks[0].start_task()
        bisect.insort(
            self.waiting_tasks, self.sleeping_tasks.pop(0), key=self.insort_method
        )
        # Evitar que uma tarefa que seja iniciada no mesmo instante não seja acordada
        while (len(self.sleeping_tasks) > 0) and (
            self.sleeping_tasks[0].next_start <= self.time
        ):
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
