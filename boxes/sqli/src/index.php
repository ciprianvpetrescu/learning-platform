<?php
// VULN: union-based SQL injection, with a verbose development build.
$q = $_GET['q'] ?? '';
$results = null; $error = null;
if ($q !== '') {
  try {
    $pdo = new PDO('mysql:host=localhost;dbname=archive', 'app', 'apppass');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $sql = "SELECT id, title, owner, body FROM documents WHERE title LIKE '%" . $q . "%'";
    $stmt = $pdo->query($sql);
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
  } catch (Exception $e) { $error = $e->getMessage(); }
}
?><!doctype html><html><head><title>Archive</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:900px;margin:40px auto;padding:20px}
input{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:9px;width:60%;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:10px 16px;cursor:pointer}
table{border-collapse:collapse;width:100%;margin-top:16px}td,th{border:1px solid #30363d;padding:8px;text-align:left}
pre{background:#161b22;padding:14px;border-radius:6px;border:1px solid #f85149;overflow:auto;color:#f85149}</style></head><body>
<h1>Document Archive</h1><p>Search the internal document store.</p>
<form method="get"><input name="q" placeholder="search titles..." value="<?= htmlspecialchars($q) ?>"><button class="btn">Search</button></form>
<?php if ($error): ?><pre>Database error: <?= htmlspecialchars($error) ?></pre><?php endif; ?>
<?php if ($results !== null && !$error): ?>
<table><tr><th>ID</th><th>Title</th><th>Owner</th><th>Body</th></tr>
<?php foreach ($results as $r): ?>
<tr><td><?= htmlspecialchars($r['id']) ?></td><td><?= htmlspecialchars($r['title']) ?></td><td><?= htmlspecialchars($r['owner']) ?></td><td><?= htmlspecialchars($r['body']) ?></td></tr>
<?php endforeach; ?></table>
<?php endif; ?>
<p style="color:#8b949e;font-size:12px">Query returns 4 columns. MySQL.
Flag at /var/www/flag.txt. The database user has FILE privilege.</p>
</body></html>
