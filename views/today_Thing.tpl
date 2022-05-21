<!DOCTYPE html>
<html lang=ja>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Three Good Things</title>
  </head>
  <body>
    <p><h3>{{day}}:Good Things</h3></p>
    <form action="/save" method="POST">
      <input type="text" name="thing1"  size="40" maxlength="160" value="{{thing1}}"><br>
      <input type="text" name="thing2"  size="40" maxlength="160" value="{{thing2}}"><br>
      <input type="text" name="thing3"  size="40" maxlength="160" value="{{thing3}}"><br>
      <input type="hidden" name="day" value="{{day}}">
      <input type="submit" name="save" value="save">
    </form>
    </p>
    <a href="/history0">History</a>
  </body>
</html>
