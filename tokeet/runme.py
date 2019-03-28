import requests
import json
import datetime
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_connection():
    conn = sqlite3.connect('tokeet.db')
    conn.row_factory = dict_factory
    return conn

def execute_query(sql):
    conn = get_connection()
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    c.close()
    conn.close()



def run_sql(sql):
    conn = get_connection()
    c = conn.cursor()
    r = c.execute(sql)
    rows = r.fetchall()
    c.close()
    conn.close()
    return rows

def create_tables():
    print("%s - Create tables" % (datetime.datetime.now()))
    execute_query("drop table booked")

    sql = "create table booked (date date, available int, price int, is_weekend int, weekday text, min_days, weekly_discount, monthly_discount, maximum_guests)"
    execute_query(sql)

    execute_query("CREATE INDEX booked_date ON booked (date);")
    execute_query("CREATE INDEX booked_weekday ON booked (weekday);")


weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_rental_availability():
    print("%s - get rental availability" % (datetime.datetime.now()))
    url = "https://capi.tokeet.com/v1/rental/19b76dc9-6b12-490c-9b8d-e1d92e8e93cd/availability"

    querystring = {"account":"1516269000.1485"}

    headers = {
        'authorization': "f8c9c6a6-e930-4df3-8d1d-0df50e46739b",
        'cache-control': "no-cache",
        'postman-token': "c932761f-ff63-295a-bc61-e220a281cbcb"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def convert_str_to_dt(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

def create_booking_dates():
    print("%s - Create booking dates" % (datetime.datetime.now()))
    dates = []
    date_from = datetime.datetime.now()
    conn = get_connection()
    cur = conn.cursor()
    for x in range(0,365):
        new_date = date_from + datetime.timedelta(days=x)
        is_weekend = 0
        if new_date.weekday() == 5 or new_date.weekday() == 4 or new_date.weekday() == 6:
            is_weekend=1
        min_days=1
        weekly_discount=0
        monthly_discount=0
        maximum_guests=0
        cur.execute("insert into booked (date, available, price, is_weekend, weekday,  min_days, weekly_discount, monthly_discount, maximum_guests) values ('%s', 1, 100, %s, '%s', %s, %s, %s, %s)" % (new_date.strftime("%Y-%m-%d"), is_weekend, weekdays[new_date.weekday()], min_days, weekly_discount, monthly_discount, maximum_guests))
    conn.commit()
    cur.close()

    js = get_rental_availability()
    cur = conn.cursor()
    for i in js:
        fr = i['from']
        to = i['to']
        title = i['title']
        available = i['available']
        if available == 0:
            #print("%s %s - %s" % (title, fr, to))
            f = convert_str_to_dt(fr)
            t = convert_str_to_dt(to)

            for single_date in daterange(f, t):
                sql = "update booked set available=0 where date='%s' " % (single_date.strftime("%Y-%m-%d"))
                cur.execute(sql)
                #print("%s [%s] (%s...%s)" % (single_date,title,fr,to))
    conn.commit()
    cur.close()
    conn.close()

def lower_price_between_gaps(days_between_gaps, price_between_gaps):
    conn = get_connection()
    cur = conn.cursor()
    rows= run_sql("select * from booked order by date")
    unbooked_days = []
    for row in rows:
        if row['weekday'] == 'Monday' or row['weekday'] == 'Friday':
            if len(unbooked_days) <= days_between_gaps:
                for i in unbooked_days:
                    cur.execute("update booked set price=%s where date='%s' " % (price_between_gaps, i))
            unbooked_days = []

        if row['available'] ==1:
            unbooked_days.append(row['date'])
        else:
            if len(unbooked_days) <= days_between_gaps:
                for i in unbooked_days:
                    cur.execute("update booked set price=%s where date='%s' " % (price_between_gaps, i))
            unbooked_days = []
    conn.commit()
    cur.close()
    conn.close()

def discount_next_days( type, total_days=0, fixed_val=None, fixed_perc=None, gradual_perc=None, perc_list=[]):
    conn = get_connection()
    cur = conn.cursor()
    if type == "custom_perc_dec":
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(len(perc_list)))
        nr = 0
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price = price-price * %s/100 where date='%s'" % (perc_list[nr], date.strftime("%Y-%m-%d")))
            nr=nr+1
    if type == "custom_perc_inc":
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(len(perc_list)))
        nr = 0
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price = price+price * %s/100 where date='%s'" % (perc_list[nr], date.strftime("%Y-%m-%d")))
            nr=nr+1

    if type == "gradual_perc_inc":
        val = gradual_perc
        chng = gradual_perc/total_days
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(total_days))
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price = price-price * %s/100 where date='%s'" % (val, date.strftime("%Y-%m-%d")))
            val = val-chng
    if type == "gradual_perc_dec":
        val = gradual_perc
        chng = gradual_perc/total_days
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(total_days))
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price = price-price * %s/100 where date='%s'" % (val, date.strftime("%Y-%m-%d")))
            val = val+chng
    if type == "fixed_val":
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(total_days))
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price =%s where date='%s'" % (fixed_val, date.strftime("%Y-%m-%d")))
    if type == "fixed_perc_dec":
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(total_days))
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price =price-price*%s/100 where date='%s'" % (fixed_perc, date.strftime("%Y-%m-%d")))
    if type == "fixed_perc_inc":
        start_date = datetime.datetime.now().date()
        end_date = (start_date + datetime.timedelta(total_days))
        for date in daterange(start_date, end_date):
            cur.execute("update booked set price =price+price*%s/100 where date='%s'" % (fixed_perc, date.strftime("%Y-%m-%d")))
    conn.commit()
    cur.close()
    conn.close()

def day_specific_pricing(monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    rows= run_sql("select * from booked order by date")
    conn = get_connection()
    cur = conn.cursor()
    for row in rows:
        val = 0
        if row['weekday'] == 'Monday':
            val = monday
        if row['weekday'] == 'Tuesday':
            val = tuesday
        if row['weekday'] == 'Wednesday':
            val = wednesday
        if row['weekday'] == 'Thursday':
            val = thursday
        if row['weekday'] == 'Friday':
            val = friday
        if row['weekday'] == 'Saturday':
            val = saturday
        if row['weekday'] == 'Sunday':
            val = sunday

        cur.execute("update booked set price =price+price*%s/100 where date='%s'" % (val, row['date']))
    conn.commit()
    cur.close()
    conn.close()

def set_minimum_days_for_far_out_days(far_out_min_days_days, far_out_min_days_later_than_days):
    start_date = datetime.datetime.now().date() + datetime.timedelta(far_out_min_days_later_than_days)
    end_date = (datetime.datetime.now().date() + datetime.timedelta(365))
    conn = get_connection()
    cur = conn.cursor()
    for date in daterange(start_date, end_date):
        cur.execute("update booked set min_days=%s where date='%s'" % (far_out_min_days_days, date.strftime("%Y-%m-%d")))
    conn.commit()
    cur.close()
    conn.close()

def set_min_days(min_days_weekday, min_days_weekend):
    execute_query("update booked set min_days=%s where weekday in ('Monday','Tuesday','Wednesday','Thursday')" % (min_days_weekday))
    execute_query("update booked set min_days=%s where weekday in ('Friday','Saturday')" % (min_days_weekend))


def run_pricing_algorithm():
    print("%s - Run pricing algorithm" % (datetime.datetime.now()))
    weekly_discount = 0
    monthly_discount = 0
    maximum_guests=4
    minimum_days = 2


    #------------------------------------
    orphan_days_enabled = True
    orphan_days_percentage = 75
    orphan_days_gap = 2
    if orphan_days_enabled == True:
        lower_price_between_gaps(orphan_days_gap, orphan_days_percentage)

    #------------------------------------
    min_days_enabled=True
    min_days_weekday=2
    min_days_weekend=2
    if min_days_enabled == True:
        set_min_days(min_days_weekday, min_days_weekend)

    far_out_min_days_enabled = True
    far_out_min_days_days = 3
    far_out_min_days_later_than_days=30
    if far_out_min_days_enabled == True:
        set_minimum_days_for_far_out_days(far_out_min_days_days, far_out_min_days_later_than_days)

    #------------------------------------
    last_minute_discount_enabled = False
    last_minute_discount_type = "gradual_perc_inc" #fixed_val, fixed_perc_dec, fixed_perc_inc, gradual_perc_inc, gradual_perc_dec, custom_perc_dec, custom_perc_inc
    last_minute_fixed_val = 0
    last_minute_fixed_perc=0
    last_minute_gradual_perc=10
    last_minute_days = 3
    last_minute_perc_list=[]

    if last_minute_discount_enabled:
        discount_next_days(total_days=last_minute_days,
                           type=last_minute_discount_type,
                           fixed_val=last_minute_fixed_val,
                           fixed_perc=last_minute_fixed_perc,
                           gradual_perc=last_minute_gradual_perc,
                           perc_list=last_minute_perc_list
                           )

    #------------------------------------
    day_specific_price_enabled=False
    day_specific_increase_mon = 0
    day_specific_increase_tue = 0
    day_specific_increase_wed = 0
    day_specific_increase_thur = 0
    day_specific_increase_fri = 0
    day_specific_increase_sat = 0
    day_specific_increase_sun = 0
    if day_specific_price_enabled == True:
        day_specific_pricing(day_specific_increase_mon,
                             day_specific_increase_tue,
                             day_specific_increase_wed,
                             day_specific_increase_thur,
                             day_specific_increase_fri,
                             day_specific_increase_sat,
                             day_specific_increase_sun)


#------------------------------------
#print("%s - Step 9" % (datetime.datetime.now()))
#rows= run_sql("select * from booked order by date")
# for row in rows:
#    print(row)



from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/", methods=['GET'])
def prices():
    rows = run_sql("select * from booked order by date")
    html = "<a href='/runcalc'>Run calcs</a>"
    html += "<table border='1' cellspacing='0' cellpadding='0'>"
    html += "<thead>"
    html += "<tr><td>Date</td><td>Weekday</td><td>Price</td><td>Min. Stay</td></tr>"
    html += "</thead>"
    html += "<tbody>"
    for row in rows:
        css = ""
        if row['available'] == 0:
            css= "background-color:red;"
        else:
            if row['weekday'] in ['Friday', 'Saturday','Sunday']:
                css = "background-color:lightgray;"
        html += "<tr style='%s'>" % (css)
        html += "<td>%s</td>" % (row['date'])
        html += "<td>%s</td>" % (row['weekday'])
        html += "<td>%s</td>" % (row['price'])
        html += "<td>%s</td>" % (row['min_days'])
        html += "</tr>"
    html += "</tbody>"
    html += "</table>"
    return html

@app.route("/runcalc", methods=['GET'])
def run_calcs():
    create_tables()
    create_booking_dates()
    run_pricing_algorithm()
    return redirect("/")

def get_rental_rates(rental_id):
    print("%s - get rental rates" % (datetime.datetime.now()))
    url = "https://capi.tokeet.com/v1/rate/%s?account=1516269000.1485" % (rental_id)

    headers = {
        'authorization': "f8c9c6a6-e930-4df3-8d1d-0df50e46739b",
        'cache-control': "no-cache",
        'postman-token': "c932761f-ff63-295a-bc61-e220a281cbcb"
        }

    response = requests.request("GET", url, headers=headers, params=None)
    return json.loads(response.text)


import threading


def delete_standard_rate(rental_id, rate_key, account):
    print("%s - get rental rates" % (datetime.datetime.now()))
    url = "https://capi.tokeet.com/v1/rate/%s/%s" %(rental_id, rate_key)
    querystring = {"account": account}

    headers = {
        'authorization': "f8c9c6a6-e930-4df3-8d1d-0df50e46739b",
        'cache-control': "no-cache",
        'postman-token': "1a8b5da9-2cbd-8a72-0f3c-ecd0aa628edc"
    }

    response = requests.request("DELETE", url, headers=headers, params=querystring)
    print(response)

#@app.route("/deletepricelabs")
def delete_pricelab_rates():
    rental_id="1d0bd75c-8660-40b8-9d4c-42d3ebfde9a2" #sunny apartment
    rental_id="19b76dc9-6b12-490c-9b8d-e1d92e8e93cd" #montagu
    rates = get_rental_rates(rental_id)
    for v in rates['data']['other']:
        nm = v['name']
        key = v['key']
        account = v['account']
        if "PriceLabs" in nm:
            print(nm+" = "+key)
            delete_standard_rate(rental_id, key, account)
            # thr = threading.Thread(target=delete_standard_rate, args=[rental_id, key, account], kwargs={})
            #thr.start()  # Will run "foo"


delete_pricelab_rates()
"""
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=800, debug=True)
"""