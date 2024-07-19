from gql import gql
from gql import Client
from gql.transport.requests import RequestsHTTPTransport

# Define your GraphQL query
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

# Execute the query
result = client.execute(query)

# Print the result
print(result)