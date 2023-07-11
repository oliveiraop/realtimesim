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

def plot_grant(values, deadlines):
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 50)
    gnt.set_xlim(0, 160)
    # gnt.set_xlabel("")
    gnt.set_ylabel("Processador")
    # gnt.set_yticks([15, 25, 35])
    labels = []
    for idx in range(len(values)):
        labels.append(f"tarefa {idx + 1}")

    gnt.set_yticklabels(labels)
    gnt.grid(True)

    for idx, value in enumerate(values):
        tuple_list = tuple(i for i in value)
        gnt.broken_barh(
            tuple_list,
            ((idx + 1) * 10, 10),
            facecolors=(f"tab:{colors[idx]}" if idx < len(colors) else "tab:blue"),
            edgecolors="black",
        )

    for idx, value in enumerate(deadlines):
        for idx2, deadline in enumerate(value):
            gnt.vlines(
                deadline,
                (idx + 1) * 10,
                (idx + 1) * 10 + 10,
                colors=colors[idx2],
                linestyles="solid",
            )
    plt.savefig("gantt1.png")


plot_grant(
    [
        [[10, 90]],
        [[100, 10], [160, 10]],
        [[110, 50]],
    ],
    [
        [20, 30, 40, 50, 60, 70, 80, 90, 10],
        [105, 165],
        [120, 130, 140, 150, 160],
    ],
)
