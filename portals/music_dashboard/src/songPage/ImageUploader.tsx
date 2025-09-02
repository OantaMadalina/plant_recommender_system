import { useState, useEffect } from "react";
import Header from "../shared/Header";
import Loader from "../shared/Loader";
import { ImageUploaderProps } from "../interfaces";

const ImageUploader = ({
  files,
  validationError,
  isImageUploadLoading,
  handleUpload,
}: ImageUploaderProps) => {
  const [width, setWidth] = useState<number>(window.innerWidth);

  function handleWindowSizeChange() {
    setWidth(window.innerWidth);
  }

  useEffect(() => {
    window.addEventListener("resize", handleWindowSizeChange);
    return () => {
      window.removeEventListener("resize", handleWindowSizeChange);
    };
  }, []);

  const isMobile = width <= 768;

  const overwriteDefaults = (e: React.DragEvent | React.ChangeEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const uploadHandler = (e: React.DragEvent | React.ChangeEvent) => {
    overwriteDefaults(e);
    handleUpload && handleUpload(e);
  };

  return (
    <>
      {!isMobile ? (
        <div
          className="flex flex-col justify-center items-center space-y-4 w-full h-44 border-dotted border-2 rounded-lg"
          onDrop={uploadHandler}
          onDragEnter={overwriteDefaults}
          onDragLeave={overwriteDefaults}
          onDragOver={overwriteDefaults}
        >
          <Header
            className="text-lime-700/75"
            level={6}
            title="Drag and Drop Here or"
          />
          <label
            className="cursor-pointer pointer-events-auto rounded-full px-4 py-2 bg-lime-700 text-slate-50 hover:bg-lime-600"
            htmlFor="image-uploader-input"
          >
            Browse
          </label>
          <input
            id="image-uploader-input"
            className="hidden"
            type="file"
            accept="image/png, image/jpeg, image/jpg, image/gif"
            onChange={uploadHandler}
          />
        </div>
      ) : (
        <>
          <label
            className="cursor-pointer pointer-events-auto rounded-full bg-lime-700 text-slate-50 hover:bg-lime-600 w-fit px-2 py-1 self-center" 
            htmlFor="image-uploader-input"
          >
            Browse for your image
          </label>
          <input
            id="image-uploader-input"
            className="hidden"
            type="file"
            accept="image/png, image/gif, image/jpg, image/jpeg"
            onChange={uploadHandler}
          />
        </>
      )}
      {files && files.length > 0 && (
        <div className="max-w-[500px] inline-block break-all">
          <p>Uploaded image:</p>
          <p>{files[0].name}</p>
        </div>
      )}
      {validationError && (
        <span className="max-w-[500px] inline-block break-all">
          {validationError}
        </span>
      )}
      {isImageUploadLoading && (
        <div className="flex space-x-2 items-center">
          <Loader />
          <span>Loading...</span>
        </div>
      )}
    </>
  );
};

export default ImageUploader;
