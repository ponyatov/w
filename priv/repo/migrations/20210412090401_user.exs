defmodule W.Repo.Migrations.User do
  use Ecto.Migration

  # https://devhints.io/phoenix-migrations

  def change do
    create table(:user) do
      add :login, :string, null: false
      add :passwd, :string, null: false
      add :role, references(:role)
      add :email, :string
      add :first_name, :string
      add :second_name, :string
      add :last_name, :string
      add :phone, :string
      add :telega, :string
      add :zoom, :string
      add :skype, :string
    end

    create unique_index(:user, [:login])

    # create table(:role) do
    #   add :name, :string, null: false
    # end

    # create unique_index(:role, [:name])

    create table(:grp) do
      add :name, :string, null: false
    end

    create unique_index(:grp, [:name])

    # many to many
    create table(:ingroup) do
      add :user, references(:user)
      add :grp, references(:grp)
      add :start, :utc_datetime
      add :stop, :utc_datetime
    end
  end
end
