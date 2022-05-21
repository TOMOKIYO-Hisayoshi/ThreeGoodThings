<!DOCTYPE html>
<html lang=ja>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Good Things History</title>
  </head>
  <body>
    <p><h3>Good Things History</h3></p>
    </p>
    %if prev >= 0:
      <a href="/history{{prev}}">&lt;&lt;</a>
    %end
    <a href="/">index</a>
    %if next >= 0:
      <a href="/history{{next}}">&gt;&gt; </a>
    %end
    </p>
    <table border="1">
    %for row in rows:
      <tr>
        <td>{{row.date}}</td>
        <td>{{row.seq}}</td>
        <td>{{row.thing}}</td>
      </tr>
    %end
    </table>
  </body>
</html>
