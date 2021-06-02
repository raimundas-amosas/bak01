<?php
if (defined('STDIN')) {
  $snd_file = $argv[1];
}
if(strlen($snd_file)<3){
    exit('no params');
}
require __DIR__ . '/vendor/autoload.php';
use Google\Cloud\Speech\V1\SpeechClient;
use Google\Cloud\Speech\V1\RecognitionAudio;
use Google\Cloud\Speech\V1\RecognitionConfig;
use Google\Cloud\Speech\V1\RecognitionConfig\AudioEncoding;

use Google\Cloud\Language\LanguageClient;
putenv('GOOGLE_APPLICATION_CREDENTIALS=/home/pi/bak1/JUSU-RAKTAS.json');
$audioFile = $snd_file;
$content = file_get_contents($audioFile);
$audio = (new RecognitionAudio())->setContent($content);
$config = new RecognitionConfig([
    'language_code' => 'lt-LT'
]);
$client = new SpeechClient();
$response = $client->recognize($config, $audio);
foreach ($response->getResults() as $result) {
    $alternatives = $result->getAlternatives();
    $mostLikely = $alternatives[0];
    $transcript = $mostLikely->getTranscript();
    $alias=str_replace(
	array("ą", "č", "ę", "ė", "į", "š", "ų", "ū", "ž", "Ą", "Č", "Ę", "Ė", "Į", "Š", "Ų", "Ū", "Ž" ), 
	array("a", "c", "e", "e", "i", "s", "u", "u", "z", "a", "c", "e", "e", "i", "s", "u", "u", "z"), $transcript);
    $alias=str_replace(array(" ", "_", ",", "."), "-", $alias);
    $alias=preg_replace("/[^0-9a-z\-]/", "", strtolower($alias));
    $alias=str_replace(array("*-", "-*"), "", "*".$alias."*");
    $alias=str_replace("*", "", $alias);
    $alias=str_replace("--", "-", $alias);

    if(strlen($transcript)>0){
	echo json_encode(array("alias"=>$alias, "transcript"=>$transcript));
    }else{
	echo "nan";
    }
}
$client->close();

