<?php session_start(); ?><!doctype html><html><head><title>Ledger - Invoicing</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
input{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:8px;width:100%;margin:6px 0;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:10px 16px;cursor:pointer}a{color:#58a6ff}
.box{border:1px solid #30363d;padding:16px;border-radius:8px;margin:14px 0}</style></head><body>
<h1>Ledger</h1>
<div class="box"><h2>Sign in</h2>
<form method="post" action="login.php">
<input name="username" placeholder="username" value="alice">
<input name="password" type="password" placeholder="password" value="alice123">
<button class="btn">Sign in</button></form>
<p><small>Demo account: alice / alice123</small></p></div>
<p>Invoices are at <code>/invoice.php?id=N</code> once signed in.</p>
</body></html>
