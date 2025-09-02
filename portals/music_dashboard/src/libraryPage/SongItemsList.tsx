import { SongItemsListProps } from "../interfaces";
import SongItem from "./SongItem";

const SongItemsList = ({
  songs,
  handleSongActionTriggered,
}: SongItemsListProps) => {
  return (
    <div className="space-y-2">
      {songs.map((song) => (
          <SongItem
            className="flex space-x-4 items-center px-4 py-2 ring-1 rounded-full cursor-pointer ring-lime-600/75 bg-white hover:ring-lime-400"
            key={song.songId}
            songId={song.songId}
            songName={song.songName}
            artist={song.artist}
            album={song.album}
            YTURL={song.YTURL}
            showActions
            handleActionTriggered={handleSongActionTriggered}
          />
      ))}
    </div>
  );
};

export default SongItemsList;
