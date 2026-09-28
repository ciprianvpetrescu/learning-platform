<?php
// VULN: no path sanitisation. file= can point anywhere.
$file = isset($_GET['file']) ? $_GET['file'] : 'welcome.txt';
$path = "docs/" . $file;
if (file_exists($path)) { header('Content-Type: text/plain'); readfile($path); }
else { header('Content-Type: text/plain', true, 404); echo "File not found: " . $path . "\n"; }
?>
