-- MariaDB dump 10.19  Distrib 10.6.4-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: spe_system
-- ------------------------------------------------------
-- Server version	10.6.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alert`
--

DROP TABLE IF EXISTS `alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alert` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` varchar(1200) NOT NULL,
  `date_sent` datetime(6) NOT NULL,
  `resolved` tinyint(1) NOT NULL,
  `coordinator_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `alert_coordinator_id_d2db111d_fk_coordinator_id` (`coordinator_id`),
  KEY `alert_student_id_dfc042f5_fk_student_id` (`student_id`),
  CONSTRAINT `alert_coordinator_id_d2db111d_fk_coordinator_id` FOREIGN KEY (`coordinator_id`) REFERENCES `coordinator` (`id`),
  CONSTRAINT `alert_student_id_dfc042f5_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert`
--

LOCK TABLES `alert` WRITE;
/*!40000 ALTER TABLE `alert` DISABLE KEYS */;
/*!40000 ALTER TABLE `alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add alert',6,'add_alert'),(22,'Can change alert',6,'change_alert'),(23,'Can delete alert',6,'delete_alert'),(24,'Can view alert',6,'view_alert'),(25,'Can add coordinator',7,'add_coordinator'),(26,'Can change coordinator',7,'change_coordinator'),(27,'Can delete coordinator',7,'delete_coordinator'),(28,'Can view coordinator',7,'view_coordinator'),(29,'Can add report',8,'add_report'),(30,'Can change report',8,'change_report'),(31,'Can delete report',8,'delete_report'),(32,'Can view report',8,'view_report'),(33,'Can add student_ report',9,'add_student_report'),(34,'Can change student_ report',9,'change_student_report'),(35,'Can delete student_ report',9,'delete_student_report'),(36,'Can view student_ report',9,'view_student_report'),(37,'Can add user',10,'add_user'),(38,'Can change user',10,'change_user'),(39,'Can delete user',10,'delete_user'),(40,'Can view user',10,'view_user'),(41,'Can add form',11,'add_form'),(42,'Can change form',11,'change_form'),(43,'Can delete form',11,'delete_form'),(44,'Can view form',11,'view_form'),(45,'Can add question_ repository',12,'add_question_repository'),(46,'Can change question_ repository',12,'change_question_repository'),(47,'Can delete question_ repository',12,'delete_question_repository'),(48,'Can view question_ repository',12,'view_question_repository'),(49,'Can add question_ form',13,'add_question_form'),(50,'Can change question_ form',13,'change_question_form'),(51,'Can delete question_ form',13,'delete_question_form'),(52,'Can view question_ form',13,'view_question_form'),(53,'Can add campus',14,'add_campus'),(54,'Can change campus',14,'change_campus'),(55,'Can delete campus',14,'delete_campus'),(56,'Can view campus',14,'view_campus'),(57,'Can add offering',15,'add_offering'),(58,'Can change offering',15,'change_offering'),(59,'Can delete offering',15,'delete_offering'),(60,'Can view offering',15,'view_offering'),(61,'Can add enrolment',16,'add_enrolment'),(62,'Can change enrolment',16,'change_enrolment'),(63,'Can delete enrolment',16,'delete_enrolment'),(64,'Can view enrolment',16,'view_enrolment'),(65,'Can add student',17,'add_student'),(66,'Can change student',17,'change_student'),(67,'Can delete student',17,'delete_student'),(68,'Can view student',17,'view_student'),(69,'Can add file',18,'add_file'),(70,'Can change file',18,'change_file'),(71,'Can delete file',18,'delete_file'),(72,'Can view file',18,'view_file'),(73,'Can add evaluation',19,'add_evaluation'),(74,'Can change evaluation',19,'change_evaluation'),(75,'Can delete evaluation',19,'delete_evaluation'),(76,'Can view evaluation',19,'view_evaluation'),(77,'Can add submission',20,'add_submission'),(78,'Can change submission',20,'change_submission'),(79,'Can delete submission',20,'delete_submission'),(80,'Can view submission',20,'view_submission'),(81,'Can add submitted_ evaluation',21,'add_submitted_evaluation'),(82,'Can change submitted_ evaluation',21,'change_submitted_evaluation'),(83,'Can delete submitted_ evaluation',21,'delete_submitted_evaluation'),(84,'Can view submitted_ evaluation',21,'view_submitted_evaluation'),(85,'Can add rating',22,'add_rating'),(86,'Can change rating',22,'change_rating'),(87,'Can delete rating',22,'delete_rating'),(88,'Can view rating',22,'view_rating'),(89,'Can add comment',23,'add_comment'),(90,'Can change comment',23,'change_comment'),(91,'Can delete comment',23,'delete_comment'),(92,'Can view comment',23,'view_comment'),(93,'Can add team',24,'add_team'),(94,'Can change team',24,'change_team'),(95,'Can delete team',24,'delete_team'),(96,'Can view team',24,'view_team'),(97,'Can add student_ team',25,'add_student_team'),(98,'Can change student_ team',25,'change_student_team'),(99,'Can delete student_ team',25,'delete_student_team'),(100,'Can view student_ team',25,'view_student_team'),(101,'Can add evaluation_ submission',21,'add_evaluation_submission'),(102,'Can change evaluation_ submission',21,'change_evaluation_submission'),(103,'Can delete evaluation_ submission',21,'delete_evaluation_submission'),(104,'Can view evaluation_ submission',21,'view_evaluation_submission');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus`
--

DROP TABLE IF EXISTS `campus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campus` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `city` varchar(20) NOT NULL,
  `country` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus`
--

LOCK TABLES `campus` WRITE;
/*!40000 ALTER TABLE `campus` DISABLE KEYS */;
/*!40000 ALTER TABLE `campus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `answer` varchar(1200) NOT NULL,
  `evaluation_id` bigint(20) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_evaluation_id_947a970f_fk_evaluation_id` (`evaluation_id`),
  KEY `comment_question_id_a75a52fe_fk_question_repository_id` (`question_id`),
  CONSTRAINT `comment_evaluation_id_947a970f_fk_evaluation_id` FOREIGN KEY (`evaluation_id`) REFERENCES `evaluation` (`id`),
  CONSTRAINT `comment_question_id_a75a52fe_fk_question_repository_id` FOREIGN KEY (`question_id`) REFERENCES `question_repository` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordinator`
--

DROP TABLE IF EXISTS `coordinator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coordinator` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(4) NOT NULL,
  `given_names` varchar(60) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `coordinator_user_id_9d80d332_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordinator`
--

LOCK TABLES `coordinator` WRITE;
/*!40000 ALTER TABLE `coordinator` DISABLE KEYS */;
/*!40000 ALTER TABLE `coordinator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user`
--

DROP TABLE IF EXISTS `custom_user_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user`
--

LOCK TABLES `custom_user_user` WRITE;
/*!40000 ALTER TABLE `custom_user_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_user_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user_groups`
--

DROP TABLE IF EXISTS `custom_user_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `custom_user_user_groups_user_id_group_id_fc2104d2_uniq` (`user_id`,`group_id`),
  KEY `custom_user_user_groups_group_id_dfde52bf_fk_auth_group_id` (`group_id`),
  CONSTRAINT `custom_user_user_groups_group_id_dfde52bf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `custom_user_user_groups_user_id_f1071bc9_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user_groups`
--

LOCK TABLES `custom_user_user_groups` WRITE;
/*!40000 ALTER TABLE `custom_user_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_user_user_user_permissions`
--

DROP TABLE IF EXISTS `custom_user_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custom_user_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `custom_user_user_user_pe_user_id_permission_id_2215a086_uniq` (`user_id`,`permission_id`),
  KEY `custom_user_user_use_permission_id_cb2d2b0f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `custom_user_user_use_permission_id_cb2d2b0f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `custom_user_user_use_user_id_65556ab9_fk_custom_us` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_user_user_user_permissions`
--

LOCK TABLES `custom_user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `custom_user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `custom_user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_custom_user_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(6,'alert','alert'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'coordinator','coordinator'),(8,'coordinator','report'),(9,'coordinator','student_report'),(10,'custom_user','user'),(11,'form','form'),(13,'form','question_form'),(12,'form','question_repository'),(14,'offering','campus'),(16,'offering','enrolment'),(15,'offering','offering'),(5,'sessions','session'),(18,'student','file'),(17,'student','student'),(23,'submission','comment'),(19,'submission','evaluation'),(21,'submission','evaluation_submission'),(22,'submission','rating'),(20,'submission','submission'),(25,'team','student_team'),(24,'team','team');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-10-31 22:01:41.413436'),(2,'contenttypes','0002_remove_content_type_name','2021-10-31 22:01:41.515931'),(3,'auth','0001_initial','2021-10-31 22:01:41.881213'),(4,'auth','0002_alter_permission_name_max_length','2021-10-31 22:01:41.927808'),(5,'auth','0003_alter_user_email_max_length','2021-10-31 22:01:41.943875'),(6,'auth','0004_alter_user_username_opts','2021-10-31 22:01:41.976791'),(7,'auth','0005_alter_user_last_login_null','2021-10-31 22:01:41.993957'),(8,'auth','0006_require_contenttypes_0002','2021-10-31 22:01:41.999731'),(9,'auth','0007_alter_validators_add_error_messages','2021-10-31 22:01:42.011520'),(10,'auth','0008_alter_user_username_max_length','2021-10-31 22:01:42.030366'),(11,'auth','0009_alter_user_last_name_max_length','2021-10-31 22:01:42.060102'),(12,'auth','0010_alter_group_name_max_length','2021-10-31 22:01:42.109424'),(13,'auth','0011_update_proxy_permissions','2021-10-31 22:01:42.129030'),(14,'auth','0012_alter_user_first_name_max_length','2021-10-31 22:01:42.148852'),(15,'custom_user','0001_initial','2021-10-31 22:01:42.584059'),(16,'admin','0001_initial','2021-10-31 22:01:42.772497'),(17,'admin','0002_logentry_remove_auto_add','2021-10-31 22:01:42.810022'),(18,'admin','0003_logentry_add_action_flag_choices','2021-10-31 22:01:42.826923'),(19,'student','0001_initial','2021-10-31 22:01:43.079049'),(20,'coordinator','0001_initial','2021-10-31 22:01:43.271428'),(21,'alert','0001_initial','2021-10-31 22:01:43.321744'),(22,'alert','0002_alert_coordinator_id','2021-10-31 22:01:43.396793'),(23,'alert','0003_alert_student_id','2021-10-31 22:01:43.501809'),(24,'coordinator','0002_initial','2021-10-31 22:01:43.795972'),(25,'form','0001_initial','2021-10-31 22:01:44.190033'),(26,'offering','0001_initial','2021-10-31 22:01:44.572370'),(27,'sessions','0001_initial','2021-10-31 22:01:44.665858'),(28,'submission','0001_initial','2021-10-31 22:01:45.545589'),(29,'team','0001_initial','2021-10-31 22:01:45.938690'),(30,'alert','0004_auto_20211101_0207','2021-10-31 22:08:13.692189'),(31,'coordinator','0003_auto_20211101_0207','2021-10-31 22:08:14.305023'),(32,'form','0002_auto_20211101_0207','2021-10-31 22:08:14.917051'),(33,'offering','0002_auto_20211101_0207','2021-10-31 22:08:15.529203'),(34,'student','0002_rename_student_id_file_student','2021-10-31 22:08:15.719451'),(35,'submission','0002_auto_20211101_0207','2021-10-31 22:08:17.306228'),(36,'team','0002_auto_20211101_0207','2021-10-31 22:08:17.876080'),(37,'submission','0003_auto_20211101_0209','2021-10-31 22:09:08.117995');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolment`
--

DROP TABLE IF EXISTS `enrolment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrolment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `offering_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `enrolment_offering_id_b0b498a9_fk_offering_id` (`offering_id`),
  KEY `enrolment_student_id_f9402bdb_fk_student_id` (`student_id`),
  CONSTRAINT `enrolment_offering_id_b0b498a9_fk_offering_id` FOREIGN KEY (`offering_id`) REFERENCES `offering` (`id`),
  CONSTRAINT `enrolment_student_id_f9402bdb_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolment`
--

LOCK TABLES `enrolment` WRITE;
/*!40000 ALTER TABLE `enrolment` DISABLE KEYS */;
/*!40000 ALTER TABLE `enrolment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS `evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evaluatee_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluation_evaluatee_id_7e9418fd_fk_student_id` (`evaluatee_id`),
  KEY `evaluation_student_id_8a24dfae_fk_student_id` (`student_id`),
  CONSTRAINT `evaluation_evaluatee_id_7e9418fd_fk_student_id` FOREIGN KEY (`evaluatee_id`) REFERENCES `student` (`id`),
  CONSTRAINT `evaluation_student_id_8a24dfae_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation`
--

LOCK TABLES `evaluation` WRITE;
/*!40000 ALTER TABLE `evaluation` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation_submission`
--

DROP TABLE IF EXISTS `evaluation_submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluation_submission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evaluation_id` bigint(20) NOT NULL,
  `submission_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `submitted_evaluation_evaluation_id_0acdce33_fk_evaluation_id` (`evaluation_id`),
  KEY `submitted_evaluation_submission_id_387aa503_fk_submission_id` (`submission_id`),
  CONSTRAINT `submitted_evaluation_evaluation_id_0acdce33_fk_evaluation_id` FOREIGN KEY (`evaluation_id`) REFERENCES `evaluation` (`id`),
  CONSTRAINT `submitted_evaluation_submission_id_387aa503_fk_submission_id` FOREIGN KEY (`submission_id`) REFERENCES `submission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation_submission`
--

LOCK TABLES `evaluation_submission` WRITE;
/*!40000 ALTER TABLE `evaluation_submission` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluation_submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `file` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(12) NOT NULL,
  `path` varchar(100) NOT NULL,
  `date_uploaded` datetime(6) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `file_student_id_ba7ee8e1_fk_student_id` (`student_id`),
  CONSTRAINT `file_student_id_ba7ee8e1_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file`
--

LOCK TABLES `file` WRITE;
/*!40000 ALTER TABLE `file` DISABLE KEYS */;
/*!40000 ALTER TABLE `file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `form`
--

DROP TABLE IF EXISTS `form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `form` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `spe_number` smallint(5) unsigned NOT NULL CHECK (`spe_number` >= 0),
  `introductory_text` varchar(1600) NOT NULL,
  `date_opened` datetime(6) NOT NULL,
  `date_closed` datetime(6) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_modified` datetime(6) NOT NULL,
  `coordinator_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `form_coordinator_id_cca28055_fk_coordinator_id` (`coordinator_id`),
  CONSTRAINT `form_coordinator_id_cca28055_fk_coordinator_id` FOREIGN KEY (`coordinator_id`) REFERENCES `coordinator` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `form`
--

LOCK TABLES `form` WRITE;
/*!40000 ALTER TABLE `form` DISABLE KEYS */;
/*!40000 ALTER TABLE `form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offering`
--

DROP TABLE IF EXISTS `offering`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offering` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `unit_id` varchar(6) NOT NULL,
  `teaching_period` varchar(3) NOT NULL,
  `year` smallint(5) unsigned NOT NULL CHECK (`year` >= 0),
  `lecturer_title` varchar(4) NOT NULL,
  `lecturer_given_names` varchar(60) NOT NULL,
  `lecturer_last_name` varchar(30) NOT NULL,
  `campus_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `offering_campus_id_35a1096b_fk_campus_id` (`campus_id`),
  CONSTRAINT `offering_campus_id_35a1096b_fk_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offering`
--

LOCK TABLES `offering` WRITE;
/*!40000 ALTER TABLE `offering` DISABLE KEYS */;
/*!40000 ALTER TABLE `offering` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_form`
--

DROP TABLE IF EXISTS `question_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_form` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `form_id` bigint(20) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_form_form_id_0cb72816_fk_form_id` (`form_id`),
  KEY `question_form_question_id_4dcd7f21_fk_question_repository_id` (`question_id`),
  CONSTRAINT `question_form_form_id_0cb72816_fk_form_id` FOREIGN KEY (`form_id`) REFERENCES `form` (`id`),
  CONSTRAINT `question_form_question_id_4dcd7f21_fk_question_repository_id` FOREIGN KEY (`question_id`) REFERENCES `question_repository` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_form`
--

LOCK TABLES `question_form` WRITE;
/*!40000 ALTER TABLE `question_form` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_repository`
--

DROP TABLE IF EXISTS `question_repository`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question_repository` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `prompt` varchar(300) NOT NULL,
  `weighting` decimal(4,2) NOT NULL,
  `question_type` varchar(7) NOT NULL,
  `evaluation_type` varchar(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_repository`
--

LOCK TABLES `question_repository` WRITE;
/*!40000 ALTER TABLE `question_repository` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_repository` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rating` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `answer` smallint(5) unsigned NOT NULL CHECK (`answer` >= 0),
  `evaluation_id` bigint(20) NOT NULL,
  `question_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rating_evaluation_id_1312365a_fk_evaluation_id` (`evaluation_id`),
  KEY `rating_question_id_782ecbbc_fk_question_repository_id` (`question_id`),
  CONSTRAINT `rating_evaluation_id_1312365a_fk_evaluation_id` FOREIGN KEY (`evaluation_id`) REFERENCES `evaluation` (`id`),
  CONSTRAINT `rating_question_id_782ecbbc_fk_question_repository_id` FOREIGN KEY (`question_id`) REFERENCES `question_repository` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating`
--

LOCK TABLES `rating` WRITE;
/*!40000 ALTER TABLE `rating` DISABLE KEYS */;
/*!40000 ALTER TABLE `rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `coordinator_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_coordinator_id_2e4b1fcc_fk_coordinator_id` (`coordinator_id`),
  CONSTRAINT `report_coordinator_id_2e4b1fcc_fk_coordinator_id` FOREIGN KEY (`coordinator_id`) REFERENCES `coordinator` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_number` varchar(8) NOT NULL,
  `title` varchar(4) NOT NULL,
  `given_names` varchar(60) NOT NULL,
  `spe1` decimal(4,2) NOT NULL,
  `spe2` decimal(4,2) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `student_user_id_dcc2526f_fk_custom_user_user_id` FOREIGN KEY (`user_id`) REFERENCES `custom_user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_report`
--

DROP TABLE IF EXISTS `student_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `report_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_report_report_id_a4b377f6_fk_report_id` (`report_id`),
  KEY `student_report_student_id_5801abf0_fk_student_id` (`student_id`),
  CONSTRAINT `student_report_report_id_a4b377f6_fk_report_id` FOREIGN KEY (`report_id`) REFERENCES `report` (`id`),
  CONSTRAINT `student_report_student_id_5801abf0_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_report`
--

LOCK TABLES `student_report` WRITE;
/*!40000 ALTER TABLE `student_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_team`
--

DROP TABLE IF EXISTS `student_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student_team` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `student_id` bigint(20) NOT NULL,
  `team_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_team_student_id_abd4af78_fk_student_id` (`student_id`),
  KEY `student_team_team_id_570f26ca_fk_team_id` (`team_id`),
  CONSTRAINT `student_team_student_id_abd4af78_fk_student_id` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `student_team_team_id_570f26ca_fk_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_team`
--

LOCK TABLES `student_team` WRITE;
/*!40000 ALTER TABLE `student_team` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date_submitted` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

LOCK TABLES `submission` WRITE;
/*!40000 ALTER TABLE `submission` DISABLE KEYS */;
/*!40000 ALTER TABLE `submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(20) NOT NULL,
  `campus_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `team_campus_id_c7cf7d2b_fk_campus_id` (`campus_id`),
  CONSTRAINT `team_campus_id_c7cf7d2b_fk_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-01  2:23:57
