-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: reklama
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `phonenumber` varchar(20) DEFAULT NULL,
  `photo_url` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_name` (`name`(255))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `played_reklama`
--

DROP TABLE IF EXISTS `played_reklama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `played_reklama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `radio` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `date_played` date DEFAULT NULL,
  `time_played` time DEFAULT NULL,
  `radio_id` int(11) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `filename` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `block` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `radio_index` (`radio`),
  KEY `time_played_index` (`time_played`),
  KEY `date_played_index` (`date_played`),
  KEY `track_id_index` (`track_id`),
  KEY `radio_id` (`radio_id`),
  KEY `filename` (`filename`(255))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `played_reklama`
--

LOCK TABLES `played_reklama` WRITE;
/*!40000 ALTER TABLE `played_reklama` DISABLE KEYS */;
/*!40000 ALTER TABLE `played_reklama` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radio`
--

DROP TABLE IF EXISTS `radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `logo` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radio`
--

LOCK TABLES `radio` WRITE;
/*!40000 ALTER TABLE `radio` DISABLE KEYS */;
/*!40000 ALTER TABLE `radio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reklama`
--

DROP TABLE IF EXISTS `reklama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reklama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `track_id` varchar(255) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `name` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  `long_text` text,
  `producer` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `status` char(1) DEFAULT NULL,
  `filename` varchar(2048) CHARACTER SET utf8 DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `language` char(2) DEFAULT NULL,
  `company_name` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `track_id` (`track_id`),
  KEY `name_index` (`name`(255)),
  KEY `company_index` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reklama`
--

LOCK TABLES `reklama` WRITE;
/*!40000 ALTER TABLE `reklama` DISABLE KEYS */;
/*!40000 ALTER TABLE `reklama` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-29 12:16:53
