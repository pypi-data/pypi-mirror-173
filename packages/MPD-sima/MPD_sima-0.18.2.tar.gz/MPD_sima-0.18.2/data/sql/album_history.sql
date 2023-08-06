-- sqlite3 ~/.local/share/mpd_sima/sima.db ".read data/sql/history.sql"
.headers on
.separator " / "

SELECT albums.name AS name,
       albums.mbid AS mbid,
       artists.name AS artist,
       albumartists.name AS albumartist
FROM history
JOIN tracks ON history.track = tracks.id
LEFT OUTER JOIN albums ON tracks.album = albums.id
LEFT OUTER JOIN artists ON tracks.artist = artists.id
LEFT OUTER JOIN albumartists ON tracks.albumartist = albumartists.id
WHERE albums.name NOT NULL AND artists.name NOT NULL
