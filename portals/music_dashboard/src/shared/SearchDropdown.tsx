import { SongItemsListProps } from "../interfaces";
import SongItem from "../libraryPage/SongItem";

const SearchDropdown = ({ songs, className }: SongItemsListProps) => {
  return (
    <div className={className}>
      {songs.map((song) => (
        <SongItem
          className="flex px-4 py-2 text-amber-700 bg-white hover:bg-slate-50"
          key={song.songId}
          songId={song.songId}
          songName={song.songName}
          artist={song.artist}
          album={song.album}
          YTURL={song.YTURL}
        />
      ))}
    </div>
  );
};

export default SearchDropdown;
