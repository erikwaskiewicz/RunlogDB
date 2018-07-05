def tab_raw(wb, runs, headers):
    ws = wb.get_active_sheet()
    ws.title = 'raw'
    
    row_no = 0
    for col in range(len(headers)-1):
        c = ws.cell(row=row_no + 1, column=col + 1)
        c.value = headers[col]
    for obj in runs:
        row_no += 1
        row = [
            obj.pipeline,
            obj.run_id,
            obj.experiment,
            obj.samplesheet_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
    return wb


def tab_panels(wb, runs, headers, panels):
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
                obj.samplesheet_date,
                obj.instrument_date,
            ]
            for col in range(len(row)):
                c = ws.cell(row=row_no + 1, column=col + 1)
                c.value = row[col]
            c = ws.cell(row=row_no + 1, column=len(row) + 1)
            c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'
    return wb


def tab_other(wb, runs, headers, panels):
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
            obj.samplesheet_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
        c = ws.cell(row=row_no + 1, column=len(row) + 1)
        c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'
    return wb