<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width">
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
    print($result['updated'] . " ");
    print("<a href='" . $result['entry_url'] . "'>");
    print($result['entry_title'] . "</a>");
    print("<br>");
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
