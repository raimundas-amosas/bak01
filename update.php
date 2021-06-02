<?php


require("datab.php");
require("config.php");

$db=new datab;
$db->mysqli_conn("db");



$rec_file=$argv[1];
$id=$argv[2];
$act=$argv[3];


if(intval($id)>0&&strlen($rec_file)>0&&strlen($act)>0){
    
    if($act=="command"){
        $upd="UPDATE `b01_commands` SET `sound_file`='{$rec_file}' WHERE `id`='{$id}';";
        $db->query($upd);
    }elseif($act=="topic"){
        $upd="UPDATE `b01_topics` SET `sound_file`='{$rec_file}' WHERE `id`='{$id}';";
        $db->query($upd);
    }
    echo "REC FILE Saved\n";
}

$db->quit();