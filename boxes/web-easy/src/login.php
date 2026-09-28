<?php
// VULN: string concatenation into SQL.
session_start();
$u = $_POST['username'] ?? '';
$p = $_POST['password'] ?? '';
$db = new PDO('sqlite:/var/www/data.db');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$q = "SELECT * FROM users WHERE username = '" . $u . "' AND password = '" . $p . "'";
?><!doctype html><html><head><title>Login</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
pre{background:#161b22;padding:14px;border-radius:6px;overflow:auto;border:1px solid #30363d}a{color:#58a6ff}.err{color:#f85149}</style></head><body>
<h1>Login result</h1>
<?php
try {
  $rows = $db->query($q)->fetchAll(PDO::FETCH_ASSOC);
  if (count($rows) > 0) {
    $_SESSION['user'] = $rows[0]['username']; $_SESSION['role'] = $rows[0]['role'];
    echo "<h2>Welcome, " . htmlspecialchars($rows[0]['username']) . "</h2>";
    echo "<p>Role: " . htmlspecialchars($rows[0]['role']) . "</p>";
    if ($rows[0]['role'] === 'admin') echo "<p>Admin panel: <a href=\"/admin/\">/admin/</a></p>";
  } else { echo "<p class=\"err\">Invalid credentials.</p>"; }
} catch (Exception $e) {
  echo "<pre>SQL error: " . htmlspecialchars($e->getMessage()) . "</pre>";
  echo "<pre>Query was: " . htmlspecialchars($q) . "</pre>";
}
?>
<p><a href="/">Back</a></p></body></html>
