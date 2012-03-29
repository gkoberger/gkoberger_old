<?php

function url_exists($url) {
    $ch = @curl_init($url);
    @curl_setopt($ch, CURLOPT_HEADER, TRUE);
    @curl_setopt($ch, CURLOPT_NOBODY, TRUE);
    @curl_setopt($ch, CURLOPT_FOLLOWLOCATION, FALSE);
    @curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $status = array();
    preg_match('/HTTP\/.* ([0-9]+) .*/', @curl_exec($ch) , $status);
    return ($status[1] == 200);
}

// This script is going to check to see this page exists on p.gko.net
if(url_exists('http://p.gkoberger.net' .  $_SERVER["REDIRECT_SCRIPT_URL"]) || url_exists('http://p.gkoberger.net' .  $_SERVER["REDIRECT_SCRIPT_URL"] . '/')) {
        Header( "HTTP/1.1 301 Moved Permanently" );
        Header( "Location: http://www.p.gkoberger.net" . $_SERVER["REDIRECT_SCRIPT_URL"]);
}

$filename = "p404.html";
$handle = fopen($filename, "r");
$contents = fread($handle, filesize($filename));
fclose($handle);

echo $contents;
