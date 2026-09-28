<?php
session_start();
if (!isset($_SESSION['user'])) { header('Location: /'); exit; }
// Generate invoices for every user. alice sees 1001. Bob's is 1002 and holds the flag.
$dir = '/var/www/invoices'; @mkdir($dir, 0777, true);
if (!file_exists("$dir/1001.txt")) {
  file_put_contents("$dir/1001.txt", "INVOICE 1001\nClient: Alice\nAmount: 240.00 GBP\nNotes: standard retainer\n");
  file_put_contents("$dir/1002.txt", "INVOICE 1002\nClient: Bob (Finance)\nAmount: 9800.00 GBP\nNotes: Acquisition payment\nAcquisition vault code: " . trim(@file_get_contents('/var/www/flag.txt')) . "\n");
  file_put_contents("$dir/1003.txt", "INVOICE 1003\nClient: Carol\nAmount: 120.00 GBP\n");
}
$mine = $_SESSION['uid'];
?><!doctype html><html><head><title>Ledger</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
a{color:#58a6ff}.box{border:1px solid #30363d;padding:16px;border-radius:8px;margin:14px 0}</style></head><body>
<h1>Dashboard</h1><p>Signed in as <b><?= htmlspecialchars($_SESSION['user']) ?></b> (uid <?= $mine ?>)</p>
<div class="box"><h2>Your invoices</h2>
<p><a href="invoice.php?id=<?= $mine ?>">View invoice <?= $mine ?></a></p>
<p><a href="export.php?user=<?= $mine ?>">Export my invoices</a></p></div>
<p><a href="logout.php">Sign out</a></p></body></html>
