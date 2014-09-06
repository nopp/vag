--
-- Database: `vag`
--

-- --------------------------------------------------------

--
-- Table structure for table `cluster`
--

CREATE TABLE IF NOT EXISTS `cluster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `varnish`
--

CREATE TABLE IF NOT EXISTS `varnish` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `ip` text NOT NULL,
  `id_cluster` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(200) NOT NULL,
  `pass` varchar(200) NOT NULL,
  `group` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `login`, `pass`, `group`) VALUES
(1, 'admin', 'admin', 'admin'),
(2, 'view', 'view', 'view');

--
-- Table structure for table `vcl`
--

CREATE TABLE IF NOT EXISTS `vcl` (   
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cluster` int(11) NOT NULL,
  `user` text NOT NULL,
  `date` text NOT NULL,
  `content` text NOT NULL,
  PRIMARY KEY (`id`) 
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;
