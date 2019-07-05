import requests
headers = {"Authorization": "Bearer YOUR API KEY"}
def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.cilabs.com/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



query = """
{
  conference(id: "ws18") {
    id
    schedule {
      days {
        timeslots {
          nodes{
            participants{
              nodes{
                attendee{
                  lastName
                  firstName
                  

                }
              }
              
            }
          }
        }
      }
    }
  }
}
"""

query_2 = """
{
  conference(id: "ws18") {
    id
    schedule {
      days {
        
        timeslots {
          
          nodes{
            id
            title
            description
            startsAt
            endsAt
            location {
              id
            }
            
            participants{
              nodes{
                attendee{
                  lastName
                  firstName
                }
              }
              
            }
          }
        }
      }
    }
  }
}



"""

working_query  = """
{
  conference(id: "rise19") {
    id
    schedule {
      days {
        
        timeslots {
          
          nodes{
            id
            title
            description
            startsAt
            endsAt
            location {
              id
            }
            
            participants{
              nodes{
                attendee{
                  lastName
                  firstName
                }
              }
              
            }
          }
        }
      }
    }
  }
}


"""


result = run_query(query) # Execute the query