<?php
// The admin bot. Visits the guestbook with a privileged cookie present.
// In the lab the cookie is exposed to any XSS payload that fires here.
header('X-Admin-Note: bot endpoint');
?><!doctype html><html><head><title>Admin Bot</title>
<style>body{font-family:system-ui;background:#0d1117;color:#c9d1d9;max-width:720px;margin:40px auto;padding:20px}</style></head><body>
<h1>Admin bot</h1><p>This endpoint simulates the administrator visiting the guestbook.</p>
<p>The admin session cookie has no HttpOnly flag, which is the whole point of the lab.</p>
<p>Flag is at /var/www/flag.txt; the admin can read it. You cannot. Get the cookie.</p>
</body></html>
