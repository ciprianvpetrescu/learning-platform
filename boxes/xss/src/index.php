<?php
// VULN: stored XSS. Entries are echoed unescaped.
session_start();
$f = '/var/www/html/entries.json';
$entries = file_exists($f) ? json_decode(file_get_contents($f), true) : [];
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['msg'])) {
  $entries[] = ['name' => $_POST['name'] ?? 'anon', 'msg' => $_POST['msg'], 't' => time()];
  file_put_contents($f, json_encode($entries));
  header('Location: /'); exit;
}
?><!doctype html><html><head><title>Guestbook</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:720px;margin:40px auto;padding:20px}
input,textarea{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:8px;width:100%;margin:6px 0;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:10px 16px;cursor:pointer}
.entry{border-left:3px solid #30363d;padding:8px 14px;margin:10px 0}.name{color:#58a6ff;font-weight:600}</style></head><body>
<h1>Guestbook</h1><p>Leave a message. Our admin reads every entry.</p>
<form method="post"><input name="name" placeholder="Your name"><textarea name="msg" placeholder="Message"></textarea><button class="btn">Post</button></form>
<h2>Entries</h2>
<?php foreach (array_reverse($entries) as $e): ?>
<div class="entry"><span class="name"><?= $e['name'] ?></span><div><?= $e['msg'] ?></div></div>
<?php endforeach; ?>
<p style="color:#8b949e;font-size:12px">Admin bot visits every 30 seconds.</p>
</body></html>
