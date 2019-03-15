-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 15, 2019 at 11:53 PM
-- Server version: 5.7.21-1
-- PHP Version: 7.0.29-1+b1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `learning`
--

-- --------------------------------------------------------

--
-- Table structure for table `activation`
--

CREATE TABLE `activation` (
  `id_activation` int(5) NOT NULL,
  `id_user` int(5) NOT NULL,
  `code_activation` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `activation`
--

INSERT INTO `activation` (`id_activation`, `id_user`, `code_activation`) VALUES
(1, 1, '6518'),
(2, 1, '9609'),
(3, 1, '2678');

-- --------------------------------------------------------

--
-- Table structure for table `Class`
--

CREATE TABLE `Class` (
  `id_class` int(5) NOT NULL,
  `id_teach` varchar(5) NOT NULL,
  `name_class` varchar(50) NOT NULL,
  `description` varchar(100) NOT NULL,
  `prodi` varchar(30) NOT NULL,
  `semester` varchar(2) NOT NULL,
  `sesi` enum('1','2') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Class`
--

INSERT INTO `Class` (`id_class`, `id_teach`, `name_class`, `description`, `prodi`, `semester`, `sesi`) VALUES
(1, '6', 'Jaringan Komputer', 'Makul Jaringan Komputer ', 'Teknik Informatika', '6', '1'),
(2, '6', 'DIgital Forensic', 'Digital Forensic', 'Teknik Informatika', '6', '1');

-- --------------------------------------------------------

--
-- Table structure for table `Comment`
--

CREATE TABLE `Comment` (
  `id_comment` int(5) NOT NULL,
  `id_posting` int(5) NOT NULL,
  `data` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Comment`
--

INSERT INTO `Comment` (`id_comment`, `id_posting`, `data`) VALUES
(2, 1, 'asajsalsj'),
(3, 1, 'hahah good'),
(4, 1, 'hahah good'),
(5, 1, 'hahah good'),
(6, 1, 'Haha Mantap');

-- --------------------------------------------------------

--
-- Table structure for table `Join_class`
--

CREATE TABLE `Join_class` (
  `id_join` int(6) NOT NULL,
  `id_user` int(5) NOT NULL,
  `id_class` int(5) NOT NULL,
  `rule` tinyint(1) NOT NULL,
  `accept` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Join_class`
--

INSERT INTO `Join_class` (`id_join`, `id_user`, `id_class`, `rule`, `accept`) VALUES
(1, 1, 1, 0, 1),
(2, 2, 1, 0, 1),
(3, 3, 1, 0, 0),
(4, 1, 2, 0, 1),
(7, 6, 1, 1, 1),
(8, 6, 2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `Posting`
--

CREATE TABLE `Posting` (
  `id_posting` int(8) NOT NULL,
  `id_class` int(5) NOT NULL,
  `id_user` int(5) NOT NULL,
  `caption` varchar(200) NOT NULL,
  `category` varchar(2) NOT NULL,
  `file` varchar(50) NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `Posting`
--

INSERT INTO `Posting` (`id_posting`, `id_class`, `id_user`, `caption`, `category`, `file`, `time`) VALUES
(1, 1, 1, 'Mencoba', '1', 'ada.png', '2019-02-26 05:14:26'),
(2, 2, 4, 'Mencoba', '2', 'ada.png', '2019-02-27 09:03:36'),
(3, 1, 1, 'Aplikasi Anti HOax', '2', 'ini.rar', '2019-02-27 09:18:25'),
(18, 2, 1, 'coba', '1', 'ada.png', '2019-02-27 22:09:55'),
(19, 2, 1, 'coba', '1', 'ada.png', '2019-02-27 22:10:33'),
(20, 2, 1, 'Mencoba', '1', 'file.png', '2019-02-28 11:25:07');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `id_user` int(5) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(25) NOT NULL,
  `prodi` varchar(50) NOT NULL,
  `verifed` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id_user`, `avatar`, `username`, `email`, `password`, `prodi`, `verifed`) VALUES
(1, 'http://puspidep.org/image_file/uploads/bikcxhyfjuptonrewazdpp.jpeg', 'nurchulis', 'nura3609@gmail.com', '12345', 'Teknik Informatika', 1),
(2, 'user2.png', 'Latifah Lina nurhidayah', 'latifahlina@gmail.com', '12345', 'Biologi', 1),
(3, 'user3.png', 'Siska Dewi S', 'siskadewis@gmail.com', '12345', 'Matematika', 1),
(4, 'user4.png', 'Bayu', 'bayuirfan@gmail.com', '12345', 'Teknik Informatika', 1),
(5, 'user5.png', 'Sasmitha Ramadhantie', 'sasmitha@gmail.com', '12345', 'Biologi', 0),
(6, 'user6.png', 'Bambang', 'bambanginfo@gmail.com', '12345', 'Teknik Informatika', 1),
(7, 'user.png', 'nurchulis', 'nura360@gmail.com', '12345', 'Teknik informatika', 0),
(8, 'user.png', 'nurchulis', 'nura360@gmail.com', '12345', 'Teknik informatika', 0),
(9, 'user1.png', 'aku', 'nura3609@gmail.com', '12345', 'Teknik Informatika', 0),
(10, 'user1.png', 'juang', 'nura3609@gmail.com', '12345', 'Teknik Informatika', 0),
(11, 'user1.png', 'nurchuliss', 'nura3609@gmail.com', '12345', 'Teknik Informatika', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activation`
--
ALTER TABLE `activation`
  ADD PRIMARY KEY (`id_activation`);

--
-- Indexes for table `Class`
--
ALTER TABLE `Class`
  ADD PRIMARY KEY (`id_class`);

--
-- Indexes for table `Comment`
--
ALTER TABLE `Comment`
  ADD PRIMARY KEY (`id_comment`);

--
-- Indexes for table `Join_class`
--
ALTER TABLE `Join_class`
  ADD PRIMARY KEY (`id_join`);

--
-- Indexes for table `Posting`
--
ALTER TABLE `Posting`
  ADD PRIMARY KEY (`id_posting`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activation`
--
ALTER TABLE `activation`
  MODIFY `id_activation` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `Class`
--
ALTER TABLE `Class`
  MODIFY `id_class` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `Comment`
--
ALTER TABLE `Comment`
  MODIFY `id_comment` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `Join_class`
--
ALTER TABLE `Join_class`
  MODIFY `id_join` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `Posting`
--
ALTER TABLE `Posting`
  MODIFY `id_posting` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `User`
--
ALTER TABLE `User`
  MODIFY `id_user` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
