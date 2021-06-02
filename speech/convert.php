<?php

if (defined('STDIN')) {
  $snd_file = $argv[1];
}


if(strlen($snd_file)<3){
    exit('no params');
}



# [START speech_quickstart]
# Includes the autoloader for libraries installed with composer
require __DIR__ . '/vendor/autoload.php';



# Imports the Google Cloud client library
use Google\Cloud\Speech\V1\SpeechClient;
use Google\Cloud\Speech\V1\RecognitionAudio;
use Google\Cloud\Speech\V1\RecognitionConfig;
use Google\Cloud\Speech\V1\RecognitionConfig\AudioEncoding;



use Google\Cloud\Language\LanguageClient;
putenv('GOOGLE_APPLICATION_CREDENTIALS=/home/pi/bak1/raimundas-org-sinteze-126fab8818af.json'); //your path to file of cred


#putenv('GOOGLE_APPLICATION_CREDENTIALS=/home/pi/keys/raimundas-org-sinteze-126fab8818af.json');
#$client->useApplicationDefaultCredentials();



# The name of the audio file to transcribe
$audioFile = $snd_file;

# get contents of a file into a string
$content = file_get_contents($audioFile);

# set string as audio content
$audio = (new RecognitionAudio())
    ->setContent($content);

# The audio file's encoding, sample rate and language
$config = new RecognitionConfig([
//    'encoding' => AudioEncoding::LINEAR16,
//    'sample_rate_hertz' => 8000,
    'language_code' => 'lt-LT'
]);

# Instantiates a client
$client = new SpeechClient();

# Detects speech in the audio file
$response = $client->recognize($config, $audio);

# Print most likely transcription
foreach ($response->getResults() as $result) {
    $alternatives = $result->getAlternatives();
    $mostLikely = $alternatives[0];
    $transcript = $mostLikely->getTranscript();
    //printf('Transcript: %s' . PHP_EOL, $transcript);


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

# [END speech_quickstart]
