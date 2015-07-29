DROP TABLE IF EXISTS `company`;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `phonenumber` varchar(20) DEFAULT NULL,
  `photo_url` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_name` (`name`(255))
) ;


DROP TABLE IF EXISTS `reklama`;
CREATE TABLE `reklama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `company` int(11) not NULL,
  `name` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  `long_text` text default null,
  `producer` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  `date_added` date default null,
  `date_start` date default null,
  `date_end` date default null,
  `status`   char(1) DEFAULT NULL,
  `filename` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `length` int(11) default null,
  PRIMARY KEY (`id`),
  UNIQUE KEY `track_id` (`track_id`),
  KEY `name_index` (`name`),
  KEY `company_index` (`company`)
);


DROP TABLE IF EXISTS `played_reklama`;
CREATE TABLE `played_reklama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `radio` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `date_played` date DEFAULT NULL,
  `time_played` time DEFAULT NULL,
  `radio_id` int(11) DEFAULT NULL,
  `length` int(11) default null,
  `filename` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `suspect` char(1) default null,
  PRIMARY KEY (`id`),
  KEY `radio_index` (`radio`),
  KEY `time_played_index` (`time_played`),
  KEY `date_played_index` (`date_played`),
  KEY `track_id_index` (`track_id`),
  KEY `radio_id` (`radio_id`),
  KEY `filename` (`filename`)
);


DROP TABLE IF EXISTS `radio`;
CREATE TABLE `radio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `logo` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;


