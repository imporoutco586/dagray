from datetime import datetime, timedelta
import mysql.connector
from gql import gql
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
import time
# Your MySQL connection parameters
mydb = mysql.connector.connect(
    host="1.116.51.32",
    user="teecertlabs",
    password="Zaq1xsw2()tcl",
    database="teecertlabs"
)

# Create a cursor object
mycursor = mydb.cursor()

# Your GraphQL query
query = gql("""
    query RunsQuery {
        runsOrError {
            __typename
            ... on Runs {
                results {
                    runId
                    jobName
                    status
                    runConfigYaml
                    startTime
                    endTime
                }
            }
        }
    }
""")

# Create a GraphQL client
transport = RequestsHTTPTransport(url="http://127.0.0.1:3000/graphql")
client = Client(transport=transport)


def insert_or_update_data(result):
    """检查 runId 是否存在，如果存在则更新数据，如果不存在则插入新数据"""
    for run in result["runsOrError"]["results"]:
        # Convert the timestamp to a datetime object
        timestamp_seconds = run["startTime"]
        datetime_obj = datetime.fromtimestamp(timestamp_seconds)

        formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        # 检查 endTime 是否存在
        if run["endTime"] is not None:
            timestamp_seconds1 = run["endTime"]
            datetime_obj1 = datetime.fromtimestamp(timestamp_seconds1)
            formatted_datetime1 = datetime_obj1.strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_datetime1 = None  # 将 endTime 设置为 None

        # 检查 runId 是否存在
        sql = "SELECT 1 FROM fk_zkytestsystem WHERE runId = %s"
        val = (run["runId"],)
        mycursor.execute(sql, val)
        exists = mycursor.fetchone()

        # 如果存在，则更新数据
        if exists:
            sql = """
                UPDATE fk_zkytestsystem 
                SET jobName = %s, status = %s, runConfigYaml = %s, startTime = %s, endTime = %s 
                WHERE runId = %s
            """
            val = (run["jobName"], run["status"], run["runConfigYaml"], formatted_datetime, formatted_datetime1, run["runId"])
            mycursor.execute(sql, val)
        # 否则插入新数据
        else:
            sql = "INSERT INTO fk_zkytestsystem (runId, jobName, status, runConfigYaml, startTime, endTime) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (run["runId"], run["jobName"], run["status"], run["runConfigYaml"], formatted_datetime, formatted_datetime1)
            mycursor.execute(sql, val)

    # Commit the changes
    mydb.commit()


while True:
    # Execute the query
    result = client.execute(query)
    insert_or_update_data(result)
    # Wait for 1 minute
    print(f"Data inserted/updated at {datetime.now()}")
    time.sleep(20)  # Sleep for 60 seconds (1 minute)

# Close the cursor and connection
mycursor.close()
mydb.close()