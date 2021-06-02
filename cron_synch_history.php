<?php

require("datab.php");
require("config.php");
$db=new datab;
$db->mysqli_conn("db");

$sel="SELECT * FROM `b01_history` WHERE `synch`='no';";
$rows=$db->all($sel);

if(count($rows)>0){
    $payload = json_encode(array("rows"=>json_encode($rows)));
    $ch = curl_init("https://raimundas.org/bak01/synch.php?act=history&key=3691308f2a4c2f6983f2880d32e29c84");
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload );
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 
    $output = curl_exec($ch);      
    curl_close($ch);
    echo $output;



    foreach($rows as $key=>$val){
        $upd="UPDATE `b01_history` SET `synch`='yes' WHERE `id`='{$val['id']}';";
        $db->query($upd);
    }
}
        
$db->quit();