-- sqlite3 ~/.local/share/mpd_sima/sima.db ".read data/sql/blocklist.sql"
--
.headers on
.separator " / "

SELECT artists.name AS artist,
       artists.mbid AS musicbrainz_artist,
	   albums.name AS album,
	   albums.mbid AS musicbrainz_album,
	   tracks.title AS title,
	   tracks.mbid AS musicbrainz_title
FROM blocklist
LEFT OUTER JOIN artists ON blocklist.artist = artists.id
LEFT OUTER JOIN albums ON blocklist.album = albums.id
LEFT OUTER JOIN tracks ON blocklist.track = tracks.id
