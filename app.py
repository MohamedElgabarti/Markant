from flask import Flask, render_template, request, redirect
import requests
import json
import csv
# append doesn't work with pandas version 2 so install pandas using this command
# pip install pandas<=1.5
import pandas as pd
from datetime import date


app = Flask(__name__)


@app.route('/')
def index():
    global employees
    employees = []
    with open("employee_data.csv", "r", newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            employees.append(row)

    return render_template('index.html', tasks=employees)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    employees = pd.read_csv('employee_data.csv', header=None)
    
    row = employees.iloc[id]
    # print(row)
    emp_id = row[1]
    original_name = row[2]
    last_org = row[3]

    if request.method == 'POST':
        # check if any fields have changed
        fields_changed = False

        # user shouldn't be able to change all the fields
        name = request.form['2']
        org = request.form['3']

        # check if name has changed
        if not original_name == name:
            fields_changed = True
            print(employees.loc[employees[2] == original_name][2])
            employees.loc[employees[2] == original_name, 2] = name

        # check if org has changed
        if not last_org == org:
            fields_changed = True

            # get today's date in right format 01.11.2022
            today = date.today().strftime("%d.%m.%Y")
            # get id of last row to add the id+1 to the new row
            last_row_id = int(employees.iloc[-1][0])

            # change the date for the row that was changed to indicate that the user changed org today
            employees.loc[employees[3] == last_org, 5] = today

            # fill info for new row
            new_row = pd.DataFrame({0: last_row_id+1, 1: emp_id,
                                    2: name, 3: org, 4: today, 5: 'now'}, index=[0])

            # append doesn't work with pandas version 2 so install pandas using this command
            # pip install pandas<=1.5
            employees = employees.append(new_row, ignore_index=True)

        if fields_changed:
            # if fields have changed, then create a new dataframe and save it
            try:
                employees.to_csv('employee_data.csv',
                                 index=False, header=False)
            except:
                print('saving failed')

        return redirect('/')
    else:
        return render_template('edit.html', row=row)


if __name__ == "__main__":
    app.run(debug=True)
