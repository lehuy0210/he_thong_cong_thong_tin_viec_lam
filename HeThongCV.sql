-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: hethongcv
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('xxxx');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cong_ty`
--

DROP TABLE IF EXISTS `cong_ty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cong_ty` (
  `ma_cong_ty` int NOT NULL AUTO_INCREMENT,
  `ten_cong_ty` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_so_thue` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mo_ta` text COLLATE utf8mb4_unicode_ci,
  `dia_chi` text COLLATE utf8mb4_unicode_ci,
  `ma_nha_tuyen_dung` int NOT NULL,
  PRIMARY KEY (`ma_cong_ty`),
  UNIQUE KEY `ma_nha_tuyen_dung` (`ma_nha_tuyen_dung`),
  UNIQUE KEY `ma_so_thue` (`ma_so_thue`),
  CONSTRAINT `cong_ty_ibfk_1` FOREIGN KEY (`ma_nha_tuyen_dung`) REFERENCES `nha_tuyen_dung` (`ma_nha_tuyen_dung`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cong_ty`
--

LOCK TABLES `cong_ty` WRITE;
/*!40000 ALTER TABLE `cong_ty` DISABLE KEYS */;
/*!40000 ALTER TABLE `cong_ty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cv`
--

DROP TABLE IF EXISTS `cv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cv` (
  `ma_cv` int NOT NULL AUTO_INCREMENT,
  `ten_cv` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ten_file` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hoc_van` text COLLATE utf8mb4_unicode_ci,
  `kinh_nghiem_lam_viec` text COLLATE utf8mb4_unicode_ci,
  `ma_ung_vien` int NOT NULL,
  PRIMARY KEY (`ma_cv`),
  KEY `ma_ung_vien` (`ma_ung_vien`),
  CONSTRAINT `cv_ibfk_1` FOREIGN KEY (`ma_ung_vien`) REFERENCES `ung_vien` (`ma_ung_vien`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cv`
--

LOCK TABLES `cv` WRITE;
/*!40000 ALTER TABLE `cv` DISABLE KEYS */;
/*!40000 ALTER TABLE `cv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cv_ky_nang`
--

DROP TABLE IF EXISTS `cv_ky_nang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cv_ky_nang` (
  `ma_cv` int NOT NULL,
  `ma_ky_nang` int NOT NULL,
  PRIMARY KEY (`ma_cv`,`ma_ky_nang`),
  KEY `ma_ky_nang` (`ma_ky_nang`),
  CONSTRAINT `cv_ky_nang_ibfk_1` FOREIGN KEY (`ma_cv`) REFERENCES `cv` (`ma_cv`) ON DELETE CASCADE,
  CONSTRAINT `cv_ky_nang_ibfk_2` FOREIGN KEY (`ma_ky_nang`) REFERENCES `ky_nang` (`ma_ky_nang`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cv_ky_nang`
--

LOCK TABLES `cv_ky_nang` WRITE;
/*!40000 ALTER TABLE `cv_ky_nang` DISABLE KEYS */;
/*!40000 ALTER TABLE `cv_ky_nang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ho_so_ung_tuyen`
--

DROP TABLE IF EXISTS `ho_so_ung_tuyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ho_so_ung_tuyen` (
  `ma_ho_so` int NOT NULL AUTO_INCREMENT,
  `trang_thai` enum('Chờ duyệt','Đã duyệt','Từ chối') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ngay_nop` datetime DEFAULT NULL,
  `ma_ung_vien` int NOT NULL,
  `tin_id` int NOT NULL,
  `ma_cv` int NOT NULL,
  PRIMARY KEY (`ma_ho_so`),
  KEY `ma_cv` (`ma_cv`),
  KEY `tin_id` (`tin_id`),
  KEY `ma_ung_vien` (`ma_ung_vien`),
  CONSTRAINT `ho_so_ung_tuyen_ibfk_1` FOREIGN KEY (`ma_cv`) REFERENCES `cv` (`ma_cv`) ON DELETE CASCADE,
  CONSTRAINT `ho_so_ung_tuyen_ibfk_2` FOREIGN KEY (`tin_id`) REFERENCES `tin_tuyen_dung` (`tin_id`) ON DELETE CASCADE,
  CONSTRAINT `ho_so_ung_tuyen_ibfk_3` FOREIGN KEY (`ma_ung_vien`) REFERENCES `ung_vien` (`ma_ung_vien`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ho_so_ung_tuyen`
--

LOCK TABLES `ho_so_ung_tuyen` WRITE;
/*!40000 ALTER TABLE `ho_so_ung_tuyen` DISABLE KEYS */;
/*!40000 ALTER TABLE `ho_so_ung_tuyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ky_nang`
--

DROP TABLE IF EXISTS `ky_nang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ky_nang` (
  `ma_ky_nang` int NOT NULL AUTO_INCREMENT,
  `ten_ky_nang` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`ma_ky_nang`),
  UNIQUE KEY `ten_ky_nang` (`ten_ky_nang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ky_nang`
--

LOCK TABLES `ky_nang` WRITE;
/*!40000 ALTER TABLE `ky_nang` DISABLE KEYS */;
/*!40000 ALTER TABLE `ky_nang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nguoi_dung`
--

DROP TABLE IF EXISTS `nguoi_dung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nguoi_dung` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `vai_tro` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ho_ten` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ngay_sinh` date DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gioi_tinh` enum('Nam','Nữ','Khác') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `so_dien_thoai` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dia_chi` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nguoi_dung`
--

LOCK TABLES `nguoi_dung` WRITE;
/*!40000 ALTER TABLE `nguoi_dung` DISABLE KEYS */;
/*!40000 ALTER TABLE `nguoi_dung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nha_tuyen_dung`
--

DROP TABLE IF EXISTS `nha_tuyen_dung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nha_tuyen_dung` (
  `ma_nha_tuyen_dung` int NOT NULL,
  PRIMARY KEY (`ma_nha_tuyen_dung`),
  CONSTRAINT `nha_tuyen_dung_ibfk_1` FOREIGN KEY (`ma_nha_tuyen_dung`) REFERENCES `nguoi_dung` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nha_tuyen_dung`
--

LOCK TABLES `nha_tuyen_dung` WRITE;
/*!40000 ALTER TABLE `nha_tuyen_dung` DISABLE KEYS */;
/*!40000 ALTER TABLE `nha_tuyen_dung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quan_tri`
--

DROP TABLE IF EXISTS `quan_tri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quan_tri` (
  `ma_quan_tri` int NOT NULL,
  PRIMARY KEY (`ma_quan_tri`),
  CONSTRAINT `quan_tri_ibfk_1` FOREIGN KEY (`ma_quan_tri`) REFERENCES `nguoi_dung` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quan_tri`
--

LOCK TABLES `quan_tri` WRITE;
/*!40000 ALTER TABLE `quan_tri` DISABLE KEYS */;
/*!40000 ALTER TABLE `quan_tri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tin_tuyen_dung`
--

DROP TABLE IF EXISTS `tin_tuyen_dung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tin_tuyen_dung` (
  `tin_id` int NOT NULL AUTO_INCREMENT,
  `tieu_de` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mo_ta` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `trang_thai` enum('Đang mở','Đã đóng') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `han_nop` date NOT NULL,
  `luong` int DEFAULT NULL,
  `quyen_loi` text COLLATE utf8mb4_unicode_ci,
  `ma_nha_tuyen_dung` int NOT NULL,
  PRIMARY KEY (`tin_id`),
  KEY `ma_nha_tuyen_dung` (`ma_nha_tuyen_dung`),
  CONSTRAINT `tin_tuyen_dung_ibfk_1` FOREIGN KEY (`ma_nha_tuyen_dung`) REFERENCES `nha_tuyen_dung` (`ma_nha_tuyen_dung`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tin_tuyen_dung`
--

LOCK TABLES `tin_tuyen_dung` WRITE;
/*!40000 ALTER TABLE `tin_tuyen_dung` DISABLE KEYS */;
/*!40000 ALTER TABLE `tin_tuyen_dung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tin_tuyen_dung_ky_nang`
--

DROP TABLE IF EXISTS `tin_tuyen_dung_ky_nang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tin_tuyen_dung_ky_nang` (
  `tin_id` int NOT NULL,
  `ma_ky_nang` int NOT NULL,
  PRIMARY KEY (`tin_id`,`ma_ky_nang`),
  KEY `ma_ky_nang` (`ma_ky_nang`),
  CONSTRAINT `tin_tuyen_dung_ky_nang_ibfk_1` FOREIGN KEY (`ma_ky_nang`) REFERENCES `ky_nang` (`ma_ky_nang`) ON DELETE CASCADE,
  CONSTRAINT `tin_tuyen_dung_ky_nang_ibfk_2` FOREIGN KEY (`tin_id`) REFERENCES `tin_tuyen_dung` (`tin_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tin_tuyen_dung_ky_nang`
--

LOCK TABLES `tin_tuyen_dung_ky_nang` WRITE;
/*!40000 ALTER TABLE `tin_tuyen_dung_ky_nang` DISABLE KEYS */;
/*!40000 ALTER TABLE `tin_tuyen_dung_ky_nang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ung_vien`
--

DROP TABLE IF EXISTS `ung_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ung_vien` (
  `ma_ung_vien` int NOT NULL,
  PRIMARY KEY (`ma_ung_vien`),
  CONSTRAINT `ung_vien_ibfk_1` FOREIGN KEY (`ma_ung_vien`) REFERENCES `nguoi_dung` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ung_vien`
--

LOCK TABLES `ung_vien` WRITE;
/*!40000 ALTER TABLE `ung_vien` DISABLE KEYS */;
/*!40000 ALTER TABLE `ung_vien` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-08 18:22:32
