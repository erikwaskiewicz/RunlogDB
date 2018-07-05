from interop import py_interop_run_metrics, py_interop_run, py_interop_summary


def parse(run_folder, dictionary):
    run_metrics = py_interop_run_metrics.run_metrics()
    valid_to_load = py_interop_run.uchar_vector(py_interop_run.MetricCount, 0)
    py_interop_run_metrics.list_summary_metrics_to_load(valid_to_load)
    run_folder = run_metrics.read(run_folder, valid_to_load)
    summary = py_interop_summary.run_summary()
    py_interop_summary.summarize_run_metrics(run_metrics, summary)
    # Parse data from interop files -- % reads over Q30, cluster density, clusters passing filter
    dictionary["Percent Q30"] = round(summary.total_summary().percent_gt_q30(), 2)
    dictionary["Cluster density"] = round(summary.at(0).at(0).density().mean() / 1000, 2)
    dictionary["Percent PF"] = round(summary.at(0).at(0).percent_pf().mean(), 2)
    dictionary["Phasing"] = round(summary.at(0).at(0).phasing().mean(), 2)
    dictionary["Prephasing"] = round(summary.at(0).at(0).prephasing().mean(), 2)
    dictionary["Error rate"] = round(summary.total_summary().error_rate(), 2)
    dictionary["Aligned"] = round(summary.total_summary().percent_aligned(), 2)
