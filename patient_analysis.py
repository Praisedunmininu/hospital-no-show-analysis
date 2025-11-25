# import pandas for data handling
import pandas as pd

# import sqlite3 to work with a sQlite database
import sqlite3

# import matplolib for plotting charts
import matplotlib.pyplot as plt

# load the csv file containing appointment data
df = pd.read_csv("data/appiontments.csv")

# print the first 5 rows of the data to see columns headers and sample values
print(df.head())

# connect  to a SQlite3 database (will create it if it does not exist)
connection = sqlite3.connect("data/appiontment.db")
cursor = connection.cursor()

# save the dataframe to the database to a table named 'appointment'
# if table exists, replace it 
df.to_sql("appiontment",connection,if_exists="replace",index = False)

# select the first 5 rows from the database table 
cursor.execute("SELECT * FROM appiontment LIMIT 5;")
rows = cursor.fetchall()
for r in rows:
    print(r)

# check the structure of the appointment table (columns ,types)
cursor.execute("PRAGMA table_info(appiontment);")
columns = cursor.fetchone()
for r in rows:
    print(r)

# convert ScheduledDay and AppointmentDay columns to a daytime format
df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"])
df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"])

# print the first 5 rows of the date columns 
print(df[["ScheduledDay","AppointmentDay"]].head())

# calculate the waiting in days between shecheduling and appointment
df["WaitingTime"] = (df["AppointmentDay"] - df["ScheduledDay"]).dt.days
print(df[["ScheduledDay","AppointmentDay","WaitingTime"]].head())

# normalize the dates to remove time differences,then calculate waiting days
df["WaitingDays"] = (df["AppointmentDay"].dt.normalize()  - df["ScheduledDay"].dt.normalize()).dt.days
print(df[["ScheduledDay", "AppointmentDay","WaitingDays"]].head())

# check for mising values in each columns 
print(df.isnull().sum())


# count how many patients showed up and did not show up
df["No-show"].value_counts()
print(df["No-show"].value_counts())

# find any negative ages
df[df["Age"]< 0]
print(df[df["Age"]< 0][["Age"]])

# select all valid ages (>=0) for calculation
valid_ages = df[df["Age"]>=0]["Age"]

# calculate median age of valid ages
median_age = valid_ages.median()
print(median_age)

# replace the invalid -1 with the  median age
df.loc[df["Age"]==-1,"Age"]=37

# check the age at a specific row index
print(df["Age"].loc[99832])

# print min, max , median and mean age  
df["Age"].min()
df["Age"].max()
df["Age"].median()
df["Age"].mean()
print(df["Age"].min(),df["Age"].max(),df["Age"].median(),df["Age"].mean())

# plot age distribution of patients 
plt.hist(df["Age"],bins=20 ,color="blue",edgecolor="black")
plt.title("Age distribution of patients")
plt.xlabel("Age")
plt.ylabel("Number of patients")
plt.show()

# count number of patients aged 115
df[df["Age"]==115].shape[0]
print(df[df["Age"]==115].shape[0])

# show unique values in the No-show column
print(df["No-show"].unique())

# convert N0_show column to numeric: "No":0,"yes":1
df["NoShowBinary"]=df["No-show"].map({"No":0, "Yes":1})
print(df[["No-show","NoShowBinary"]].head())

# calculate average No-show rate by age 
age_no_show_rate = df.groupby("Age")["NoShowBinary"].mean()
print(age_no_show_rate.head(10))

# calculate overall No-show percentage
overall_no_show_rate = df["NoShowBinary"].mean()
overall_no_show_percentage = overall_no_show_rate*100
print(overall_no_show_percentage)

# compare No-show rate between patient who recived SMS and those who did not
SMS_NoShow = df.groupby("SMS_received")["NoShowBinary"].mean()
print(SMS_NoShow)

# create a table to see counts of patients by SMS recieved and N0- show status
pd.crosstab(df["SMS_received"],df["NoShowBinary"])
print(pd.crosstab(df["SMS_received"],df["NoShowBinary"]))

# crosstab of age , SMS received,and no show
print(  pd.crosstab(df["Age"],
            [df["SMS_received"], df["NoShowBinary"]])  )

# calculate No-show rate by age and SMS received 
No_show_rate_by_age =df.groupby(["Age", "SMS_received"])["NoShowBinary"].mean()
print(No_show_rate_by_age)

# group data by age and SMS received, calculate mean no_show
group_age_sms = df.groupby(["Age","SMS_received"] )["NoShowBinary"].mean()
print(group_age_sms)

# pivot the grouped data to separate columns for SMS received vrs no SMS
pivot_table = group_age_sms.unstack()
ages = pivot_table.index
no_sms = pivot_table[0]
with_sms = pivot_table[1]

# plot no-show rate by age for patients with and without SMS
plt.plot(ages,no_sms, label="no_sms")
plt.plot(ages,with_sms,label="SMS_received")
plt.title ("No Show Rate By Age and SMS Reminder")
plt.xlabel ("Age")
plt.ylabel ("No show rate(%)")
plt.legend()
plt.show()








               













