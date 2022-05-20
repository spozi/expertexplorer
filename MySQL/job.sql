DROP TABLE IF EXISTS `job`;

CREATE TABLE `job` (
  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(30) NOT NULL,
  `link` varchar(240) NOT NULL,
  `name` varchar(60) NOT NULL,
  `description` varchar(3500) NOT NULL,
  `company` varchar(60) NOT NULL,
  `image` varchar(140) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;