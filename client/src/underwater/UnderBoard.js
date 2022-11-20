import "./css/board.css"

export default function UnderBoard({length, width}) {
    const array = Array.from(Array(length*width).keys());
    
    function setDimention(w) {
        switch (w) {
            case '24': return "u-grid-24"; break;
            case '28': return "u-grid-28"; break;
            default: return "u-grid-20";
        }
    }

    return (
        <div className="u-board-container">
            <div className={"u-grid-" + width}>
                {array.map(element => {
                    return <div className="u-cell"></div>
                })}
            </div>
        </div>
    )
}