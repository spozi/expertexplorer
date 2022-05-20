DROP TABLE IF EXISTS `publications_tab_2020`;

CREATE TABLE `publications_tab_2020` (
  `id` int(90) unsigned NOT NULL AUTO_INCREMENT,
  `photo` blob NOT NULL,
  `author` varchar(512) NOT NULL,
  `university` varchar(60) NOT NULL,
  `vector` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;