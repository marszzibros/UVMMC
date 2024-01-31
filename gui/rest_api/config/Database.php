<?php
    class Database{
        // DB Params
        private $host = 'webdb.uvm.edu';
        private $db_name = 'JJUNG2_AUTOMATION_DATABASE';
        private $username = 'jjung2_admin';
        private $password = 'UzAn4dsM6VIZigk1';
        private $conn;
        // DB Connect
        public function connect(){
            $this->conn = null;

            try {
                $this->conn = new PDO('mysql:host='.$this->host.';dbname ='.$this->db_name, $this->username, $this->password);
            } catch (PDOException $e){
                echo 'Connection Error: ' . $e->getMessage();
            }
            
            return $this->conn;
        }
    }
?>
