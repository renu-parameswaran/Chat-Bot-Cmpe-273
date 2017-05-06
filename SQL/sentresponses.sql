-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 06, 2017 at 04:28 AM
-- Server version: 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sarasjsu`
--

-- --------------------------------------------------------

--
-- Table structure for table `sentresponses`
--

CREATE TABLE `sentresponses` (
  `ID` int(100) NOT NULL,
  `UserQuestion` varchar(2048) NOT NULL,
  `Answer` varchar(2048) NOT NULL,
  `MatchingKeywords` varchar(2048) NOT NULL,
  `QuestionPart` varchar(2048) NOT NULL,
  `CurrentScore` int(100) NOT NULL,
  `Timestamp` varchar(2048) NOT NULL,
  `image_url` varchar(2048) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sentresponses`
--

INSERT INTO `sentresponses` (`ID`, `UserQuestion`, `Answer`, `MatchingKeywords`, `QuestionPart`, `CurrentScore`, `Timestamp`, `image_url`) VALUES
(1, 'who is the professor for cmpe 273', 'sithu aung', 'professor,cmpe,273 ', 'who', 0, '2017-05-05 08:05:39.252000', 'http://www.intuitlabs.com/wp-content/uploads/2014/12/saung_gif.jpg'),
(2, 'where is cmpe 273 class?', 'sh100 ', 'cmpe,273,class? ', 'where', 1, '2017-05-05 08:07:16.022000', 'none'),
(3, 'who is the instructor', 'sithu', 'instructor ', 'who', 0, '2017-05-05 18:14:44.677000', 'none'),
(4, 'who is the ta', 'umang', 'ta ', 'who', 1, '2017-05-05 18:25:44.997000', 'none'),
(5, 'who is the department chair', 'professor su', 'department,chair ', 'who', 1, '2017-05-05 18:26:48.425000', 'none'),
(6, 'who is the department head', 'professor su', 'department,head ', 'who', 1, '2017-05-05 18:26:59', 'none'),
(7, 'what is the name of department chair', 'professor su', 'name,department,chair ', 'what', -2, '2017-05-05 18:42:35.625000', 'none');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sentresponses`
--
ALTER TABLE `sentresponses`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sentresponses`
--
ALTER TABLE `sentresponses`
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
