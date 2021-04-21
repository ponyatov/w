use Mix.Config

# Configure your database
#
# The MIX_TEST_PARTITION environment variable can be used
# to provide built-in test partitioning in CI environment.
# Run `mix help test` for more information.
config :w, W.Repo, database: "tmp/test.db"

# username: "postgres",
# password: "postgres",
# database: "w_test#{System.get_env("MIX_TEST_PARTITION")}",
# hostname: "localhost",
# pool: Ecto.Adapters.SQL.Sandbox

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :w, WWeb.Endpoint,
  # http: [port: 54321],
  url: [host: "your.server.here", port: 54321],
  debug_errors: true,
  code_reloader: true,
  check_origin: false,
  watchers: [
    node: [
      "node_modules/webpack/bin/webpack.js",
      "--mode",
      "development",
      "--watch-stdin",
      cd: Path.expand("../assets", __DIR__)
    ]
  ]

# server: false

# Print only warnings and errors during test
# config :logger, level: :debug
