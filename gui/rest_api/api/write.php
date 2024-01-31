<?php
    // Headers
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json');
    include_once '../config/Database.php';
    include_once '../models/Record.php';

    // Instantiate DB & connect
    $database = new Database();
    $db = $database->connect();

    // POST
    if ($_SERVER["REQUEST_METHOD"] == "POST") {

	$data = json_decode(file_get_contents('php://input'), true);
        if(!empty($_POST['group_id'])){
            $record = new Record($db);
            $record_data = array();
            $record_data['data'] = array();
            $now = DateTime::createFromFormat('U.u', microtime(true));
            $record_data['data']['entered_time'] = $now->format("Y-m-d H:i:s.u");
            $record_data['data']['x'] = $_POST['x'];
            $record_data['data']['y'] = $_POST['y'];
            $record_data['data']['z'] = $_POST['z'];
            $record_data['data']['a'] = $_POST['a'];
            $record_data['data']['b'] = $_POST['b'];
	        $record_data['data']['item_order'] = $_POST['order'];
            $record_data['data']['sample_name'] = $_POST['sample_name'];
            $record_data['data']['group_id'] = $_POST['group_id'];
            $record_data['data']['target'] = $_POST['target'];
            $record -> write($record_data);
        }
        else {
            echo json_encode(
                array('message' => 'Invalid Request (no group_id)')
            );
        }
    }
    else {
        echo json_encode(
            array('message' => 'Invalid Request (wrong request)')
        );
    }
?>
