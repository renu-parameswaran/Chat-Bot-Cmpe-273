-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 29, 2017 at 04:49 AM
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
  `Timestamp` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sentresponses`
--

INSERT INTO `sentresponses` (`ID`, `UserQuestion`, `Answer`, `MatchingKeywords`, `QuestionPart`, `CurrentScore`, `Timestamp`) VALUES
(1, 'where is the classroom for 273', 'Hello I am sara', 'is,classroom,273 ', 'where', 1, '2017-04-28 18:26:17.425000'),
(2, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:27:00.157000'),
(3, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:29:17.381000'),
(4, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:30:17.969000'),
(5, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:30:25.221000'),
(6, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:30:31.392000'),
(7, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:30:37.608000'),
(8, 'who is the instructor for 273', 'Hello I am sara', 'is,instructor,273 ', 'who', 1, '2017-04-28 18:57:33.506000'),
(9, 'where is 273', 'Hello I am sara', 'is,273 ', 'where', 1, '2017-04-28 18:57:50.308000'),
(10, 'where is 273', 'Hello this is sara', 'is,273 ', 'where', 1, '2017-04-28 18:58:26.953000'),
(11, 'who is 273', 'Hello this is sara', 'is,273 ', 'who', 1, '2017-04-28 19:19:00.967000');

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
  MODIFY `ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
