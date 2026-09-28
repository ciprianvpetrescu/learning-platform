<?php
// VULN: IDOR - the id is taken from the request with no ownership check.
session_start();
if (!isset($_SESSION['user'])) { header('Location: /'); exit; }
$id = preg_replace('/[^0-9]/', '', $_GET['id'] ?? (string)$_SESSION['uid']);
$f = "/var/www/invoices/$id.txt";
?><!doctype html><html><head><title>Invoice <?= htmlspecialchars($id) ?></title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
pre{background:#161b22;padding:16px;border-radius:6px;border:1px solid #30363d;white-space:pre-wrap}a{color:#58a6ff}</style></head><body>
<h1>Invoice <?= htmlspecialchars($id) ?></h1>
<?php if (file_exists($f)): ?><pre><?= htmlspecialchars(file_get_contents($f)) ?></pre>
<?php else: ?><p>Invoice not found.</p><?php endif; ?>
<p><a href="dashboard.php">Back to dashboard</a></p></body></html>
