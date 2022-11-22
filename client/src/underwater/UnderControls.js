import React, { useEffect } from "react";
import AuthService from "../services/auth.service"

export default function UnderControls() {
  const userId = AuthService.getCurrentUser().sub;

  return (
    <div className="u-controls-container">
      <div className="u-left-controls">
        <span>{userId}</span>
      </div>
      <div className="u-right-controls">
        <span>Acá van los controles de acciones</span>
      </div>
    </div>
  )
}
