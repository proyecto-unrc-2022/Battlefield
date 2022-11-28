import { useRef, useState } from "react";

const FiltersComponent = ({ filter }) => {
  const [option, setOption] = useState(null);

  const inputMyGames = useRef(null);
  const inputWaiting = useRef(null);
  const inputPlaying = useRef(null);

  const handleChange = (e) => {
    const refs = [inputMyGames, inputPlaying, inputWaiting];
    refs.forEach((ref) => {
      if (ref.current.value !== e.target.value) {
        ref.current.checked = false;
      }
    });
    if (e.target.value === option) {
      setOption(null);
      filter(null);
    } else {
      setOption(e.target.value);
      filter(e.target.value);
    }
  };

  return (
    <div style={{ gap: "14px" }} className="d-flex">
      <div style={{ gap: "4px" }} className="d-flex">
        <label className="navy-text">My Games</label>
        <input
          ref={inputMyGames}
          onChange={handleChange}
          type={"checkbox"}
          value="my-games"
        ></input>
      </div>
      <div style={{ gap: "4px" }} className="d-flex">
        <label className="navy-text">Waiting</label>
        <input
          ref={inputWaiting}
          onChange={handleChange}
          type={"checkbox"}
          value="waiting"
        ></input>
      </div>
      <div style={{ gap: "4px" }} className="d-flex">
        <label className="navy-text">Playing</label>
        <input
          ref={inputPlaying}
          onChange={handleChange}
          type={"checkbox"}
          value="playing"
        ></input>
      </div>
    </div>
  );
};

export default FiltersComponent;
