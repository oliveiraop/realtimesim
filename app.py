from rm_sim import RMSim
from common import Task


if __name__ == '__main__':
    tasks : list[Task] = []
    tasks.append(Task(1, 20, 10, 3))
    tasks.append(Task(2, 15, 5, 4))
    tasks.append(Task(3, 5, 2, 5))
    sim = RMSim(tasks)  
    sim.simulate(50)

    for task in tasks:
        print(task.execution_chart)