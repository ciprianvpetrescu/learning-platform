<?php
// VULN: same IDOR via a different parameter name. Always check both.
session_start();
if (!isset($_SESSION['user'])) { header('Location: /'); exit; }
$u = preg_replace('/[^0-9]/', '', $_GET['user'] ?? (string)$_SESSION['uid']);
$f = "/var/www/invoices/$u.txt";
header('Content-Type: text/plain');
echo file_exists($f) ? file_get_contents($f) : "No export available\n";
