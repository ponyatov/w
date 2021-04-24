defmodule ExpostTest do
  use ExUnit.Case
  doctest Vaop

  test "hello" do
    assert Vaop.hello() == :world
  end
end
