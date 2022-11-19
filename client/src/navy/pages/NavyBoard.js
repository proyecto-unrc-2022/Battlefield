import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import authService from "../../services/auth.service";
import AccessDenied from "../components/AccessDenied";
import NavyGameService from "../services/NavyGameService";

const NavyBoard = () => {
  const [game, setGame] = useState(null);
  const [accessDenied, setAccessDenied] = useState(true);
  const navigate = useNavigate()
  const {id} = useParams()

  useEffect(() => {
    NavyGameService.getNavyGame(id)
      .then((resp) => {
        const currentUser = authService.getCurrentUser();
        const accessDenied =
          currentUser.sub !== resp.data.data.user_1.id &&
          currentUser.sub !== resp.data.data.user_2.id;

        setAccessDenied(accessDenied);

        if (!accessDenied) {
          if (resp.data.data.status === "WAITING_PICKS") {
            navigate(`/navy/games/${id}/ship_selection`);
          } else if (resp.data.data.status === "WAITING_PLAYERS") {
            navigate(`/navy/games/${id}/lobby`);
          }
        }
        setGame(resp.data.data);
      })
      .catch((resp) => {
        setGame({});
        setAccessDenied(true);
      });
  }, []);

  return (
    <div style={{ flexGrow: "1" }} className="container-fluid bg-navy">
      {!game ? (
        <div className="row mt-5">
          <div className="col-12 text-center">
            <div className="spinner-border" role="status">
              <span className="sr-only">Loading...</span>
            </div>
          </div>
        </div>
      ) : accessDenied ? (
        <AccessDenied
          text={"You can't join to this game"}
          buttonText={"Go to games"}
          redirectTo={"/navy/games"}
        />
      ) : (
        <>
          NavyBoard
        </>
      )}
    </div>
  )
};

export default NavyBoard;
