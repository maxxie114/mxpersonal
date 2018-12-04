<?php

$msg = $_POST["message"];
$email = $_POST["email"];

$to = "maxxie114@mxpersonal.com";

$subject = "Email from " . $email . " via mxpersonal.com.";

$header = "From: ubuntu@mxpersonal.com";

$status = mail($to,$subject,$msg);

echo $email . "<br>";
echo $msg . "<br>";

echo $status ? "Mail sent" : "Mail failed";

echo "<h1>Your message has been sent to Max Xie!<h1>";
