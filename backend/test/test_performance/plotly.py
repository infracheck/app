import pandas
import plotly.express as px


def show_scatter():
    df = pandas.read_csv('test_100_10_threads.csv')
    df["module_count"] = df["module_count"].astype(str)
    fig = px.scatter(df, x="host_count", y="time", log_y=False, log_x=False,
                     color="module_count", trendline="ols")

    fig.update_layout(
        xaxis_title="Host system count",
        yaxis_title="Execution time in seconds",

        font=dict(
            family="Georgia",
            size=20,
            color="black"
        )
    )
    fig.update_traces(marker=dict(size=15, opacity=0.8),
                      selector=dict(mode='markers')
                      )
    fig.update_xaxes(
        nticks=20)
    fig.show()
    # fig.write_image("execution2.pdf", width=1200, height=600)


def show_line():
    df = pandas.read_csv('test_100_hosts_10_threads.csv')
    df["module_count"] = df["module_count"].astype(str)
    fig = px.line(df, x="host_count", y="time", log_y=False, log_x=False,
                  color="module_count")
    fig.show()


if __name__ == '__main__':
    show_line()
