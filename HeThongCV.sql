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
-- Table structure for table `congty`
--

DROP TABLE IF EXISTS `congty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `congty` (
  `MaCongTy` int NOT NULL AUTO_INCREMENT,
  `TenCongTy` varchar(255) NOT NULL,
  `MoTa` text,
  PRIMARY KEY (`MaCongTy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `congty`
--

LOCK TABLES `congty` WRITE;
/*!40000 ALTER TABLE `congty` DISABLE KEYS */;
/*!40000 ALTER TABLE `congty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cv`
--

DROP TABLE IF EXISTS `cv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cv` (
  `MaCV` int NOT NULL AUTO_INCREMENT,
  `TenFile` varchar(255) NOT NULL,
  `MaUngVien` int NOT NULL,
  PRIMARY KEY (`MaCV`),
  KEY `MaUngVien` (`MaUngVien`),
  CONSTRAINT `cv_ibfk_1` FOREIGN KEY (`MaUngVien`) REFERENCES `ungvien` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cv`
--

LOCK TABLES `cv` WRITE;
/*!40000 ALTER TABLE `cv` DISABLE KEYS */;
/*!40000 ALTER TABLE `cv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hosoungtuyen`
--

DROP TABLE IF EXISTS `hosoungtuyen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hosoungtuyen` (
  `MaHoSo` int NOT NULL AUTO_INCREMENT,
  `MaUngVien` int NOT NULL,
  `TinId` int NOT NULL,
  `MaCV` int NOT NULL,
  `TrangThai` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `NgayNop` date NOT NULL,
  PRIMARY KEY (`MaHoSo`),
  KEY `MaUngVien` (`MaUngVien`),
  KEY `TinId` (`TinId`),
  KEY `MaCV` (`MaCV`),
  CONSTRAINT `hosoungtuyen_ibfk_1` FOREIGN KEY (`MaUngVien`) REFERENCES `ungvien` (`Id`),
  CONSTRAINT `hosoungtuyen_ibfk_2` FOREIGN KEY (`TinId`) REFERENCES `tintuyendung` (`TinId`),
  CONSTRAINT `hosoungtuyen_ibfk_3` FOREIGN KEY (`MaCV`) REFERENCES `cv` (`MaCV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hosoungtuyen`
--

LOCK TABLES `hosoungtuyen` WRITE;
/*!40000 ALTER TABLE `hosoungtuyen` DISABLE KEYS */;
/*!40000 ALTER TABLE `hosoungtuyen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nguoidung`
--

DROP TABLE IF EXISTS `nguoidung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nguoidung` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `VaiTro` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nguoidung`
--

LOCK TABLES `nguoidung` WRITE;
/*!40000 ALTER TABLE `nguoidung` DISABLE KEYS */;
/*!40000 ALTER TABLE `nguoidung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhatuyendung`
--

DROP TABLE IF EXISTS `nhatuyendung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhatuyendung` (
  `MaNhaTuyenDung` int NOT NULL,
  `TenNguoiTuyenDung` varchar(255) NOT NULL,
  `MaCongTy` int NOT NULL,
  PRIMARY KEY (`MaNhaTuyenDung`),
  KEY `MaCongTy` (`MaCongTy`),
  CONSTRAINT `nhatuyendung_ibfk_1` FOREIGN KEY (`MaNhaTuyenDung`) REFERENCES `nguoidung` (`Id`),
  CONSTRAINT `nhatuyendung_ibfk_2` FOREIGN KEY (`MaCongTy`) REFERENCES `congty` (`MaCongTy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhatuyendung`
--

LOCK TABLES `nhatuyendung` WRITE;
/*!40000 ALTER TABLE `nhatuyendung` DISABLE KEYS */;
/*!40000 ALTER TABLE `nhatuyendung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quantri`
--

DROP TABLE IF EXISTS `quantri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quantri` (
  `Id` int NOT NULL,
  `TenQuanTri` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `quantri_ibfk_1` FOREIGN KEY (`Id`) REFERENCES `nguoidung` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quantri`
--

LOCK TABLES `quantri` WRITE;
/*!40000 ALTER TABLE `quantri` DISABLE KEYS */;
/*!40000 ALTER TABLE `quantri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tintuyendung`
--

DROP TABLE IF EXISTS `tintuyendung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tintuyendung` (
  `TinId` int NOT NULL AUTO_INCREMENT,
  `TieuDe` varchar(255) NOT NULL,
  `MoTa` text,
  `MaNhaTuyenDung` int NOT NULL,
  PRIMARY KEY (`TinId`),
  KEY `MaNhaTuyenDung` (`MaNhaTuyenDung`),
  CONSTRAINT `tintuyendung_ibfk_1` FOREIGN KEY (`MaNhaTuyenDung`) REFERENCES `nhatuyendung` (`MaNhaTuyenDung`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tintuyendung`
--

LOCK TABLES `tintuyendung` WRITE;
/*!40000 ALTER TABLE `tintuyendung` DISABLE KEYS */;
/*!40000 ALTER TABLE `tintuyendung` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ungvien`
--

DROP TABLE IF EXISTS `ungvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ungvien` (
  `Id` int NOT NULL,
  `HoTen` varchar(255) NOT NULL,
  `SoDienThoai` varchar(20) NOT NULL,
  `NgaySinh` date NOT NULL,
  `GioiTinh` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Email` varchar(100) NOT NULL,
  PRIMARY KEY (`Id`),
  CONSTRAINT `ungvien_ibfk_1` FOREIGN KEY (`Id`) REFERENCES `nguoidung` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ungvien`
--

LOCK TABLES `ungvien` WRITE;
/*!40000 ALTER TABLE `ungvien` DISABLE KEYS */;
/*!40000 ALTER TABLE `ungvien` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-19 13:52:03
