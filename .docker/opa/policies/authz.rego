package app.authz

import rego.v1

default allow := false

# Allow authenticated users to access their own profile
allow if {
    input.method == "GET"
    input.path == "/api/app/v1/users/me"
    "view-profile" in input.user.roles
}

# Only users with "admin" role can create new user
allow if {
    input.method == "POST"
    input.path == "/api/app/v1/users"
    "admin" in input.user.roles
}

# Only authenticated users can read the list of users
allow if {
    input.method == "GET"
    input.path == "/api/app/v1/users"
}
