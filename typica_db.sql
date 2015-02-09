CREATE TABLE `Student` (
  `idStudent` int(11) NOT NULL,
  `StudentName` varchar(45) NOT NULL,
  `StudentBirthDate` int(11)  NOT NULL,
  `StudentPW` varchar(255) NOT NULL,
  `StudentEmail` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idStudent`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Student_cabinet` (
  `StudentCabinet_ID` int(11) NOT NULL,
  `Student_ID` int(11) NOT NULL,
  `Cabinet_ID` int(11) NOT NULL,
  `Time` time NOT NULL,
  PRIMARY KEY (`StudentCabinet_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Student_Fee` (
  `idStudent_Fee` int(11) NOT NULL,
  `Student_ID` int(11) NOT NULL,
  `Fee_TF` tinyint(1) NULL,
  PRIMARY KEY (`idStudent_Fee`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `TotalCabinet` (
  `idTotalCabinet` int(11) NOT NULL,
  `Cabinet_Area` varchar(3) NOT NULL,
  `Cabinet_Number` varchar(45) NOT NULL,
  PRIMARY KEY (`idTotalCabinet`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
