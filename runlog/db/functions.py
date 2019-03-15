"""
--- Make excel tab for data that doesn't match a panel ---
Creates an empty worksheet and fills in the headers from the list. 
Loops through the query set and excludes any records which have a panel in the input list.
Loops through the remaining records and saves each to a new row.
"""
def tab_other(wb, runs, panels):
    # define headers
    headers = ['Panel', 'Run ID', 'Worksheet', 'Description', 'Setup Date', 'Run Date', 'TAT']
    headers = ['Panel', 'Run ID', 'Worksheet', 'Worksheet Date', 'Setup Date', 'Run Date', 'TAT1', 'TAT2', 'Total TAT', 'Description']
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
            '', # worksheet date
            obj.setup_date,
            obj.instrument_date,
            '', # TAT1
            '', # TAT2
            '', # Total TAT - this is to preserve column ordering, all three of these are overwritten in the next section
            obj.description2
        ]
        for col in range(len(row)):
            # loops through list to add each column
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
            
        # add custom excel formula to workout working days between start and end dates
        # TAT1 - worksheet date - setup date
        c = ws.cell(row=row_no + 1, column=7)
        c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'

        #TAT2 - Setup date to run date
        c = ws.cell(row=row_no + 1, column=8)
        c.value = '=NETWORKDAYS(E' + str(n+2) + ',F' + str(n+2) + ',1)'

        # Total TAT - Worksheet date - run date
        c = ws.cell(row=row_no + 1, column=9)
        c.value = '=NETWORKDAYS(D' + str(n+2) + ',F' + str(n+2) + ',1)'

    return wb


"""
--- Make excel tabs with data split by panel ---
Creates an empty worksheet for each panel in the input and fills in the headers from the list. 
Loops through the query set for each panel and saves each result to a new row.
The output is a seperate tab for each panel.
"""
def tab_panels(wb, runs, panels):
    # define headers
    #headers = ['Panel', 'Run ID', 'Worksheet', 'Setup Date', 'Run Date', 'TAT']
    headers = ['Panel', 'Run ID', 'Worksheet', 'Worksheet Date', 'Setup Date', 'Run Date', 'TAT1', 'TAT2', 'Total TAT']
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
                '',   # Worksheet date - imported but poorly formatted so cant parse - GTs to manually input
                obj.setup_date,
                obj.instrument_date,
            ]
            for col in range(len(row)):
                # loops through list to add each column
                c = ws.cell(row=row_no + 1, column=col + 1)
                c.value = row[col]

            # add custom excel formula to workout working days between start and end dates
            # TAT1 - worksheet date - setup date
            c = ws.cell(row=row_no + 1, column=len(row) + 1)
            c.value = '=NETWORKDAYS(D' + str(n+2) + ',E' + str(n+2) + ',1)'

            #TAT2 - Setup date to run date
            c = ws.cell(row=row_no + 1, column=len(row) + 2)
            c.value = '=NETWORKDAYS(E' + str(n+2) + ',F' + str(n+2) + ',1)'

            # Total TAT - Worksheet date - run date
            c = ws.cell(row=row_no + 1, column=len(row) + 3)
            c.value = '=NETWORKDAYS(D' + str(n+2) + ',F' + str(n+2) + ',1)'

    return wb


"""
--- Make raw data excel tab ---
Creates an empty worksheet and fills in the headers from the list. 
Loops through the query set and saves each result to a new row.
"""
def tab_raw(wb, runs):
    # define headers and make new worksheet
    headers = ['Panel', 'Run ID', 'Worksheet', 'Worksheet Date', 'Setup Date', 'Run Date', 'Description']
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
            '', # worksheet date - enter manually
            obj.setup_date,
            obj.instrument_date,
            obj.description2
        ]
        for col in range(len(row)):
            # loops through list to add each column
            c = ws.cell(row=row_no + 1, column=col + 1)
            c.value = row[col]
    return wb
