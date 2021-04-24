defmodule Vaop.MixProject do
  use Mix.Project

  def project do
    [
      app: :vaop,
      version: "0.0.1",
      elixir: "~> 1.11",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      aliases: aliases()
    ]
  end

  def application do
    [
      mod: {Vaop.Application, []},
      applications: [:logger],
      extra_applications: [:exsync]
    ]
  end

  defp deps do
    [
      {:exsync, "~> 0.2", only: :dev}
    ]
  end

  defp aliases do
    [
      test: "test --no-start"
    ]
  end
end
