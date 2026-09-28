<?php
// VULN: fixed demo credentials, then trust the session entirely.
session_start();
$users = ['alice' => 'alice123', 'bob' => 'bob123', 'carol' => 'carol123'];  // bob is the finance manager
$u = $_POST['username'] ?? ''; $p = $_POST['password'] ?? '';
if (isset($users[$u]) && $users[$u] === $p) {
  $_SESSION['user'] = $u; $_SESSION['uid'] = ['alice'=>1001,'bob'=>1002,'carol'=>1003][$u];
  header('Location: /dashboard.php'); exit;
}
?><!doctype html><html><head><title>Login</title></head><body style="font-family:system-ui;background:#0d1117;color:#c9d1d9;padding:40px">
<h1>Invalid credentials</h1><a href="/">Back</a></body></html>
