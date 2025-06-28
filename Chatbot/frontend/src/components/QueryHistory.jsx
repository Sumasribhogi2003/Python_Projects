import React from "react";
import { List } from "@mui/material";
import Message from "./Message";

const QueryHistory = ({ messages }) => {
  return (
    <List style={{ maxHeight: "400px", overflowY: "auto" }}>
      {messages.map((msg, index) => (
        <Message key={index} text={msg.text} sender={msg.sender} />
      ))}
    </List>
  );
};

export default QueryHistory;
