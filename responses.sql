-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 04, 2017 at 09:20 AM
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
-- Table structure for table `responses`
--

CREATE TABLE `responses` (
  `ID` int(11) NOT NULL,
  `Answer` varchar(2040) NOT NULL,
  `Keywords` varchar(2040) NOT NULL,
  `Question` varchar(2040) NOT NULL,
  `image_url` varchar(2048) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `responses`
--

INSERT INTO `responses` (`ID`, `Answer`, `Keywords`, `Question`, `image_url`) VALUES
(1, 'sh100 ', 'classroom,273,cmpe', 'where', 'none'),
(2, 'eng281', 'office,location', 'what', 'none'),
(3, 'wednesday 5:00 to 6:00 pm', 'office,hours', 'what', 'none'),
(4, 'sithu aung', 'cmpe,273,instructor', 'who', 'none'),
(5, 'sithu.aung@sjsu.edu', 'professor,email,273', 'what', 'none'),
(7, 'wednesday 6:00pm–8:45pm', 'class,273,days,time', 'what', 'none'),
(8, 'strong in a oop or functional programming language', 'prerequisites,cmpe,273', 'what', 'none'),
(9, 'https://sjsu.instructure.com', 'website,canvas,course,273', 'what', 'none'),
(10, 'the objective of this course is to introduce you to the architecture principles, application protocols, web service api design and integration patterns for building distributed system.', 'course,description,273', 'what', 'none'),
(11, 'introduction to application protocols for large scale distributed systems including object request brokers, asynchronous messaging, and web services. lab is based on using protocols to build distributed systems', 'course,catalog,description,273', 'what', 'none'),
(12, 'be able to demonstrate an understanding of advanced knowledge of the practice of software engineering, from vision to analysis, design, validation and deployment.', 'program,outcomes,1,po1', 'what', 'none'),
(13, 'be able to tackle complex engineering problems and tasks, using contemporary engineering principles, methodologies and tools.', 'program,outcomes,2,po2', 'what', 'none'),
(14, 'be able to demonstrate leadership and the ability to participate in teamwork in an environment with different disciplines of engineering, science and business.', 'program,outcomes,3,po3', 'what', 'none'),
(15, 'be aware of ethical, economic and environmental implications of their work, as appropriate.', 'program,outcomes,4,po4', 'what', 'none'),
(16, 'be able to advance successfully in the engineering profession, and sustain a process of life-long learning in engineer or other professional areas.', 'program,outcomes,5,po5', 'what', 'none'),
(17, 'be able to communicate effectively, in both oral and written forms.', 'program,outcomes,6,po6', 'what', 'none'),
(18, 'ability to demonstrate an understanding of architecture principles in building distributed systems.', 'course,learning,objectives,clo1', 'what', 'none'),
(19, 'ability to create application services using web services.', 'course,learning,objectives,clo2', 'what', 'none'),
(20, 'ability to integrate application services using java messaging services.', 'course,learning,objectives,clo3', 'what', 'none'),
(21, 'ability to design and implement distributed systems with a particular emphasis on how to deal with the shared state using distributed caching.', 'course,learning,objectives,clo4', 'what', 'none'),
(22, 'ability to identify and evaluate application protocols and integration patterns for distributed system.', 'course,learning,objectives,clo5', 'what', 'none'),
(23, 'there is no text that really corresponds to the material and focus of this course, \r\nhowever, some recommended books for the class are:\r\n\r\n/n web services, by gustavo alonso, fabio casati, harumi kuno and vijay machiraju (2003)\r\n/n enterprise integration patterns, by gregor hohpe and bobby woolf (2003)\r\n/n restful web services, by leonard richardson, sam ruby and david hansson (2007) \r\n', 'text,book,readings,273', 'what', 'none'),
(24, 'this course consists of a single lecture per week.  in-class activities including hands-on labs will be given to encourage attendance. you are encouraged to consult with me on your group project to make sure it is successful.', 'classroom,protocol,cmpe,273', 'what', 'none'),
(25, 'students are responsible for understanding the policies and procedures about add/drops, academic renewal, etc. information on add/drops is available at http://info.sjsu.edu/web-dbgen/narr/soc-fall/rec-298.html. information about late drop is available at http://www.sjsu.edu/sac/advising/latedrops/policy/. students should be aware of the current deadlines and penalties for adding and dropping classes.', 'dropping,and,adding,273', 'how', 'none'),
(26, 'your final grade will be based on labs, assignments, project, exams, and class participation. these will be weighted as follows: \r\n/n pop quizzes - 5%\r\n/n labs - 5%\r\n/n assignments - 30%\r\n/n class project - 20%\r\n/n midterm exam - 20%\r\n/n final exam - 20%\r\n\r\nthere will be no make-up exam. absence from the scheduled final exam will result in a failing grade in the course unless documented reasons are submitted to the instructor and receiving a written approval from the instructor before the exam.', 'assignments,grading,policy,273', 'what', 'none'),
(27, 'all labs must be done in the class or you will get no credit.', 'hands-on,labs,cmpe,273', 'where', 'none'),
(28, 'students will work in groups of five students on a semester-long project. you will be required to give a presentation on a running demo and submit project documents and source code to github for shared team project and bitbucket for individual assignments.', 'project,cmpe,273', 'how', 'none'),
(29, 'assignments and projects are due before class. that means that i will collect all the hardcopies at the beginning of class. late submissions incur a 20% penalty of total points for each day. exceptions will be granted only if arranged prior to the due date or a documented illness intervenes.', 'deadlines,assignments,projects,273', 'what', 'none'),
(30, 'the grading will be curved.\r\nnote: the instructor reserves the right to change the grade based on class participation, quality of work on assignments, and above-and-beyond project contribution. \r\n', 'grading,course,cmpe,273', 'how', 'none'),
(31, '/n all the assignments and project code must be submitted electronically to your gitHub/gitbucket’s repository. \r\n/n all assignments and the final exam must be done individually.  \r\n', 'submission,assignment,project,273', 'when', 'none'),
(32, 'students should know that the university’s academic integrity policy is available at http://www.sa.sjsu.edu/download/judicial_affairs/academic_integrity_policy_s07-2.pdf. your own commitment to learning, as evidenced by your enrollment at san jose state university and the university’s integrity policy, require you to be honest in all your academic course work. faculty members are required to report all infractions to the office of student conduct and ethical development. the website for student conduct and ethical development is available at http://www.sa.sjsu.edu/judicial_affairs/index.html. \r\ninstances of academic dishonesty will not be tolerated. cheating on exams or plagiarism (presenting the work of another as your own, or the use of another person’s ideas without giving proper credit) will result in a failing grade and sanctions by the university. for this class, all assignments are to be completed by the individual student unless otherwise specified. if you would like to include in your assignment any material you have submitted, or plan to submit for another class, please note that sjsu’s academic policy f06-1 requires approval of instructors.\r\ncampus policy in compliance with the american disabilities act\r\nif you need course adaptations or accommodations because of a disability, or if you need to make special arrangements in case the building must be evacuated, please make an appointment with me as soon as possible, or see me during office hours. presidential directive 97-03 requires that students with disabilities requesting accommodations must register with the drc (disability resource center) to establish a record of their disability.\r\n\r\n', 'academic,integrity,course,policy', 'what', 'none'),
(33, '/n	copying online content without correct quote is treated as plagiarism in this class.\r\n/n	both the person who copies and the person who facilitates the copying will be prosecuted for academic dishonesty.\r\n/n	a student or students involved in a cheating incident involving any non-exam instrument (homework, reports, projects, or class exercises) will receive an f on that instrument, and will be reported to the judicial affairs office. whether the report will carry a recommendation for disciplinary action will be left to my judgment.\r\n/n	a student or students involved in a cheating incident on any quick test, the midterm exam or the final exam will receive an f in the course, and will be reported to the judicial affairs office with a recommendation for disciplinary action.\r\nthings (among many others) you may not do when working with other students (except for team work):\r\n/n	the term “solution” mentioned below means anything (code, design document, description, etc.) you will submit for assignments and exams.\r\n/n	work on an assignment together, type in solutions (separately or together) and turn in separate copies.\r\n/n	each works on a part of an assignment and turn in separate copies after combining solutions.\r\n/n	give any part of your solution (through paper, board writing, email, web posting, reading loud, letting someone else look at your screen, etc.) to other students before the assignment deadline.\r\n\r\nthings you may do when working with other students:\r\n/n	discuss with other students and leave the discussion with empty hands.\r\n/n	share assignment solutions after the assignment deadline in order to compare different techniques used for solving the problems.\r\n\r\n', 'university,course,policy,plagiarism', 'what', 'none'),
(34, 'the learning assistance resource center (larc) is located in room 600 in the student services center. it is designed to assist students in the development of their full academic potential and to motivate them to become self-directed learners. the center provides support services, such as skills assessment, individual or group tutorials, subject advising, learning assistance, summer academic preparation and basic skills development. the larc website is located at http:/www.sjsu.edu/larc/.', 'learning,assistance,resource,center', 'where', 'none'),
(35, 'the sjsu writing center is located in room 126 in clark hall.  it is staffed by professional instructors and upper-division or graduate-level writing specialists from each of the seven sjsu colleges. our writing specialists have met a rigorous gpa requirement, and they are well trained to assist all students at all levels within all disciplines to become better writers. the writing center website is located at http://www.sjsu.edu/writingcenter/about/staff/\r\n\r\n', 'sjsu,writing,center', 'where', 'none'),
(36, 'the peer mentor center is located on the 1st floor of clark hall in the academic success center. the peer mentor center is staffed with peer mentors who excel in helping students manage university life, tackling problems that range from academic challenges to interpersonal struggles. on the road to graduation, peer mentors are navigators, offering “roadside assistance” to peers who feel a bit lost or simply need help mapping out the locations of campus resources. peer mentor services are free and available on a drop –in basis, no reservation required. the peer mentor center website is located at http://www.sjsu.edu/muse/peermentor/', 'peer,mentor,center,sjsu', 'where', 'none'),
(37, 'distributed systems overview ', 'course,schedule,week,1,topic', 'what', 'none'),
(38, 'no dues', 'course,schedule,week,1,dues', 'what', 'none'),
(39, 'integration protocols', 'course,schedule,week,2,topic', 'what', 'none'),
(40, 'no dues', 'course,schedule,week,2,dues', 'what', 'none'),
(41, 'remote procedural calls', 'course,schedule,week,3,topic', 'what', 'none'),
(42, 'lab 1', 'course,schedule,week,3,dues', 'what', 'none'),
(43, 'restful web services', 'course,schedule,week,4,topic', 'what', 'none'),
(44, 'no dues', 'course,schedule,week,4,dues', 'what', 'none'),
(46, 'restful web services', 'course,schedule,week,5,topic', 'what', 'none'),
(47, 'no dues', 'course,schedule,week,5,dues', 'what', 'none'),
(48, 'messaging', 'course,schedule,week,6,topic', 'what', 'none'),
(49, 'assignment 1 ', 'course,schedule,week,6,dues', 'what', 'none'),
(50, 'consistency models', 'course,schedule,week,7,topic', 'what', 'none'),
(51, 'no dues', 'course,schedule,week,7,dues', 'what', 'none'),
(52, 'fault tolerance (replication)', 'course,schedule,week,8,topic', 'what', 'none'),
(53, 'lab 2', 'course,schedule,week,8,dues', 'what', 'none'),
(54, 'spring recess – no class', 'course,schedule,week,9,topic', 'what', 'none'),
(55, 'assignment 2 ', 'course,schedule,week,9,dues', 'what', 'none'),
(56, 'mid-term exam', 'course,schedule,week,10,topic', 'what', 'none'),
(57, 'tbd', 'course,schedule,week,10,dues', 'what', 'none'),
(58, 'fault tolerance (sharding)', 'course,schedule,week,11,topic', 'what', 'none'),
(59, 'lab 3', 'course,schedule,week,11,dues', 'what', 'none'),
(60, 'fault tolerance (consensus)', 'course,schedule,week,12,topic', 'what', 'none'),
(61, 'no dues', 'course,schedule,week,12,dues', 'what', 'none'),
(62, 'performance', 'course,schedule,week,13,topic', 'what', 'none'),
(63, 'assignment 3', 'course,schedule,week,13,dues', 'what', 'none'),
(64, 'decentralized applications', 'course,schedule,week,14,topic', 'what', 'none'),
(65, 'no dues', 'course,schedule,week,14,dues', 'what', 'none'),
(66, 'project presentations', 'course,schedule,week,15,topic', 'what ', 'none'),
(67, 'lab 4', 'course,schedule,week,15,dues', 'what', 'none'),
(68, 'final exam 5:15 pm –7:30 pm', 'course,schedule,week,17,topic', 'what', 'none'),
(69, 'tbd', 'course,schedule,week,17,dues', 'what', 'none');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `responses`
--
ALTER TABLE `responses`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `responses`
--
ALTER TABLE `responses`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
