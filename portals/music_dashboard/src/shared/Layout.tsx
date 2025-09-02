import { useContext, useMemo, useState } from "react";
import { Link, Outlet, useNavigate } from "react-router-dom";
import { faMicrophone, faUser } from "@fortawesome/free-solid-svg-icons";

import { ReactComponent as SoundPlaceSVG } from "../assets/soundplace_logo.svg";
import { Action } from "../interfaces";
import { isClubThemeContext, userRoleContext } from "../App";

import IconicDropdown from "./IconicDropdown";
import IconicButton from "./IconicButton";
import Header from "./Header";

const Layout = () => {
  const navigate = useNavigate();
  const { isClubTheme, setIsClubTheme } = useContext(isClubThemeContext);
  const { userRole, setUserRole } = useContext(userRoleContext);
  const [showToggleClub, setShowToggleClub] = useState(false);
  const layoutTheme = useMemo(
    () => ({
      pageBackground: isClubTheme
        ? "bg-contain bg-[url('https://media1.tenor.com/m/YXs_zN1f1QgAAAAC/lights-color.gif')]"
        : "",
      elementBackground: isClubTheme ? "bg-lime-100/25 " : "bg-white/75 z-auto",
      greenTextColor: isClubTheme ? "text-lime-400" : "text-lime-700",
      amberTextColor: isClubTheme ? "text-amber-500" : "text-amber-700/75",
      amberRingColor: isClubTheme ? "ring-amber-500/75" : "ring-amber-700/25",
    }),
    [isClubTheme]
  );

  window.addEventListener(
    "mousemove",
    (e) => {
      const vw = Math.max(
        document.documentElement.clientWidth || 0,
        window.innerWidth || 0
      );
      const cursorPositionOnRightEdge = e.clientX > vw - 50;

      if (!cursorPositionOnRightEdge && showToggleClub) {
        setShowToggleClub(false);
        return;
      }
      if (cursorPositionOnRightEdge && !showToggleClub) {
        setShowToggleClub(true);
        return;
      }
    },
    false
  );
  const profileActions = [
    userRole !== "admin"
      ? { id: "login", label: "Login" }
      : { id: "logout", label: "Logout" },
  ];

  const handleActionTriggered = (event: Action) => {
    event.id === "login" ? navigate("login") : setUserRole("user");
  };

  return (
    <div
      className={`flex justify-center items-center ${layoutTheme.pageBackground}`}
    >
      <div
        className={`flex flex-col justify-center items-center px-[10%] py-[5%] space-y-12 `}
      >
        <div
          className={`sticky top-0 py-3 px-2 flex w-full justify-between items-center z-10 rounded-lg ${layoutTheme.elementBackground}`}
        >
          <Link className="flex items-center" to="/">
            <SoundPlaceSVG className="fill-amber-700/75" width={25} height={25}/>
            <Header
              className={layoutTheme.greenTextColor}
              title="SoundSpot"
              level={2}
            />
          </Link>
          <IconicDropdown
            className={`${layoutTheme.amberTextColor} px-3 py-1 rounded-full ring-1 ${layoutTheme.amberRingColor} hover:bg-slate-50`}
            icon={faUser}
            actions={profileActions}
            handleActionTriggered={handleActionTriggered}
          />
        </div>
        {showToggleClub && (
          <IconicButton
            className={`fixed right-[20px] top-[2px] ${layoutTheme.greenTextColor}`}
            icon={faMicrophone}
            onClick={() => setIsClubTheme(!isClubTheme)}
          />
        )}
        <div className="px-2">
          <Outlet />
        </div>
        {isClubTheme && (
          <>
            <img
              className="fixed top-[2%] left-0 w-full max-w-[20%] lg:max-w-[15%]"
              alt="baby dance"
              src="https://media.tenor.com/Ai1vIx1OJ3AAAAAi/dancing-baby.gif"
            />
            <img
              className="fixed top-[30%] left-[1%] w-full max-w-[15%] lg:max-w-[10%]"
              alt="baby dance"
              src="https://media.tenor.com/cmOW2cG6zVgAAAAj/cat-dancing.gif"
            />
            <img
              className="fixed top-[45%] left-[1%] w-full max-w-[15%] lg:left-[5%]"
              alt="baby dance"
              src="https://media.tenor.com/reHvQm_EdVUAAAAj/thanos-endgame.gif"
            />
            <img
              className="fixed top-[70%] left-[1%] w-full max-w-[15%]"
              alt="baby dance"
              src="https://media.tenor.com/xboU8El2puUAAAAj/alice-sawyer-3d.gif"
            />
            <img
              className="fixed top-[23%] left-[5%] w-full max-w-[5%] lg:left-[13%]"
              alt="baby dance"
              src="https://media.tenor.com/DiT4eAWAyEkAAAAj/dancing-racoon-dancing.gif"
            />
            <img
              className="fixed top-[50px] right-[1%] w-full max-w-[15%]"
              alt="baby dance"
              src="https://media.tenor.com/OmEzUnxv7MsAAAAj/bowser-dance.gif"
            />
            <img
              className="fixed top-[40%] right-[2%] w-full max-w-[10%] lg:right-[8%] lg:top-[35%]"
              alt="baby dance"
              src="https://media.tenor.com/bYv9V464OcUAAAAj/dance-skeleton.gif"
            />

            <img
              className="fixed top-[30%] right-[2%] w-full max-w-[5%]"
              alt="baby dance"
              src="https://media.tenor.com/DiT4eAWAyEkAAAAj/dancing-racoon-dancing.gif"
            />

            <img
              className="fixed top-[55%] right-[2%] w-full max-w-[15%]"
              alt="baby dance"
              src="https://media.tenor.com/yOqgOJDlyzMAAAAi/club-penguin-club.gif"
            />

            <img
              className="fixed top-[70%] right-[2%] w-full max-w-[13%] lg:top-[85%] lg:max-w-[6%] lg:right-[4%]"
              alt="baby dance"
              src="https://media1.tenor.com/m/ETKELYMrCUIAAAAC/cat.gif"
            />
          </>
        )}
      </div>
    </div>
  );
};
export default Layout;
