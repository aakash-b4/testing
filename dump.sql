-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: payout_database
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apis_bankmodel`
--

DROP TABLE IF EXISTS `apis_bankmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_bankmodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(100) NOT NULL,
  `bank_code` varchar(100) NOT NULL,
  `nodal_account_number` varchar(300) NOT NULL,
  `nodal_ifsc` varchar(300) NOT NULL,
  `nodal_account_name` varchar(300) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_bankmodel`
--

LOCK TABLES `apis_bankmodel` WRITE;
/*!40000 ALTER TABLE `apis_bankmodel` DISABLE KEYS */;
INSERT INTO `apis_bankmodel` VALUES (1,'HDFC','1010','test','test','test','2021-06-22 11:16:55.255150','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `apis_bankmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_chargemodel`
--

DROP TABLE IF EXISTS `apis_chargemodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_chargemodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client` int(11) NOT NULL,
  `mode` int(11) NOT NULL,
  `min_amount` int(11) NOT NULL,
  `max_amount` int(11) NOT NULL,
  `charge_percentage_or_fix` int(11) NOT NULL,
  `charge_amount_percentage` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_chargemodel`
--

LOCK TABLES `apis_chargemodel` WRITE;
/*!40000 ALTER TABLE `apis_chargemodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_chargemodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_clientmodel`
--

DROP TABLE IF EXISTS `apis_clientmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_clientmodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client` int(11) NOT NULL,
  `client_code` varchar(60) NOT NULL,
  `auth_key` varchar(60) NOT NULL,
  `auth_iv` varchar(60) NOT NULL,
  `bank` int(11) NOT NULL,
  `client_password` varchar(100) NOT NULL,
  `client_username` varchar(100) NOT NULL,
  `is_merchant` tinyint(1) NOT NULL,
  `is_payout` tinyint(1) NOT NULL,
  `role` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_clientmodel`
--

LOCK TABLES `apis_clientmodel` WRITE;
/*!40000 ALTER TABLE `apis_clientmodel` DISABLE KEYS */;
INSERT INTO `apis_clientmodel` VALUES (1,2001,'KUBER','oLA38cwT6IYNGqb3','x0xzPnXsgTq0QqXx',1,'P8c3WQ7eiKub','kub789@sp',0,0,3,1,'2021-06-22 11:16:55.239518','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `apis_clientmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_featuremodel`
--

DROP TABLE IF EXISTS `apis_featuremodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_featuremodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `feature_name` varchar(300) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_featuremodel`
--

LOCK TABLES `apis_featuremodel` WRITE;
/*!40000 ALTER TABLE `apis_featuremodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_featuremodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_iphittingrecordmodel`
--

DROP TABLE IF EXISTS `apis_iphittingrecordmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_iphittingrecordmodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(300) NOT NULL,
  `hitting_time` datetime(6) NOT NULL,
  `ip_type` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_iphittingrecordmodel`
--

LOCK TABLES `apis_iphittingrecordmodel` WRITE;
/*!40000 ALTER TABLE `apis_iphittingrecordmodel` DISABLE KEYS */;
INSERT INTO `apis_iphittingrecordmodel` VALUES (1,'127.0.0.1','2021-06-14 14:45:19.766520','Blocked'),(2,'127.0.0.1','2021-06-14 14:45:22.941648','Blocked'),(3,'127.0.0.1','2021-06-14 14:47:20.124918','Blocked'),(4,'127.0.0.1','2021-06-14 14:47:49.430217','Blocked'),(5,'127.0.0.1','2021-06-14 14:47:52.166343','Blocked'),(6,'127.0.0.1','2021-06-14 14:47:56.687614','Blocked'),(7,'127.0.0.1','2021-06-14 14:49:27.841367','Allowed'),(8,'127.0.0.1','2021-06-14 14:49:28.239326','Allowed'),(9,'127.0.0.1','2021-06-14 14:49:30.384482','Allowed'),(10,'127.0.0.1','2021-06-14 14:49:30.963655','Allowed'),(11,'127.0.0.1','2021-06-14 14:49:32.746628','Allowed'),(12,'127.0.0.1','2021-06-14 14:49:33.000516','Allowed'),(13,'127.0.0.1','2021-06-14 14:49:36.770546','Allowed'),(14,'127.0.0.1','2021-06-14 14:51:36.013613','Allowed'),(15,'127.0.0.1','2021-06-14 14:51:36.198128','Allowed'),(16,'127.0.0.1','2021-06-14 14:51:36.749764','Allowed'),(17,'127.0.0.1','2021-06-14 14:52:22.649289','Allowed'),(18,'127.0.0.1','2021-06-14 14:52:53.050313','Allowed'),(19,'127.0.0.1','2021-06-14 14:52:53.282683','Allowed'),(20,'127.0.0.1','2021-06-14 14:52:54.902306','Allowed'),(21,'127.0.0.1','2021-06-14 14:52:55.265322','Allowed'),(22,'127.0.0.1','2021-06-14 14:52:57.948302','Allowed'),(23,'127.0.0.1','2021-06-14 14:52:58.458781','Blocked'),(24,'127.0.0.1','2021-06-14 14:53:49.651295','Blocked'),(25,'127.0.0.1','2021-06-14 14:59:39.172842','Allowed'),(26,'127.0.0.1','2021-06-14 14:59:39.453864','Allowed'),(27,'127.0.0.1','2021-06-14 14:59:39.730308','Allowed'),(28,'127.0.0.1','2021-06-14 15:43:06.241033','Allowed'),(29,'127.0.0.1','2021-06-14 15:43:06.514185','Allowed'),(30,'127.0.0.1','2021-06-14 15:43:08.394259','Allowed'),(31,'127.0.0.1','2021-06-14 15:43:22.774647','Allowed'),(32,'127.0.0.1','2021-06-14 15:43:23.037892','Allowed'),(33,'127.0.0.1','2021-06-14 15:43:39.810752','Allowed'),(34,'127.0.0.1','2021-06-14 15:43:39.983128','Allowed'),(35,'127.0.0.1','2021-06-14 15:43:40.430552','Allowed'),(36,'127.0.0.1','2021-06-14 15:45:23.796590','Allowed'),(37,'127.0.0.1','2021-06-14 15:45:26.097444','Allowed'),(38,'127.0.0.1','2021-06-14 16:03:48.620781','Allowed'),(39,'127.0.0.1','2021-06-14 16:03:52.873414','Allowed'),(40,'127.0.0.1','2021-06-14 16:03:55.962639','Allowed'),(41,'127.0.0.1','2021-06-14 16:03:57.840321','Allowed'),(42,'127.0.0.1','2021-06-14 16:04:02.819939','Allowed'),(43,'127.0.0.1','2021-06-14 16:04:04.254200','Allowed'),(44,'127.0.0.1','2021-06-14 16:04:09.450139','Allowed'),(45,'127.0.0.1','2021-06-14 16:04:09.989832','Allowed'),(46,'127.0.0.1','2021-06-14 16:04:12.173433','Allowed'),(47,'127.0.0.1','2021-06-14 16:04:12.629949','Allowed'),(48,'127.0.0.1','2021-06-14 16:04:21.731237','Allowed'),(49,'127.0.0.1','2021-06-14 16:04:22.837081','Allowed'),(50,'127.0.0.1','2021-06-14 16:04:29.665166','Allowed'),(51,'127.0.0.1','2021-06-14 16:04:30.250089','Allowed'),(52,'127.0.0.1','2021-06-14 16:04:32.351024','Allowed'),(53,'127.0.0.1','2021-06-14 16:04:32.764769','Allowed'),(54,'127.0.0.1','2021-06-15 10:22:11.962854','Allowed'),(55,'127.0.0.1','2021-06-15 10:22:13.028239','Allowed'),(56,'127.0.0.1','2021-06-15 10:23:46.667926','Allowed'),(57,'127.0.0.1','2021-06-15 10:24:06.929983','Allowed'),(58,'127.0.0.1','2021-06-15 10:24:39.851076','Allowed'),(59,'127.0.0.1','2021-06-15 10:25:08.808986','Allowed'),(60,'127.0.0.1','2021-06-15 10:25:22.316001','Allowed');
/*!40000 ALTER TABLE `apis_iphittingrecordmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_ipwhitelistedmodel`
--

DROP TABLE IF EXISTS `apis_ipwhitelistedmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_ipwhitelistedmodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client_model` int(11) NOT NULL,
  `ip_address` varchar(300) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_ipwhitelistedmodel`
--

LOCK TABLES `apis_ipwhitelistedmodel` WRITE;
/*!40000 ALTER TABLE `apis_ipwhitelistedmodel` DISABLE KEYS */;
INSERT INTO `apis_ipwhitelistedmodel` VALUES (1,1,'127.0.0.1',1,'2021-06-22 11:16:55.318383','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `apis_ipwhitelistedmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_ledgermodel`
--

DROP TABLE IF EXISTS `apis_ledgermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_ledgermodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client` int(11) NOT NULL,
  `client_code` varchar(60) NOT NULL,
  `amount` double NOT NULL,
  `bank` int(11) NOT NULL,
  `bank_ref_no` varchar(1000) NOT NULL,
  `customer_ref_no` varchar(1000) NOT NULL,
  `type_status` varchar(60) NOT NULL,
  `trans_type` varchar(20) NOT NULL,
  `bene_account_name` varchar(300) NOT NULL,
  `bene_account_number` varchar(300) NOT NULL,
  `bene_ifsc` varchar(300) NOT NULL,
  `trans_status` varchar(100) NOT NULL,
  `charge` double NOT NULL,
  `mode` int(11) NOT NULL,
  `request_header` varchar(400) NOT NULL,
  `trans_time` datetime(6) NOT NULL,
  `van` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_ledgermodel`
--

LOCK TABLES `apis_ledgermodel` WRITE;
/*!40000 ALTER TABLE `apis_ledgermodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_ledgermodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_modemodel`
--

DROP TABLE IF EXISTS `apis_modemodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_modemodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mode` varchar(300) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_modemodel`
--

LOCK TABLES `apis_modemodel` WRITE;
/*!40000 ALTER TABLE `apis_modemodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_modemodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_rolefeaturemodel`
--

DROP TABLE IF EXISTS `apis_rolefeaturemodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_rolefeaturemodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role` int(11) NOT NULL,
  `feature` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_rolefeaturemodel`
--

LOCK TABLES `apis_rolefeaturemodel` WRITE;
/*!40000 ALTER TABLE `apis_rolefeaturemodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_rolefeaturemodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_rolemodel`
--

DROP TABLE IF EXISTS `apis_rolemodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_rolemodel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(300) NOT NULL,
  `create` tinyint(1) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  `read` tinyint(1) NOT NULL,
  `update` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `deleted_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_rolemodel`
--

LOCK TABLES `apis_rolemodel` WRITE;
/*!40000 ALTER TABLE `apis_rolemodel` DISABLE KEYS */;
INSERT INTO `apis_rolemodel` VALUES (1,'admin',1,1,1,1,'2021-06-22 11:16:55.330380','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(2,'operational',0,0,0,0,'2021-06-22 11:16:55.330380','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000'),(3,'end_user',0,0,0,0,'2021-06-22 11:16:55.330380','0000-00-00 00:00:00.000000','0000-00-00 00:00:00.000000');
/*!40000 ALTER TABLE `apis_rolemodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apis_test2`
--

DROP TABLE IF EXISTS `apis_test2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `apis_test2` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `vv` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apis_test2`
--

LOCK TABLES `apis_test2` WRITE;
/*!40000 ALTER TABLE `apis_test2` DISABLE KEYS */;
/*!40000 ALTER TABLE `apis_test2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add bank model',7,'add_bankmodel'),(26,'Can change bank model',7,'change_bankmodel'),(27,'Can delete bank model',7,'delete_bankmodel'),(28,'Can view bank model',7,'view_bankmodel'),(29,'Can add client model',8,'add_clientmodel'),(30,'Can change client model',8,'change_clientmodel'),(31,'Can delete client model',8,'delete_clientmodel'),(32,'Can view client model',8,'view_clientmodel'),(33,'Can add ledger model',9,'add_ledgermodel'),(34,'Can change ledger model',9,'change_ledgermodel'),(35,'Can delete ledger model',9,'delete_ledgermodel'),(36,'Can view ledger model',9,'view_ledgermodel'),(37,'Can add charge model',10,'add_chargemodel'),(38,'Can change charge model',10,'change_chargemodel'),(39,'Can delete charge model',10,'delete_chargemodel'),(40,'Can view charge model',10,'view_chargemodel'),(41,'Can add feature model',11,'add_featuremodel'),(42,'Can change feature model',11,'change_featuremodel'),(43,'Can delete feature model',11,'delete_featuremodel'),(44,'Can view feature model',11,'view_featuremodel'),(45,'Can add mode model',12,'add_modemodel'),(46,'Can change mode model',12,'change_modemodel'),(47,'Can delete mode model',12,'delete_modemodel'),(48,'Can view mode model',12,'view_modemodel'),(49,'Can add role feature model',13,'add_rolefeaturemodel'),(50,'Can change role feature model',13,'change_rolefeaturemodel'),(51,'Can delete role feature model',13,'delete_rolefeaturemodel'),(52,'Can view role feature model',13,'view_rolefeaturemodel'),(53,'Can add role model',14,'add_rolemodel'),(54,'Can change role model',14,'change_rolemodel'),(55,'Can delete role model',14,'delete_rolemodel'),(56,'Can view role model',14,'view_rolemodel'),(57,'Can add ip hitting record model',15,'add_iphittingrecordmodel'),(58,'Can change ip hitting record model',15,'change_iphittingrecordmodel'),(59,'Can delete ip hitting record model',15,'delete_iphittingrecordmodel'),(60,'Can view ip hitting record model',15,'view_iphittingrecordmodel'),(61,'Can add ip white listed model',16,'add_ipwhitelistedmodel'),(62,'Can change ip white listed model',16,'change_ipwhitelistedmodel'),(63,'Can delete ip white listed model',16,'delete_ipwhitelistedmodel'),(64,'Can view ip white listed model',16,'view_ipwhitelistedmodel');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$260000$z20ahx4qZrJUVvvpbgt476$ARKm807tz+euuQlQd3AteyFULgt5FgaCECgukXDjQIs=','2021-06-13 05:16:53.882643',1,'payout_admin','','','',1,1,'2021-06-13 04:56:23.191142');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-06-13 05:03:35.070406','1','1',1,'[{\"added\": {}}]',14,1),(2,'2021-06-13 05:03:48.312170','2','2',1,'[{\"added\": {}}]',14,1),(3,'2021-06-13 05:03:57.742225','3','3',1,'[{\"added\": {}}]',14,1),(4,'2021-06-13 05:08:03.600973','1','1',2,'[{\"changed\": {\"fields\": [\"Create\", \"Read\", \"Update\", \"Delete\"]}}]',14,1),(5,'2021-06-13 05:08:24.606283','3','3',2,'[{\"changed\": {\"fields\": [\"Create\", \"Read\"]}}]',14,1),(6,'2021-06-13 05:08:30.492281','3','3',2,'[{\"changed\": {\"fields\": [\"Create\", \"Read\"]}}]',14,1),(7,'2021-06-13 05:08:36.232906','2','2',2,'[]',14,1),(8,'2021-06-13 05:13:29.399545','1','1',1,'[{\"added\": {}}]',8,1),(9,'2021-06-13 05:14:04.926250','1','1',1,'[{\"added\": {}}]',7,1),(10,'2021-06-14 09:19:12.046059','1','1',1,'[{\"added\": {}}]',16,1),(11,'2021-06-14 09:22:58.241893','1','1',2,'[{\"changed\": {\"fields\": [\"Status\"]}}]',16,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'apis','bankmodel'),(10,'apis','chargemodel'),(8,'apis','clientmodel'),(11,'apis','featuremodel'),(15,'apis','iphittingrecordmodel'),(16,'apis','ipwhitelistedmodel'),(9,'apis','ledgermodel'),(12,'apis','modemodel'),(13,'apis','rolefeaturemodel'),(14,'apis','rolemodel'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-06-11 06:25:53.350427'),(2,'auth','0001_initial','2021-06-11 06:26:20.366214'),(3,'admin','0001_initial','2021-06-11 06:26:25.639473'),(4,'admin','0002_logentry_remove_auto_add','2021-06-11 06:26:25.712414'),(5,'admin','0003_logentry_add_action_flag_choices','2021-06-11 06:26:25.804546'),(6,'apis','0001_initial','2021-06-11 06:26:26.683929'),(7,'apis','0002_auto_20210611_1004','2021-06-11 06:26:28.175049'),(8,'apis','0003_auto_20210611_1112','2021-06-11 06:26:37.945989'),(9,'contenttypes','0002_remove_content_type_name','2021-06-11 06:33:12.109642'),(10,'auth','0002_alter_permission_name_max_length','2021-06-11 06:33:13.765826'),(11,'auth','0003_alter_user_email_max_length','2021-06-11 06:33:14.621242'),(12,'auth','0004_alter_user_username_opts','2021-06-11 06:33:14.680254'),(13,'auth','0005_alter_user_last_login_null','2021-06-11 06:33:16.551781'),(14,'auth','0006_require_contenttypes_0002','2021-06-11 06:33:16.621072'),(15,'auth','0007_alter_validators_add_error_messages','2021-06-11 06:33:16.694274'),(16,'auth','0008_alter_user_username_max_length','2021-06-11 06:33:18.589925'),(17,'auth','0009_alter_user_last_name_max_length','2021-06-11 06:33:20.745374'),(18,'auth','0010_alter_group_name_max_length','2021-06-11 06:33:21.096738'),(19,'auth','0011_update_proxy_permissions','2021-06-11 06:33:21.169762'),(20,'auth','0012_alter_user_first_name_max_length','2021-06-11 06:33:23.627852'),(21,'sessions','0001_initial','2021-06-11 06:33:24.792886'),(22,'apis','0002_auto_20210612_1115','2021-06-12 05:46:06.151805'),(23,'apis','0003_auto_20210613_1025','2021-06-13 04:55:34.098619'),(24,'apis','0004_auto_20210613_1037','2021-06-13 05:07:30.227974'),(25,'apis','0005_remove_ledgermodel_trans_time','2021-06-13 05:25:18.313768'),(26,'apis','0006_ledgermodel_trans_time','2021-06-13 05:26:18.407943'),(27,'apis','0007_ledgermodel_van','2021-06-13 05:35:12.425313'),(28,'apis','0008_alter_ledgermodel_trans_status','2021-06-14 04:29:26.799352'),(29,'apis','0009_iphittingrecordmodel_ipwhitelistedmodel','2021-06-14 09:14:23.405534'),(30,'apis','0010_auto_20210614_1602','2021-06-14 10:33:06.845014'),(31,'apis','0011_auto_20210622_1116','2021-06-22 05:48:44.339489');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('o2vj0ozb8cljrylqbibum0nkoyo0z1qj','.eJxVjEEOwiAQRe_C2hBgBiku3fcMBIZBqoYmpV0Z765NutDtf-_9lwhxW2vYOi9hyuIitDj9binSg9sO8j222yxpbusyJbkr8qBdjnPm5_Vw_w5q7PVbk2I_WGsVlAxAmE3CmDQyeFLgNaoIhiAzOE3qnFwBb3AoxThU1rN4fwDRXDc2:1lsIUQ:OK3lfJCUhLwULuGbjo8-nMdj5PK1VyzTkeYy7Gg3ORE','2021-06-27 05:16:54.047847');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-22 11:26:29
