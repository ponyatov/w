defmodule VAOP do
  @moduledoc """

  пример реализации конечного автомата на языке Elixir

  https://habr.com/ru/post/554014/

  1. состояние конечного автомата кодируется в параметре функции, реализующей КА
  2. цикл КА заменяется на рекурсивный вызов КА (с хвостовой рекурсией)
  3. переключения КА реализуются через сопоставление с образцом (суперфишка Erlang/Elixir)
  4. останов КА выполняется по конечному состоянию, или по ошибке
  """

  @doc " запуск автомата с начальными значениями "
  def demo(init_list \\ [34, 45, 57, 8, 14]) do
    fsm(:start, %{m: init_list, sum: 0, i: 0})
  end

  # в Elixir функции полиморфные: задается группа функций с одним именем
  # срабатывает первая подошедшая по параметрам

  @doc " чисто для демонстрации: переключение в другое состояние "
  def fsm(:start, state) do
    IO.inspect({:start, state})
    fsm(:sum, state)
  end

  @doc " состояние суммирования с пустым m[] переключает на :end "
  def fsm(:sum, state) when state.m == [] do
    IO.inspect({:sum, state})
    fsm(:end, state)
  end

  def fsm(:sum, state) do
    IO.inspect({:sum, state})
    # разбор мапы через pattern matching
    %{i: ii, sum: summ, m: [head | tail]} = state
    # хвостовая рекурсия
    fsm(:sum, %{i: ii + 1, sum: summ + head, m: tail})
  end

  @doc " конечное состояние: возвращает мапу с результатом "
  def fsm(:end, state) do
    IO.inspect({:end, state})
    {:ok, state}
  end

  @doc " последний вариант: непредусмотренный state является ошибкой "
  def fsm(any, something_bad),
    do: IO.inspect({:error, [something_bad, "in", any, "state"]})
end
