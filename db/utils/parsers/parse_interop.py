from interop import py_interop_run_metrics, py_interop_run, py_interop_summary


def parse(run_folder):
    """
    Parses summary statistics out of interops data using the Illumina interops package
    """

    # make empty dict to store output
    interop_dict = {}

    # taken from illumina interops package documentation, all of this is required, 
    # even though only the summary variable is used further on
    run_metrics = py_interop_run_metrics.run_metrics()
    valid_to_load = py_interop_run.uchar_vector(py_interop_run.MetricCount, 0)
    py_interop_run_metrics.list_summary_metrics_to_load(valid_to_load)
    run_folder = run_metrics.read(run_folder, valid_to_load)
    summary = py_interop_summary.run_summary()
    py_interop_summary.summarize_run_metrics(run_metrics, summary)

    # parse data from interop files -- % reads over Q30, cluster density, clusters passing filter
    interop_dict["percent_q30"] = round(summary.total_summary().percent_gt_q30(), 2)
    interop_dict["cluster_density"] = round(summary.at(0).at(0).density().mean() / 1000, 2)
    interop_dict["percent_pf"] = round(summary.at(0).at(0).percent_pf().mean(), 2)
    interop_dict["phasing"] = round(summary.at(0).at(0).phasing().mean(), 2)
    interop_dict["prephasing"] = round(summary.at(0).at(0).prephasing().mean(), 2)
    interop_dict["error_rate"] = round(summary.total_summary().error_rate(), 2)
    interop_dict["aligned"] = round(summary.total_summary().percent_aligned(), 2)

    return interop_dict