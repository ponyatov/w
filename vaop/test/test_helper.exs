# https://virviil.github.io/2016/10/26/elixir-testing-without-starting-supervision-tree/

Application.load(:vaop)

for app <- Application.spec(:vaop, :applications) do
  case app do
    :exsync ->
      :skip

    app ->
      IO.inspect(app)
      Application.ensure_all_started(app)
  end
end

ExUnit.start()
