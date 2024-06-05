<?php
    class Record {
        // DB stuff
        private $conn;
        private $table = 'RECORD_SAMPLE';

        // tblReaders properties
        public $id;
        public $entered_time;
        public $x;
        public $y;
        public $z;
        public $a;
        public $b;
	    public $item_order;
        public $sample_name;
        public $group_id;
        public $target;

        // Constructor with DB
        public function __construct($db){
            $this->conn = $db;
        }
        public function all() {
            // Create Query
            $query = 'SELECT * FROM JJUNG2_AUTOMATION_DATABASE.' . $this -> table .';';
            $stmt = $this->conn->prepare($query);
            try{
            // Execute Query
            $stmt -> execute();
            }
            catch (Exception $e){
                echo $e;
            }
            return $stmt;
        }
        // Get records
        public function read($group_id) {
            // Create Query
            $query = 'SELECT * FROM JJUNG2_AUTOMATION_DATABASE.' . $this -> table .' WHERE group_id = "'.$group_id.'";';
            $stmt = $this->conn->prepare($query);
            try{
            // Execute Query
            $stmt -> execute();
            }
            catch (Exception $e){
                echo $e;
            }
            return $stmt;
        }
        // write new records
        public function write($data) {
            // Create Query
            $query_record = "INSERT INTO JJUNG2_AUTOMATION_DATABASE.".$this -> table." (entered_time, x, y, z, a, b, item_order,sample_name, group_id,target)
            VALUES ('".$data['data']['entered_time']."',".$data['data']['x'].",".$data['data']['y'].
            ",".$data['data']['z'].",".$data['data']['a'].",".$data['data']['b'].
            ",".$data['data']['item_order'].",'".$data['data']['sample_name']."','".$data['data']['group_id']."','".$data['data']['target']."');";
            
	    $stmt = $this->conn->prepare($query_record);
	
            try{
            // Execute Query
                $stmt -> execute();
            }
            catch (Exception $e){
                echo $e;
            }
            return $stmt;
        }    
    }
?>
