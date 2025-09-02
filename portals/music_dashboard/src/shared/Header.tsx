import { HeaderProps } from "../interfaces";

const Header = ({ title, level, className }: HeaderProps) => {
  const Header = (
    level >= 1 && level <= 6 ? `h${level}` : "h2"
  ) as keyof JSX.IntrinsicElements;
  return <Header className={`text-3xl font-bold ${className}`}>{title}</Header>;
};
export default Header;
