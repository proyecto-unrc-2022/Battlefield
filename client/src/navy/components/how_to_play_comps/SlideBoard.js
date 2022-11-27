import WaterWave from "react-water-wave";
import board from "../../assets/board.png";

const SlideBoard = () => {
  return (
    <WaterWave
      className="image mx-auto"
      style={{ width: "100%", height: "100%", backgroundSize: "cover" }}
      imageUrl={board}
      perturbance={0.005}
      resolution={256}
      dropRadius={30}
    >
      {() => <div style={{width:"716px", height: "134px" }}></div>}
    </WaterWave>
  );
};

export default SlideBoard;
