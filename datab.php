<?php

class datab{
var $db_link;

function mysqli_conn($db){
global $dbc;
    $this->db_link = mysqli_connect($dbc[$db]['host'],$dbc[$db]['username'],$dbc[$db]['password'], $dbc[$db]['dbname']);
    if(isset($dbc[$db]['enc'])){
        mysqli_query($this->db_link, "SET NAMES '{$dbc[$db]['enc']}';");
    }else{
        mysqli_query($this->db_link, "SET NAMES 'UTF8;");
    }
    
}

function mysqli_quit(){
	mysqli_close($this->db_link);
}

function all($que){
    $mas=array();
    $result=$this->db_link->query($que);
    foreach ( $result as $row ) {
        $mas[]=$row;
    }
    $result->free();
return $mas;
}


function row($que, $el=0){
    $mas=array();
    $result=$this->db_link->query($que);
    foreach ( $result as $row ) {
        $mas[]=$row;
    }
    $result->free();
return $mas[$el];
}


function val($que, $key, $el=0){
    $mas=array();
    $result=$this->db_link->query($que);
    foreach ( $result as $row ) {
        $mas[]=$row;
    }
    $result->free();
return $mas[$el][$key];
}

function query($que){
    if (!mysqli_query($this->db_link, $que)){
        printf("Error message: %s\n", mysqli_error($this->db_link));
    }
}

function id(){
     return mysqli_insert_id($this->db_link);
}

function quit(){
    mysqli_close($this->db_link);
}

} // eof class datab





