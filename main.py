import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gantt


def create_layout(tasks_length):
    setup_colum = [
        [
            sg.Button("Adicionar tarefa", key="-ADD-", size=(10, 2)),
            sg.Button(
                "RM",
                key="-RM-",
                size=(10, 2),
            ),
            sg.Button("EDF", key="-EDF-", size=(10, 2)),
        ],
        [
            sg.Text("Tarefa", size=(10, 1)),
            sg.Text("Período", size=(10, 1)),
            sg.Text("Duração", size=(10, 1)),
            sg.Text("Prioridade", size=(10, 1)),
        ],
        create_row(0),
    ]

    graph_column = [
        [sg.Text("Gráfico:")],
        [sg.Canvas(key="-CANVAS-")],
    ]

    layout = [
        [
            sg.Column(setup_colum, key="-COL1-", vertical_alignment="top"),
            sg.VSeperator(),
            sg.Column(graph_column, vertical_alignment="top", size=(800, 600)),
        ]
    ]
    return layout


def create_row(row_counter):
    row = [
        sg.pin(
            sg.Column(
                [
                    [
                        sg.Text(
                            f"Tarefa {row_counter + 1}",
                            key=f"-TASK_{row_counter}-",
                        ),
                        sg.Input(
                            "",
                            enable_events=True,
                            key=(f"-INPUT_0_TASK_{row_counter}-", row_counter),
                            expand_x=True,
                            justification="left",
                            size=(10, 1),
                        ),
                        sg.Input(
                            "",
                            enable_events=True,
                            key=(f"-INPUT_1_TASK_{row_counter}-", row_counter),
                            expand_x=True,
                            justification="left",
                            size=(10, 1),
                        ),
                        sg.Input(
                            "",
                            enable_events=True,
                            key=(f"-INPUT_2_TASK_{row_counter}-", row_counter),
                            expand_x=True,
                            justification="left",
                            size=(10, 1),
                        ),
                    ]
                ],
                key=(f"-ROW-", row_counter),
            )
        )
    ]
    return row


def plot_graph(window, values, deadlines):
    fig = gantt.plot_grant(values, deadlines)

    # clear the old plot
    if len(window["-CANVAS-"].TKCanvas.children) > 0:
        child_to_remove = [x for x in window["-CANVAS-"].TKCanvas.children]
        for child in child_to_remove:
            window["-CANVAS-"].TKCanvas.children[child].destroy()

    draw_figure(window["-CANVAS-"].TKCanvas, fig)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def get_task_values(values, row_counter):
    tasks = []
    for i in range(row_counter):
        task = []
        for j in range(3):
            task.append(int(values[(f"-INPUT_{j}_TASK_{i}-", i)]))
        tasks.append(task)
    return tasks


def start():
    layout = create_layout(1)
    window = sg.Window(
        "SIMULADOR DE PROCESSOS", layout, size=(1000, 600), resizable=True
    )

    row_counter = 1
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-ADD-":
            # extend the layout with a new row
            window.extend_layout(window["-COL1-"], [create_row(row_counter)])
            row_counter += 1

        if event == "-RM-":
            print("RM")
            tasks = get_task_values(values, row_counter)
            print(tasks)
            plot_graph(
                window,
                [
                    [[10, 10]],
                    [[5, 5], [20, 5], [35, 5], [50, 5]],
                    [[0, 5], [15, 5], [30, 5], [45, 5]],
                ],
                [],
            )

        if event == "-EDF-":
            print("EDF")
            tasks = get_task_values(values, row_counter)
            print(tasks)


if __name__ == "__main__":
    start()