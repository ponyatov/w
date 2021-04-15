# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

config :w,
  ecto_repos: [W.Repo]

# Configures the endpoint
config :w, WWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "gpUkga2K86D6hqxZXfbMEU8mdQ+l052LBi6AIFoJZ8p7fYtKPgQpk8yQAZRIcCrz",
  render_errors: [view: WWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: W.PubSub,
  live_view: [signing_salt: "c38gev6t"]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
