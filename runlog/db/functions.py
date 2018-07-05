def tab_raw(wb, runs):
    headers = ['Panel', 'Run ID', 'Worksheet', 'Setup Date', 'Run Date']
    ws = wb.get_active_sheet()
    ws.title = 'raw'
    
    row_no = 0
    for col in range(len(headers)):
        c = ws.cell(row=row_no + 1, column=col + 1)
        c.value = headers[col]
    for obj in runs:
        row_no += 1
        row = [
            obj.pipeline,
            obj.run_id,
            obj.experiment,
            obj.setup_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
    return wb


def tab_panels(wb, runs, panels):
    headers = ['Panel', 'Run ID', 'Worksheet', 'Setup Date', 'Run Date', 'TAT']
    for panel in panels:
        qs = runs.filter(pipeline__contains=panel)
        ws = wb.create_sheet(title=panel)
        
        row_no = 0
        for col in range(len(headers)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = headers[col]
        for n, obj in enumerate(qs):
            row_no += 1
            row = [
                obj.pipeline,
                obj.run_id,
                obj.experiment,                        
                obj.setup_date,
                obj.instrument_date,
            ]
            for col in range(len(row)):
                c = ws.cell(row=row_no + 1, column=col + 1)
                c.value = row[col]
            c = ws.cell(row=row_no + 1, column=len(row) + 1)
            c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'
    return wb


def tab_other(wb, runs, panels):
    headers = ['Panel', 'Run ID', 'Worksheet', 'Description', 'Setup Date', 'Run Date', 'TAT']
    qs = runs
    for panel in panels:
        qs = qs.exclude(pipeline__contains=panel)
    ws = wb.create_sheet(title='other')
    
    row_no = 0
    for col in range(len(headers)):
        c = ws.cell(row=row_no + 1, column=col + 1)
        c.value = headers[col]
    for n, obj in enumerate(qs):
        row_no += 1
        row = [
            obj.pipeline,
            obj.run_id,
            obj.experiment,
            obj.description2,
            obj.setup_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
        c = ws.cell(row=row_no + 1, column=len(row) + 1)
        c.value = '=NETWORKDAYS(E' + str(n+2) + ',F' + str(n+2) + ',1)'
    return wb