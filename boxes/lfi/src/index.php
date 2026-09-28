<?php
// VULN: local file inclusion with no validation whatsoever.
$page = $_GET['page'] ?? 'home';
?><!doctype html><html><head><title>Pamphlet CMS</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
a{color:#58a6ff}input{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:8px;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:9px 14px;cursor:pointer}.nav a{margin-right:14px}
pre{background:#161b22;padding:14px;border-radius:6px;border:1px solid #30363d;overflow:auto}</style></head><body>
<h1>Pamphlet CMS</h1>
<div class="nav"><a href="?page=home">Home</a><a href="?page=about">About</a><a href="?page=contact">Contact</a></div>
<hr>
<div>
<?php
$target = "pages/" . $page . ".php";
if (file_exists($target)) { include($target); }
else { echo "<p>Page not found: <code>" . htmlspecialchars($target) . "</code></p>"; }
?>
</div><hr>
<h3>Feedback</h3><p>We log every feedback submission to our access log.</p>
<form method="get" action="index.php">
<input type="hidden" name="page" value="home">
<input name="ref" placeholder="reference code" size="40">
<button class="btn">Submit feedback</button></form>
<p style="color:#8b949e;font-size:12px">Log at /var/log/php-lab/access.log</p>
</body></html>
