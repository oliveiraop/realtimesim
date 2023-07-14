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


def plot_grant(values, deadlines, periods, test_period=24):
    fig, gnt = plt.subplots()
    gnt.set_ylabel("Processador")
    labels = []
    yticks = []
    for idx in range(len(values)):
        labels.append(f"tarefa {idx + 1}")
        yticks.append((idx + 1) * 5 + 5)

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(labels)
    gnt.grid(True)

    for idx, value in enumerate(values):
        tuple_list = tuple(i for i in value)
        gnt.broken_barh(
            tuple_list,
            ((idx + 1) * 5, 5),
            facecolors=(f"tab:{colors[idx%len(colors)]}"),
            edgecolors="white",
        )
        gnt.hlines(
            (idx + 1) * 5,
            0,
            test_period,
            colors="black",
            linestyles="solid",
            linewidth=1,
        )

    for idx, value in enumerate(deadlines):
        for idx2, deadline in enumerate(value):
            gnt.vlines(
                deadline,
                (idx + 1) * 5,
                (idx + 1) * 5 + 7,
                colors="black",
                linestyles="solid",
            )

    for idx, deadline in enumerate(periods):
        i = 1
        while deadline * i < test_period:
            gnt.vlines(
                deadline * i,
                (idx + 1) * 5,
                (idx + 1) * 5 + 7,
                color="red",
                linestyle="dashed",
            )
            i += 1
    plt.figure(figsize=(800/96, 800/96), dpi=96)
    plt.savefig("gantt1.png")
    return fig