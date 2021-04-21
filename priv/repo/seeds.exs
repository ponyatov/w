# Script for populating the database. You can run it as:
#
#     mix run priv/repo/seeds.exs
#
# Inside the script, you can read and write to any of your
# repositories directly:
#
#     W.Repo.insert!(%W.SomeSchema{})
#
# We recommend using the bang functions (`insert!`, `update!`
# and so on) as they will fail if something goes wrong.

alias W.{User, Role}

W.Repo.insert!(%User{login: "admin", passwd: "passwd"})
W.Repo.insert!(%User{login: "user", passwd: "passwd"})
W.Repo.insert!(%User{login: "guest", passwd: "guest"})
W.Repo.insert!(%User{login: "anon", passwd: ""})

W.Repo.insert!(%User{
  login: "dponyatov",
  passwd: "passwd",
  email: "dponyatov@gmail.com",
  first_name: "Dmitry",
  second_name: "A",
  last_name: "Ponyatov"
})

W.Repo.insert!(%Role{name: "admin"})
W.Repo.insert!(%Role{name: "user"})
W.Repo.insert!(%Role{name: "guest"})
W.Repo.insert!(%Role{name: "anon"})
