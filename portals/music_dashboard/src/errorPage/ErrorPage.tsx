import { Link } from "react-router-dom";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";

import Header from "../shared/Header";
import Button from "../shared/Button";

const ErrorPage = () => {
  return (
    <div className="flex flex-col w-full h-screen justify-center items-center space-y-8">
      <img
        className="max-w-[350px] max-h-[350px]"
        alt="There's nothing here"
        src="https://media.tenor.com/wsobmzpjvugAAAAi/rolling-cat-cat-rolling.gif"
      />
      <div className="flex flex-col space-y-4 items-center">
        <Header className="text-lime-700" title="Oopsie-daisy" level={6} />
        <p className="text-lime-800">Nothing to see here</p>
        <Link to="/">
          <Button
            className="ring-1 ring-lime-600 text-lime-700 hover:bg-slate-50"
            icon={faArrowLeft}
            label="Back to library"
          />
        </Link>
      </div>
    </div>
  );
};

export default ErrorPage;
