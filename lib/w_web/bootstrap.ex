defmodule Bootstrap do
  def cdnjs, do: "https://cdnjs.cloudflare.com/ajax/libs"

  def dark_cdn, do: "https://bootswatch.com"
  def dark_css, do: "#{dark_cdn()}/4/darkly/bootstrap.min.css"

  def jquery_ver, do: "3.6.0"
  def jquery_cdn, do: "#{cdnjs()}/jquery"
  def jquery_js, do: "#{jquery_cdn()}/#{jquery_ver()}/jquery.min.js"

  def popper_ver, do: "2.9.2"
  def popper_cdn, do: "#{cdnjs()}/popper.js"
  def popper_js, do: "#{popper_cdn()}/#{popper_ver()}/umd/popper.min.js"

  def bootstrap_ver, do: "4.6.0"
  def bootstrap_cdn, do: "#{cdnjs()}/twitter-bootstrap"
  def bootstrap_js, do: "#{bootstrap_cdn()}/#{bootstrap_ver()}/js/bootstrap.min.js"

  def pegjs_ver, do: "0.9.0"
  def pegjs_cdn, do: "#{cdnjs()}/pegjs"
  def pegjs_js, do: "#{pegjs_cdn()}/#{pegjs_ver()}/peg.min.js"

  # def mapbox_ver(), do: "3.3.1"
  # def mapbox_cdn(), do: "#{cdnjs()}/mapbox.js"
  # def mapbox_js, do: "#{mapbox_cdn()}/#{mapbox_ver()}/mapbox.js"
  # def mapbox_css, do: "#{mapbox_cdn()}/#{mapbox_ver()}/mapbox.min.css"

  def mapbox_ver(), do: "2.2.0"
  def mapbox_cdn(), do: "#{cdnjs()}/mapbox-gl"
  def mapbox_js, do: "#{mapbox_cdn()}/#{mapbox_ver()}/mapbox-gl.js"
  def mapbox_css, do: "#{mapbox_cdn()}/#{mapbox_ver()}/mapbox-gl.css"

  def mapbox_lang,
    do:
      "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-language/v0.10.1/mapbox-gl-language.js"

  def mapbox_token,
    do:
      "pk.eyJ1IjoiZHBvbnlhdG92IiwiYSI6ImNrbmQzcnE2NjBrc3oyb283b2NhNm9mbmwifQ.Ead2JLytP-WMlLUJ6Nb_rQ"
end
