ALL_USERS = """query {
  allUsers {
    results {
      id
    }
  }
}
"""
ALL_USERS1 = """query {
  allUsers1 {
      id
      username
      firstName
      lastName
      email
  }
}
"""
ALL_USERS2 = """query {
  allUsers2 {
      username
  }
}
"""
ALL_USERS3 = """query {
  allUsers3 {
      id
  }
}
"""
ALL_USERS4 = """query {
  allUsers4 {
    id
    username
  }
}
"""

ALL_USERS5 = """query {
  allUsers5 {
    id
    username
    first_name
    last_name
  }
}"""

ALL_USERS5_WITH_SEARCH = """query {
  allUsers5 (search: %(search)s) {
    results {
      firstName
      lastName
    }
  }
}"""


ALL_USERS3_WITH_FILTER = """query {
  allUsers3 (%(filter)s) {
    results {
      %(fields)s
    }
  }
}
"""

# Queries for DjangoSerializerType
USER = """query {
  user2 (%(filter)s) {
      %(fields)s
  }
}
"""

USERS = """query {
  users(%(filter)s){
    results(%(pagination)s){
        %(fields)s
    },
    totalCount
  }
}
"""
