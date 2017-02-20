<?php
/**
 * Created by PhpStorm.
 * User: matthias_home
 * Date: 4/25/16
 * Time: 1:27 PM
 */

include("./connector.php");
include("./pushHandler.php");
//echo $_GET["verification_challenge"];
$input = @file_get_contents("php://input");
$event_json = json_decode($input);
function getProfile($link, $id)
{
    $result = mysqli_query($link, "SELECT * from modelProfiles WHERE profileID='" . $id . "'");
    $num_rows = mysqli_num_rows($result);
    if (!$num_rows) {
        $result = mysqli_query($link, "SELECT * from clientProfiles WHERE profileID='" . $id . "'");
    }
    $row = mysqli_fetch_assoc($result);
    $currentProfile = $row;
    return $currentProfile;
}


function updateNotificationsForChat($link, $recipient, $sender, $newState)
{

    $result = mysqli_query($link, "SELECT * FROM notificationTable WHERE recipientID='$recipient' AND relevantPersonChat='$sender' AND status='$newState'");
    if (mysqli_num_rows($result)) {
        $row = mysqli_fetch_assoc($result);
        $quantity = intval($row['quantity']) + 1;
    } else {
        $quantity = 1;
    }
    mysqli_query($link, "DELETE FROM notificationTable WHERE recipientID='$recipient' AND relevantPersonChat='$sender' AND status='$newState'");
    mysqli_query($link, "INSERT INTO notificationTable (recipientID,relevantPersonChat,status,quantity) VALUES ('$recipient','$sender','$newState','$quantity')");
}

try {
    $eventID = $_SERVER["HTTP_LAYER_WEBHOOK_REQUEST_ID"];
    if (mysqli_num_rows(mysqli_query($link, "SELECT * FROM webhookIDs WHERE eventID='$eventID'"))) {
        syslog(LOG_INFO, 'already exist');
        syslog(LOG_INFO, $input);
    } else {
        $sender = $event_json->event->actor->user_id;
        foreach ($event_json->message->recipient_status as $recipient => $status) {
            try {
                if ($recipient != $sender) {
                    $recipientProfile = getProfile($link, $recipient);
                    $senderProfile = getProfile($link, $sender);
                    $sentMessage = mysqli_escape_string($link,str_replace('"', '', $event_json->message->parts[0]->body));
                    mysqli_query($link, "INSERT INTO webhookIDs (eventID,senderID,recipientID,message) VALUES ('$eventID','$sender','$recipient','$sentMessage')");
                    syslog(LOG_INFO, 'new entry');
                    syslog(LOG_INFO, $input);
                    updateNotificationsForChat($link, $recipient, $sender, "messageAdded");
                    $success = handlePush($link, $recipient, $senderProfile["firstName"] . " " . $senderProfile["lastName"] . ": " . $sentMessage, "messageAdded", $senderProfile["profileID"]);
                    if (mysqli_num_rows(mysqli_query($link, "SELECT * FROM chatProfiles WHERE (profileID1='$sender' AND profileID2='$recipient')"))) {
                        mysqli_query($link, "UPDATE chatProfiles SET mostRecentText='$sentMessage' WHERE (profileID1='$sender' AND profileID2='$recipient')");
                    } else {
                        if (mysqli_num_rows(mysqli_query($link, "SELECT * FROM chatProfiles WHERE (profileID1='$recipient' AND profileID2='$sender')"))) {
                            mysqli_query($link, "UPDATE chatProfiles SET mostRecentText='$sentMessage' WHERE (profileID1='$recipient' AND profileID2='$sender')");
                        } else {
                            mysqli_query($link, "INSERT INTO chatProfiles (profileID1, profileID2,mostRecentText) VALUES('$recipient','$sender','$sentMessage')");
                        }
                    }
                    mysqli_query($link, "INSERT INTO webhookIDs (eventID,senderID,recipientID,message) VALUES ('$eventID','$sender','$recipient','repeat')");
                }
            }
            catch
            (MyException $e) {
            }
        }
    }
} catch
(MyException $e) {
}
http_response_code(204);
