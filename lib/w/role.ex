defmodule W.Role do
  use Ecto.Schema

  schema "role" do
    field :name, :string
    field :skr, :integer
  end

  # %W.Role{}
end
