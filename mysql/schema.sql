USE airflowcovid;

CREATE TABLE `airflowcovid`.`confirmed` (
    `Province` VARCHAR(100) NULL,
    `Country` VARCHAR(100) NULL,
    `Lat` VARCHAR(100) NULL,
    `Lon` VARCHAR(100) NULL,
    `Date` VARCHAR(100) NULL,
    `Cases` INT NULL,
    `Increment` INT NULL
);

CREATE TABLE `airflowcovid`.`death` (
    `Province` VARCHAR(100) NULL,
    `Country` VARCHAR(100) NULL,
    `Lat` VARCHAR(100) NULL,
    `Lon` VARCHAR(100) NULL,
    `Date` VARCHAR(100) NULL,
    `Deaths` INT NULL
);


CREATE TABLE `airflowcovid`.`recoverd` (
    `Province` VARCHAR(100) NULL,
    `Country` VARCHAR(100) NULL,
    `Lat` VARCHAR(100) NULL,
    `Lon` VARCHAR(100) NULL,
    `Date` VARCHAR(100) NULL,
    `Recovered` INT NULL
);