import pandas
import plotly.express as px


def final_scalability():
    df = pandas.read_csv('measurements/test_100_hosts_10_threads.csv')
    df["module_count"] = df["module_count"].astype(str)
    fig = px.line(df, x="host_count", y="time", line_shape="spline")

    fig.update_layout(
        title={"text": "Infrastrukturtest mit 5 Modulen nach der Parallelisierung und Persistierung der SSH-Verbindung",
               "xanchor": "left", "x": 0.1},
        xaxis_title="Anzahl der Hostsysteme",
        yaxis_title="Ausführungszeit in Sekunden",
    )
    fig.update_xaxes(
        nticks=20)
    fig.update_yaxes(nticks=25)
    return fig


def module_comparison():
    fig = px.box(pandas.read_csv('measurements/module.csv'),
                 x=["service_module", "address_module", "os_module", "compare_module"],
                 points="all"
                 )
    fig.update_layout(
        title={"text": "Ausführungszeit der verschiedenen Testinfra-Module",
               "xanchor": "left", "x": 0.1},
        yaxis_title="Module",
        xaxis_title="Ausführungszeit in Sekunden",
    )
    fig.update_xaxes(
        nticks=20)
    return fig


def initial_performance_problem():
    df = pandas.read_csv('measurements/test_100.csv')
    df["module_count"] = df["module_count"].astype(str)
    df["Anzahl Module"] = df["module_count"]

    fig = px.scatter(df, x="host_count", y="time", color="Anzahl Module", trendline="ols", range_y=[0, 140],
                     range_x=[0.98, 10.2])
    fig.update_layout(
        title={"text": "Ausführungszeit bei variierender Host- und Modul-Anzahl",
               "xanchor": "left", "x": 0.1},
        xaxis_title="Anzahl der Hostsysteme",
        yaxis_title="Ausführungszeit in Sekunden",
    )
    fig.update_xaxes(nticks=10)
    fig.update_yaxes(nticks=14)
    return fig


def optimization_comparison():
    data = pandas.read_csv('measurements/5_module_tests.csv')

    fig = px.scatter(data, x="host_count", y="time", color="Optimierung", trendline="ols", opacity=0.9, log_x=False,
                     log_y=False,
                     range_y=[1, 220],
                     color_discrete_sequence=px.colors.qualitative.Safe,
                     range_x=[1, 30])

    fig.update_layout(
        title={"text": "Vergleich der Optimierungsansätze auf die Ausführungszeit",
               "xanchor": "left", "x": 0.1},
        xaxis_title="Anzahl der Hostsysteme",
        yaxis_title="Ausführungszeit in Sekunden",
    )
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    fig.update_yaxes(nticks=30)
    fig.update_xaxes(nticks=30)

    return fig


if __name__ == '__main__':
    functions = [
        module_comparison,
        initial_performance_problem,
        optimization_comparison,
        final_scalability
    ]
    for func in functions:
        dia = func()
        dia.update_layout(
            font=dict(
                family="Georgia",
                size=20,
                color="black"
            )
        )
        dia.write_image(F"statistic_{func.__name__}.pdf", width=1200, height=600)
