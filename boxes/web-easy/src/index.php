<?php session_start(); ?><!doctype html>
<html><head><title>Vantage Group - Corporate Site</title>
<style>
body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:760px;margin:40px auto;padding:20px}
a{color:#58a6ff}input{background:#161b22;border:1px solid #30363d;color:#c9d1d9;padding:8px;width:100%;margin:6px 0;box-sizing:border-box}
.btn{background:#238636;border:0;color:#fff;padding:10px 16px;cursor:pointer}
.box{border:1px solid #30363d;padding:20px;border-radius:8px;margin:16px 0}
</style></head><body>
<h1>Vantage Group</h1>
<p>Internal document portal and staff login.</p>
<div class="box"><h2>Documents</h2>
<p><a href="download.php?file=welcome.txt">welcome.txt</a></p>
<p><a href="download.php?file=policy.txt">policy.txt</a></p>
<p><a href="download.php?file=faq.txt">faq.txt</a></p>
</div>
<div class="box"><h2>Staff Login</h2>
<form method="post" action="login.php">
<input name="username" placeholder="username" autocomplete="off">
<input name="password" type="password" placeholder="password" autocomplete="off">
<button class="btn" type="submit">Sign in</button>
</form>
<p><small>Development build - do not use real credentials.</small></p>
</div></body></html>
