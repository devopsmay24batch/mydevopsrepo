from flask import Flask, session, redirect, url_for, request, render_template, flash
import json
import sqlite3
app = Flask(__name__)
db_file = "/tmp/manual_test.db"
table = "test"
app.secret_key = b']\xe7(\x17\xbd\xa3\xba\x007\x1e`\xcdfrq\x1b'

@app.route('/create_step/', methods=["POST"])
def save_info():
    item = {
            "stepID"     : "",
            "options"    : "",
            "selected"   : "",
            "status"     : "",
            "description": "",
            "image"      : ""
            }


    item.update(request.form)
    sql = "INSERT INTO {}".format(table)
    sql += ' VALUES ("{stepID}", "{options}", "{selected}", "{status}",'.format(**item)
    sql += ' "{description}", "{image}")'.format(**item)
    drop_table(table)
    create_table(table)
    insert_item(sql)
    rows = query_item()
    print(rows)

    return "save success\n"


@app.route('/confirm/<stepid>/', methods=["GET", "POST"])
def confirm_selection(stepid):
    if request.method == "GET":
        sql = "SELECT * FROM {} WHERE stepID='{}'".format(table, stepid)
        rows = query_item(sql)
        if rows:
            options = rows[0][1].split(",")
            description = rows[0][4]
            step_dict = { "options":options, "description":description, "stepid":stepid }
            return render_template("confirm.html", **step_dict)
        else:
            return render_template("404.html")
    else:
        option = request.form.get("selected", "")
        sql = "UPDATE {} SET selected='{}' WHERE stepID='{}'".format(table, option, stepid)
        execute_sql(sql)
        return render_template("selected.html", option=option)


@app.route('/query/<stepid>/', methods=["GET"])
def query_data(stepid):
    sql = "SELECT * FROM {}".format(table)
    if stepid != "0":
        sql = "SELECT selected FROM {} WHERE stepID='{}'".format(table, stepid)
    rows = query_item(sql)
    if rows:
        return json.dumps(rows[0])
    else:
        return ""


@app.route('/', methods=['GET', 'POST'])
@app.route('/PassFailDialog', methods=['GET', 'POST'])
def PassFailDialog():
    error = None
    if request.method == 'POST':
        if request.form['result'] == 'PASS' or request.form['result'] == 'FAIL':
            flash("Your response is \"" + str(request.form['result']) + "\"")
            return redirect(url_for('thanks'))
        else:
            error = 'Invalid response'

    return render_template('PassFailDialog.j2',
        error=error,
        message="How is your observed LED color?")


@app.route('/Thanks')
def thanks():
    return render_template('Thanks.j2')


def execute_sql(sql=None):
    if not sql:
        print("SQL scentence is null")
        return
    print("Execute SQL: {}".format(sql))
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    result = cur.execute(sql)
    if "select" in sql.lower():
        result = [row for row in result]
    conn.commit()
    conn.close()

    return result


def create_table(tableName):
    '''
     stepID : ID for test step,
     options : choices for selecting
     selected: the selected option
     status: status for this item, can be created, selected, finished
     description: the description for the test step
     image: image path if there is one
    '''
    create_table_sql = '''CREATE TABLE {} (stepID text, options text,
                          selected text, status text, description text,
                          image text)'''.format(tableName)
    execute_sql(create_table_sql)


def drop_table(tablename):
    sql = "DROP TABLE {}".format(tablename)
    execute_sql(sql)


def insert_item(insert_sql):
    execute_sql(insert_sql)

def query_item(sql=None):
    query_sql = "SELECT * FROM {}".format(table)
    if sql:
        query_sql = sql
    rows = execute_sql(query_sql)

    return rows
