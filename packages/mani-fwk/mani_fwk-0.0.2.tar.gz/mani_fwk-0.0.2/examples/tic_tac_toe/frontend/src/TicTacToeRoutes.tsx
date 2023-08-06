import {Routes} from "react-router-dom";
import {Route} from "react-router";
import {FC} from "react";
import {LobbyPage} from "./pages/LobbyPage";
import GamePage from "./pages/GamePage";

export enum AppRoutes {
  HOME = "/",
  GAME_SCREEN = "/game"
}


export const TicTacToeRoutes: FC = () => {
  return <Routes>
    <Route path={`${AppRoutes.HOME}`} element={<LobbyPage/>}/>
    <Route path={`${AppRoutes.GAME_SCREEN}/:gameId`} element={<GamePage/>}/>
  </Routes>
}
