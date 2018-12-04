<?php

$msg = $_POST["message"];
$email = $_POST["email"];

$to = "maxxie114@mxpersonal.com";

$subject = "Email from " . $email . " via mxpersonal.com.";

$header = "From: no-reply@mxpersonal.com";
$status = mail($to,$subject,$msg,$header);

// echo $status ? "Mail sent" : "Mail failed";

if($status) {
    echo "<h1>Your message has been sent to Max Xie!<h1>";
} else {
    echo "<h1>System Error, the message has failed to be sent :(<h1>";
}

