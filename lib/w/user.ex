defmodule W.User do
  use Ecto.Schema

  schema "user" do
    field :login, :string, null: false
    field :passwd, :string, null: false
    #   # field :role, references(:role)
    field :email, :string
    field :first_name, :string
    field :second_name, :string
    field :last_name, :string
    #   field :phone, :string
    #   field :telega, :string
    #   field :zoom, :string
    #   field :skype, :string
    #   field :sync, :string, :virtual
  end

  # W.Repo.insert! %W.User{login: "admin", passwd: "passwd" }
end
