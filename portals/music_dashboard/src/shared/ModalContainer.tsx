import { LayoutProps } from "../interfaces";

const ModalContainer = ({ children }: LayoutProps) => {
  return (
    <div className="fixed top-0 left-0 w-screen h-screen bg-amber-600/25">
      <div className="absolute left-[50%] top-[50%] -translate-x-1/2 -translate-y-1/2 bg-white py-8 px-6 rounded-lg space-y-4 w-full lg:w-fit">
        {children}
      </div>
    </div>
  );
};

export default ModalContainer;
