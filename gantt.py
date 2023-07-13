import matplotlib.pyplot as plt

colors = [
    "orange",
    "blue",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
]


def plot_grant(values, deadlines, periods):
    fig, gnt = plt.subplots()
    gnt.set_ylabel("Processador")
    labels = []
    yticks = []
    for idx in range(len(values)):
        labels.append(f"tarefa {idx + 1}")
        yticks.append((idx + 1) * 10 + 5)

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(labels)
    gnt.grid(True)

    for idx, value in enumerate(values):
        tuple_list = tuple(i for i in value)
        gnt.broken_barh(
            tuple_list,
            ((idx + 1) * 10, 10),
            facecolors=(f"tab:{colors[idx%len(colors)]}"),
            edgecolors="black",
        )

    for idx, value in enumerate(deadlines):
        for idx2, deadline in enumerate(value):
            gnt.vlines(
                deadline,
                (idx + 1) * 10,
                (idx + 1) * 10 + 12,
                colors=colors[idx2 % len(colors)],
                linestyles="solid",
            )

    for idx, deadline in enumerate(periods):
        i = 0
        while deadline * i < 50:
            print(deadline * i, (idx + 1) * 10, (idx + 1) * 10 + 12)
            gnt.vlines(
                deadline * i,
                (idx + 1) * 10,
                (idx + 1) * 10 + 12,
                color=colors[idx % len(colors)],
                linestyle="dashed",
            )
            i += 1

    plt.savefig("gantt1.png")
    return fig


def plot_deadlines(periods):
    for idx, deadline in enumerate(periods):
        i = 0
        while deadline * i < 50:
            print(deadline * i, deadline)
            plt.axvline(deadline * i, 0, 50, color="white", linestyle="dashed")
            i += 1


plot_grant(
    [
        [[9, 1], [12, 3], [24, 1], [27, 3], [39, 1], [42, 1]],
        [[2, 3], [7, 2], [17, 3], [22, 2], [32, 3], [37, 2], [47, 3]],
        [
            [0, 2],
            [5, 2],
            [10, 2],
            [15, 2],
            [20, 2],
            [25, 2],
            [30, 2],
            [35, 2],
            [40, 2],
            [45, 2],
            [50, 2],
        ],
    ],
    [],
    [3, 4, 5],
)
