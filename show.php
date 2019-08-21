<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

</head>
<body>
<h1>記事一覧</h1>
<?php
try {
  $db = "sqlite:production.sqlite3";
  // データベースへの接続
  $pdo = new PDO($db);

  // テーブル内容を出力
  $sql = "select * from entries order by updated desc";
  $stmt = $pdo->query($sql);

  while ($result = $stmt->fetch()) {
    print("<div class=\"card\" style=\"width: 60rem;\">");
    print("<div class=\"card-head\">");
    print($result['updated']);
    print("</div>");
    print("<div class=\"card-body\">");
    print("<h5 class=\"card-title\">" . $result['entry_title'] . "</h5>");
    print("<p class=\"card-text\">" . $result['summary'] . "</p>");
    print("<a href=\"" . $result['entry_url'] . "\" class=\"btn btn-primary\">Read more</a>");
    print("</div>");
    print("</div>");
  }
  print('<br>');

} catch (PDOException $e) {
  print('データベース接続失敗。' . $e->getMessage());
  die();
}

// データベース切断
$pdo = null;
?>
</body>
</html>
