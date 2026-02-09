package app.authz

default allow = false

# Example rule: allow users with role admin
allow {
  input.user.roles[_] == "admin"
}
