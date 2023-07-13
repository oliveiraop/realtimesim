from rm_sim import RMSim
from common import Task
import gantt
import matplotlib.pyplot as plt


if __name__ == '__main__':
    tasks : list[Task] = []
    tasks.append(Task(1, 20, 10, 3))
    tasks.append(Task(2, 15, 5, 4))
    tasks.append(Task(3, 5, 2, 5))
    sim = RMSim(tasks)
    sim.simulate(50)

    execution_charts = []
    for task in tasks:
        execution_charts.append(task.execution_chart)
        print(task.execution_chart)

    fig = gantt.plot_grant(execution_charts, [])
    plt.savefig("gantt1.png")