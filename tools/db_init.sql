CREATE DATABASE InstagramSchema;
USE InstagramSchema;
CREATE TABLE `igdb` (
 `ig_key` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
 `ig_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
 `file_path` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
 `status` int(11) NOT NULL DEFAULT '1',
 PRIMARY KEY (`ig_key`,`ig_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci