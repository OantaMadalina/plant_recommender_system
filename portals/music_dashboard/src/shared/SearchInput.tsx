import { useRef, useMemo } from "react";
import { debounce } from "lodash";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

import { SearchInputProps } from "../interfaces";

const SearchInput = ({
  className,
  children,
  onFocus,
  onBlur,
  searchHandler,
}: SearchInputProps) => {
  const searchValue = useRef<HTMLInputElement>(null);

  const debounceSearch = useMemo(
    () => debounce(() => searchHandler(searchValue.current?.value), 1500),
    [searchHandler]
  );

  return (
    <div className={`relative ${className}`}>
      <div onFocus={onFocus} onBlur={onBlur}>
        <input
          ref={searchValue}
          className="rounded-full ring-1 px-2 py-1 w-full ring-lime-500 text-lime-800 focus:ring-lime-600 focus:outline-none"
          type="text"
          placeholder="Search our library"
          onChange={debounceSearch}
        />
        <FontAwesomeIcon
          className="absolute top-2 right-4 text-lime-800"
          icon={faMagnifyingGlass}
        />
      </div>
      {children}
    </div>
  );
};

export default SearchInput;
