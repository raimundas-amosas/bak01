<?php

require("datab.php");
require("config.php");
$db=new datab;
$db->mysqli_conn("db");

$payload = json_encode(array("rows"=>json_encode($rows)));
$ch = curl_init("https://raimundas.org/bak01/synch.php?act=commands&key=3691308f2a4c2f6983f2880d32e29c84");
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload );
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type:application/json'));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 
$output = curl_exec($ch);      
curl_close($ch);
        
$rows=json_decode($output, true);
if(is_array($rows)){
    foreach($rows as $key=>$val){
        $sel="SELECT COUNT(`id`) AS `qty` FROM `b01_commands` WHERE `id`='{$val['id']}';";
        $qty=$db->val($sel, "qty");
        
        if(intval($qty)==0){
            $ins="INSERT INTO `b01_commands` (`alias`, `text`, `active`) "
                    . "VALUES ('{$val['alias']}', '{$val['text']}', '{$val['active']}');";
            $db->query($ins);
        }else{
            $upd="UPDATE `b01_commands` SET `alias`='{$val['alias']}', `text`='{$val['text']}', "
            . "`active`='{$val['active']}' WHERE `id`='{$val['id']}'";
            $db->query($upd);
        }
    }
}
$db->quit();

echo json_encode(array("res"=>"updated"));
