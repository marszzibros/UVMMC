<?php
    // Headers
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json');
    include_once '../config/Database.php';
    include_once '../models/Record.php';

    // Instantiate DB & connect
    $database = new Database();
    $db = $database->connect();

    if (isset($_GET["group_id"])) {
        // Instantiate record object
        $record = new Record($db);

        // readers query
        $result = $record->read($_GET["group_id"]);

        // Get Row count
        $num = $result -> rowCount();

        // Check if any records
        if($num > 0) {
            // reader array
            $record_arr = array();
            $record_arr['data'] = array();

            while($row = $result -> fetch(PDO::FETCH_ASSOC)) {
                extract($row);
                $record_item = array(
                    'entered_time' => $entered_time,
                    'x' => $x,
                    'y' => $y,
                    'z' => $z,
                    'a' => $a,
                    'b' => $b,
		            'item_order' => $item_order,
                    'sample_name' => $sample_name,
                    'group_id' => $group_id,
                    'target' => $target
                );
                try{
                // Push to "data"
                    array_push($record_arr['data'], $record_item);
                }
                catch(Exception $e){
                    echo $e;
                }
            }

            // Turn to JSON & output
            echo json_encode($record_arr);
        }
        else{
            // no group_id found
            echo json_encode(
                array('message' => 'No information found')
            );
        }
    }
    else{
        // no readers
        echo json_encode(
            array('message' => 'please provide the group_id')
        );
    }

?>

