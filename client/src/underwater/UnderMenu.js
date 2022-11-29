import { Outlet } from "react-router-dom";

export default function UnderMenu() {
  return (
    <div className="u-centered-container u-background-image">
      <div className="u-title">SUBMARINE BATTLE</div>
      <Outlet />
    </div>
  );
}
