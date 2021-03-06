# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

# , W.Psql]
config :w, ecto_repos: [W.Repo]

config :w, W.Psql,
  username: "zay",
  password: "testpass",
  database: "zay",
  hostname: "localhost",
  show_sensitive_data_on_connection_error: true,
  pool_size: 10

# Configures the endpoint
config :w, WWeb.Endpoint,
  http: [port: 54321],
  url: [host: "localhost", port: 54321],
  secret_key_base: "gpUkga2K86D6hqxZXyQAZRIcCrz",
  render_errors: [view: WWeb.ErrorView, accepts: ~w(html json), layout: false],
  pubsub_server: W.PubSub,
  live_view: [signing_salt: "c38gev6t"]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:mfa, :request_id],
  level: :debug

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
