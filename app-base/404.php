<?php

// This script is going to check to see this page exists on p.gko.net
if(file_exists('../../p.gkoberger.net' . $_SERVER["REDIRECT_SCRIPT_URL"])) {
	Header( "HTTP/1.1 301 Moved Permanently" );
	Header( "Location: http://www.p.gkoberger.net" . $_SERVER["REDIRECT_SCRIPT_URL"]); 
}

