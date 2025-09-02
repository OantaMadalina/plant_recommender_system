import React from "react";

interface MessageProps {
  message: string | null;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  if (!message) return null;
  return <p className="message">{message}</p>;
};

export default Message;
