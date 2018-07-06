"""
--- Make excel tab for data that doesn't match a panel ---
Creates an empty worksheet and fills in the headers from the list. 
Loops through the query set and excludes any records which have a panel in the input list.
Loops through the remaining records and saves each to a new row.
"""
def tab_other(wb, runs, panels):
    # define headers
    headers = ['Panel', 'Run ID', 'Worksheet', 'Description', 'Setup Date', 'Run Date', 'TAT']
    # get queryset and exclude runs where the panels are in the input list
    qs = runs
    for panel in panels:
        qs = qs.exclude(pipeline__contains=panel)
    # get active worksheet and rename - active worksheet will be first tab in excel
    ws = wb.get_active_sheet()
    ws.title = 'other'
    # add headers
    row_no = 0
    for col in range(len(headers)):
        c = ws.cell(row=row_no + 1, column=col + 1)
        c.value = headers[col]
    # add data
    for n, obj in enumerate(qs):
        row_no += 1
        # make list for each row
        row = [
            obj.pipeline,
            obj.run_id,
            obj.experiment,
            obj.description2,
            obj.setup_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            # loops through list to add each column
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
        # add custom excel formula to workout working days between start and end dates
        c = ws.cell(row=row_no + 1, column=len(row) + 1)
        c.value = '=NETWORKDAYS(E' + str(n+2) + ',F' + str(n+2) + ',1)'
    return wb


"""
--- Make excel tabs with data split by panel ---
Creates an empty worksheet for each panel in the input and fills in the headers from the list. 
Loops through the query set for each panel and saves each result to a new row.
The output is a seperate tab for each panel.
"""
def tab_panels(wb, runs, panels):
    # define headers
    headers = ['Panel', 'Run ID', 'Worksheet', 'Setup Date', 'Run Date', 'TAT']
    # loop through each of the input panels and create worksheets and a subset of the orginal queryset
    for panel in panels:
        qs = runs.filter(pipeline__contains=panel)
        ws = wb.create_sheet(title=panel)
        row_no = 0
        # add headers
        for col in range(len(headers)):
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = headers[col]
        # add data
        for n, obj in enumerate(qs):
            row_no += 1
            # make list for each row
            row = [
                obj.pipeline,
                obj.run_id,
                obj.experiment,                        
                obj.setup_date,
                obj.instrument_date,
            ]
            for col in range(len(row)):
                # loops through list to add each column
                c = ws.cell(row=row_no + 1, column=col + 1)
                c.value = row[col]
            # add custom excel formula to workout working days between start and end dates
            c = ws.cell(row=row_no + 1, column=len(row) + 1)
            c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'
    return wb


"""
--- Make raw data excel tab ---
Creates an empty worksheet and fills in the headers from the list. 
Loops through the query set and saves each result to a new row.
"""
def tab_raw(wb, runs):
    # define headers and make new worksheet
    headers = ['Panel', 'Run ID', 'Worksheet', 'Setup Date', 'Run Date']
    ws = wb.create_sheet(title='raw')
    row_no = 0
    # add headers
    for col in range(len(headers)):
        c = ws.cell(row=row_no + 1, column=col + 1)
        c.value = headers[col]
    # add data
    for obj in runs:
        row_no += 1
        # make list for each row
        row = [
            obj.pipeline,
            obj.run_id,
            obj.experiment,
            obj.setup_date,
            obj.instrument_date,
        ]
        for col in range(len(row)):
            # loops through list to add each column
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
    return wb
