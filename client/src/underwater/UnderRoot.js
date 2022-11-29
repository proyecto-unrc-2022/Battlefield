import { Outlet } from "react-router-dom";
import "./css/style.css";

export default function UnderRoot() {
  return (
    <div className="u-container">
      <Outlet />
    </div>
  );
}
