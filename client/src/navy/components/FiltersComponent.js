import { useEffect, useState } from "react";

const FiltersComponent = ({filter}) => {

  const [option, setOption] = useState(null)

  const handleChange = (e) => {
    if(e.target.value === option){
      setOption(null)
      filter(null)
    }
    else {
      setOption(e.target.value)
      filter(e.target.value)
    }
  }

  return (
    <div style={{gap: "14px"}} className="d-flex">
      <div style={{gap: "4px"}} className="d-flex">
        <input disabled={option && option !== "my-games"} onChange={handleChange} type={"checkbox"} value="my-games"></input>
        <label>My Games</label>
      </div>
      <div style={{gap: "4px"}} className="d-flex">
        <input disabled={option && option !== "waiting"} onChange={handleChange} type={"checkbox"} value="waiting"></input>
        <label>Waiting</label>
      </div>
      <div style={{gap: "4px"}} className="d-flex">
        <input disabled={option && option !== "playing"} onChange={handleChange} type={"checkbox"} value="playing"></input>
        <label>Playing</label>
      </div>
    </div>
  )
}

export default FiltersComponent