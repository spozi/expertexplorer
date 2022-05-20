DROP TABLE IF EXISTS `candidate`;

CREATE TABLE `candidate` (
  `Photo` text,
  `Candidate` text,
  `University` text,
  `Number_of_docs` text,
  `Avg_sim` text,
  `Average_Similarity` text,
  `Image_Avg` text,
  `Variance` text,
  `Image_Var` text,
  `Related` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;