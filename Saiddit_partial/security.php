<?php

$mainpass = "mary123";

$md5pass = md5($mainpass);
$sha1pass = sha1($mainpass);
$crytpass = crypt($mainpass,'st');

echo "$md5pass <br />";
echo "$sha1pass <br />";
echo "$crytpass <br />";

?>