-- sqlite3 ~/.local/share/mpd_sima/sima.db ".read data/sql/history.sql"
.headers on
.separator " / "

SELECT history.last_play, tracks.title, artists.name, albums.name
FROM history
JOIN tracks ON history.track = tracks.id
LEFT OUTER JOIN artists ON tracks.artist = artists.id
LEFT OUTER JOIN albumartists ON tracks.albumartist = albumartists.id
LEFT OUTER JOIN albums ON tracks.album = albums.id;
