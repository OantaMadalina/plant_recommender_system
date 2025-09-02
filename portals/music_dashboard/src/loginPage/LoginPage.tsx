import { ChangeEvent, FormEvent, useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import TextInput from "../libraryPage/TextInput";
import Header from "../shared/Header";
import Button from "../shared/Button";
import { ReactComponent as SoundPlaceSVG } from "../assets/soundplace_logo.svg";
import { LoginFormState } from "../interfaces";
import { emptyLoginFormState, loginFormFields } from "../constants";
import { userRoleContext } from "../App";

const LoginPage = () => {
  const [loginCredentials, setLoginCredentials] =
    useState<LoginFormState>(emptyLoginFormState);
  const { setUserRole } = useContext(userRoleContext);
  const navigateTo = useNavigate();

  const setFormValue = (e: ChangeEvent) => {
    const fieldName = e.target.id;
    const fieldValue = (e.target as HTMLInputElement).value;

    setLoginCredentials((prevState) => ({
      ...prevState,
      [fieldName]: fieldValue,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (loginCredentials.username === "" || loginCredentials.password === "")
      return;

    const role =
      loginCredentials.username === "admin" &&
      loginCredentials.password === "admin"
        ? "admin"
        : "user";
    setUserRole(role);
    navigateTo("/");
  };
  return (
    <div
      className={`flex flex-col w-fit-content justify-center items-center px-[10%] py-[5%] space-y-12`}
    >
      <Link className="flex items-center" to="/">
        <SoundPlaceSVG className="fill-amber-700/75" width={25} height={25}/>
        <Header className="text-lime-700" title="SoundSpot" level={2} />
      </Link>
      <form className="flex flex-col space-y-6" onSubmit={handleSubmit}>
        <div className="space-y-2">
          {loginFormFields.map((loginFormField) => (
            <TextInput
              fieldName={loginFormField.fieldName}
              label={loginFormField.label}
              type={loginFormField.type}
              value={
                loginCredentials[
                  loginFormField.fieldName as keyof LoginFormState
                ]
              }
              setFormValue={setFormValue}
            />
          ))}
        </div>
        <Button className="bg-lime-700 text-slate-50" label="Login" />
      </form>
    </div>
  );
};

export default LoginPage;
