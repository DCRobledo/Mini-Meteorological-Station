docker exec -it iotservicescode_mariaDB_1 mysql -uroot -probledogarcia

create database final_practice;

grant all privileges on final_practice.* TO 'iot_user'@'%' identified by 'robledogarcia';

flush privileges;

use final_practice;

CREATE OR REPLACE TABLE measurements (
   id MEDIUMINT NOT NULL AUTO_INCREMENT, 
   humidity float NOT NULL, 
   temperature float NOT NULL,
   timestamp datetime NOT NULL,
   UNIQUE (timestamp),
   PRIMARY KEY (id)
);

SELECT temperature, humidity, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1;

CREATE OR REPLACE TABLE devices (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    device_id varchar(50) NOT NULL,
    device_state varchar(15) NOT NULL,
    device_location varchar(80) NOT NULL,
    device_timestamp datetime NOT NULL,
    UNIQUE (device_id),
    PRIMARY KEY (id)
);

SELECT device_id, device_location, device_timestamp FROM devices ORDER BY id DESC LIMIT 1;