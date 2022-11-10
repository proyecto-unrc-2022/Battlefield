export default function HomeButtons({setVisibleComp}) {

  return (
    <div className="u-options">
      <div onClick={() => {setVisibleComp("new")}} className="u-big-button">New Game</div>
      <div onClick={() => {setVisibleComp("join")}} className="u-big-button">Join Game</div>
    </div>
  );
}