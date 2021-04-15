defmodule W.Repo do
  use Ecto.Repo,
    otp_app: :w,
    adapter: Ecto.Adapters.Postgres
end
