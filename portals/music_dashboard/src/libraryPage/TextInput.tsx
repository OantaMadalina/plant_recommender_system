import { TextInputProps } from "../interfaces";

const TextInput = ({
  className,
  fieldName,
  placeholder,
  value,
  label,
  type,
  readOnly,
  disabled,
  setFormValue,
}: TextInputProps) => {
  return (
    <div className={className}>
      <label className="text-lime-800" htmlFor={fieldName}>{label}</label>
      <input
        className="w-full rounded-full px-2 py-1 ring-1 ring-lime-500 text-lime-800 focus:ring-lime-600 focus:outline-none"
        type={type ?? "text"}
        id={fieldName}
        placeholder={placeholder ?? ""}
        value={value}
        onChange={setFormValue}
        readOnly={readOnly ?? false}
        disabled={disabled ?? false}
      />
    </div>
  );
};

export default TextInput;
