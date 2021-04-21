defmodule W.Weather do
  use Ecto.Repo,
    otp_app: :w,
    adapter: Ecto.Adapters.Postgres
end
