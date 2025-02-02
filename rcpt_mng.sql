CREATE DATABASE  IF NOT EXISTS `rcpt_mng1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `rcpt_mng1`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: rcpt_mng1
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(255) DEFAULT NULL,
  `c_surname` varchar(255) DEFAULT NULL,
  `c_password` int DEFAULT '123',
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'ali','ctk',123),(2,'veli','ctk',123),(3,'kemal','ctk',123),(4,'hasan','ctk',123),(5,'hikmet','ctk',123);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `p_total_price`
--

DROP TABLE IF EXISTS `p_total_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `p_total_price` (
  `p_id` int NOT NULL AUTO_INCREMENT,
  `c_id` int DEFAULT NULL,
  `r_id` int DEFAULT NULL,
  `p_date` timestamp NULL DEFAULT NULL,
  `p_total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  KEY `r_id` (`r_id`),
  CONSTRAINT `p_total_price_ibfk_1` FOREIGN KEY (`r_id`) REFERENCES `receipt_header` (`all_receipt_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `p_total_price`
--

LOCK TABLES `p_total_price` WRITE;
/*!40000 ALTER TABLE `p_total_price` DISABLE KEYS */;
/*!40000 ALTER TABLE `p_total_price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_header`
--

DROP TABLE IF EXISTS `receipt_header`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_header` (
  `all_receipt_id` int NOT NULL AUTO_INCREMENT,
  `c_id` int DEFAULT NULL,
  `r_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`all_receipt_id`),
  KEY `c_id` (`c_id`),
  CONSTRAINT `receipt_header_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `customer` (`c_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_header`
--

LOCK TABLES `receipt_header` WRITE;
/*!40000 ALTER TABLE `receipt_header` DISABLE KEYS */;
INSERT INTO `receipt_header` VALUES (1,1,'2025-01-26 09:37:22'),(2,1,'2025-02-01 08:39:41'),(3,1,'2025-02-01 08:42:02'),(4,1,'2025-02-01 09:08:41'),(5,1,'2025-02-01 09:39:47'),(6,1,'2025-02-01 12:48:04'),(7,1,'2025-02-01 16:43:47'),(8,1,'2025-02-02 00:17:28'),(9,1,'2025-02-02 00:19:11'),(10,1,'2025-02-02 00:24:56');
/*!40000 ALTER TABLE `receipt_header` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_items`
--

DROP TABLE IF EXISTS `receipt_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_items` (
  `c_id` int DEFAULT NULL,
  `r_id` int DEFAULT NULL,
  `r_item_name` varchar(255) DEFAULT NULL,
  `r_quantity` int DEFAULT NULL,
  `r_price` decimal(10,2) DEFAULT NULL,
  KEY `c_id` (`c_id`),
  CONSTRAINT `receipt_items_ibfk_1` FOREIGN KEY (`c_id`) REFERENCES `receipt_header` (`all_receipt_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_items`
--

LOCK TABLES `receipt_items` WRITE;
/*!40000 ALTER TABLE `receipt_items` DISABLE KEYS */;
INSERT INTO `receipt_items` VALUES (1,1,'SENPILIC TAVUK POSET',4,298.70),(1,1,'TANEM ITHAL K.MERCIM',1,38.50),(1,1,'TAT MAYONEZ 550GR',1,74.95),(1,1,'MARKET POSETI BATTAL',1,0.25),(1,2,'SOMUN BIFTEK TANTUNI',1,80.00),(1,2,'ET-CIGER KARISIK',2,360.00),(1,2,'(BB) KOFTE PORSIYON',1,240.00),(1,2,'BUYUK AYRAN',1,20.00),(1,2,'ACIK AYRAN',5,100.00),(1,2,'SU',5,35.00),(1,2,'KOFTE MENU',1,185.00),(1,3,'SENPILIC TAVUK POSET',4,298.70),(1,3,'TANEM ITHAL K.MERCIM',1,38.50),(1,3,'TAT MAYONEZ 550GR',1,74.95),(1,3,'MARKET POSETI BATTAL',1,0.25),(1,4,'YUMURTA 15Lİ L',1,9.95),(1,4,'KARADEM FİLİZ500G',1,11.90),(1,4,'KEYFE 100 G',1,4.50),(1,4,'YUDUM A. YAĞ 1,25L',1,21.95),(1,4,'MAK.SPAGETTI',1,2.95),(1,4,'MAKARNA BURGU',1,2.95),(1,4,'UN BUĞDAY2KGYGNLR',1,6.95),(1,4,'MBİR VAK. XS 500G',1,13.75),(1,4,'BOZBEYİ 600G B.PEYNR',1,21.95),(1,4,'BİRŞAH 1 L YAĞLI SÜT',1,3.75),(1,5,'SOMUN BIFTEK TANTUNI',1,80.00),(1,5,'ET-CIGER KARISIK',2,360.00),(1,5,'(BB) KOFTE PORSIYON',1,240.00),(1,5,'BUYUK AYRAN',1,20.00),(1,5,'ACIK AYRAN',5,100.00),(1,5,'SU',5,35.00),(1,5,'KOFTE MENU',1,185.00),(1,6,'Orange Juice',1,2.15),(1,6,'Apples',1,3.50),(1,6,'Tomato',1,2.40),(1,6,'Fish',1,6.99),(1,6,'Beef',1,10.00),(1,6,'Onion',1,1.25),(1,6,'Cheese',1,3.40),(1,7,'SOMUN BIFTEK TANTUNI',1,80.00),(1,7,'ET-CIGER KARISIK',2,360.00),(1,7,'(BB) KOFTE PORSIYON',1,240.00),(1,7,'BUYUK AYRAN',1,20.00),(1,7,'ACIK AYRAN',5,100.00),(1,7,'SU',5,35.00),(1,7,'KOFTE MENU',1,185.00),(1,8,'GRILL COVER',1,14.97),(1,8,'FIBER CHOICE',1,12.94),(1,8,'CELERY HEART',1,2.48),(1,8,'RED GRAPE',3,3.61),(1,9,'OZMO FUN FİGÜRLÜ 23G',1,13.50),(1,9,'7-24 NAMET DANA MACA',1,27.90),(1,9,'OZMO FUN FİGÜRLÜ 23G',1,13.50),(1,9,'TADPİ PİLİÇ BAGET KG',1,102.27),(1,9,'FINISH QUANTUM ÖZEL',1,259.00),(1,9,'25TLFINISH110TL',1,149.00),(1,9,'FINISH QUANTUM ÖZEL',1,259.00),(1,9,'25TLFINISH110TL',1,149.00),(1,9,'ARKO DEĞERLİ YAĞLAR',1,104.50),(1,9,'25TLARK050TL',1,54.50),(1,9,'ALIŞVERİŞ POŞETİ 43',1,0.25),(1,10,'SENPILIC TAVUK POSET',4,298.70),(1,10,'TANEM ITHAL K.MERCIM',1,38.50),(1,10,'TAT MAYONEZ 550GR',1,74.95),(1,10,'MARKET POSETI BATTAL',1,0.25);
/*!40000 ALTER TABLE `receipt_items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-02 12:54:56
