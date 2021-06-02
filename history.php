<?php

require("datab.php");
require("config.php");
$db=new datab;
$db->mysqli_conn("db");

$device_id="device_id";
$transcript=$argv[1];
$cmd1=$argv[2];
$cmd2=$argv[3];
$date=date("Y-m-d H:i:s");

$ins="INSERT INTO `b01_history` (`device_id`, `date`, `transcript`, `cmd1`, `cmd2`) "
        . "VALUES ('{$device_id}', '{$date}', '{$transcript}', '{$cmd1}', '{$cmd2}');";
$db->query($ins);


$db->quit();