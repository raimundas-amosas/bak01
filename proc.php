<?php


require("datab.php");
require("config.php");

$nb=array(1=>"Pirma", 2=>"Antra", 3=>"Trečia", 4=>"Ketvirta", 5=>"Penkta", 6=>"Šešta", 7=>"Septinta", 8=>"Aštunta", 9=>"Devinta", 10=>"Dešimta");
$tx=array("pirma"=>1, "antra"=>2, "trecia"=>3, "ketvirta"=>4, "penkta"=>5, "sesta"=>6, "septinta"=>7, "astunta"=>8, "devinta"=>9, "desimta"=>10);
$db=new datab;
$db->mysqli_conn("db");



$transcript=$argv[1];
$alias=str_replace("_", "-", $argv[2]);
$filename=$argv[3];
$rec_file="tts/komanda-{$filename}.wav";

$unknown=false;
$cmd="";


if(strpos($alias, "tema")!==false){
    
    $act="topic";
    foreach($tx as $a=>$t){
        $alias=str_replace($a, $t, $alias);
    }
    
    $tema=intval(preg_replace("/[^0-9]/", "", $alias));
    $alias=str_replace("[x]", $tema, $alias);
    
    if($tema>0){
        $sel="SELECT * FROM `b01_topics` WHERE `alias` LIKE '%{$alias}%' AND `active`='yes';";
        $row=$db->row($sel);

        $rc_file="topic_".$row['id'];

        if(intval($row['id'])>0&&strlen($row['sound_file'])==0){
            $row['text']=$row['name'].". ".$row['text'];
            $cmd="convert";
        }elseif(intval($row['id'])>0&&strlen($row['sound_file'])>0){
            $cmd="read";
        }else{
            $unknown=true;
        }
    }else{
        $unknown=true;
    }
    
    
}else{
    $act="command";
    $sel="SELECT * FROM `b01_commands` WHERE `alias` LIKE '%{$alias}%' AND `active`='yes';";
    $row=$db->row($sel);


    $rc_file="cmd_".intval($row['id']);


    if($row['id']>0&&strlen($row['sound_file'])==0){
        $tpc="";
        $sel="SELECT `name`, `num` FROM `b01_topics` WHERE `active`='yes' ORDER BY `num` ASC;";
        $rows=$db->all($sel);
        if(is_array($rows)){
            foreach($rows as $k=>$v){
                $tpc.=$nb[$v['num']]." tema: ".$v['name'].". ";
            }
        }
        $row['text']=str_replace("_TOPICS_", $tpc, $row['text']);
        $cmd="convert";



    }elseif($row['id']>0&&strlen($row['sound_file'])>0){
        $cmd="read";
    }else{
        $unknown=true;
    }

}

echo json_encode(array("ret"=>"ok", "cnt"=>(intval($row['id']>0)?1:0),"rec_file"=>"{$rc_file}", "row"=>$row, "cmd"=>$cmd, "act"=>$act, "unknown"=>$unknown));


$db->quit();