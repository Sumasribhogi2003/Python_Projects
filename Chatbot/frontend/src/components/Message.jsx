import React from "react";
import { ListItem, ListItemText } from "@mui/material";

const Message = ({ text, sender }) => {
  return (
    <ListItem style={{ justifyContent: sender === "user" ? "flex-end" : "flex-start" }}>
      <ListItemText
        primary={text}
        style={{ backgroundColor: sender === "user" ? "#e0f7fa" : "#f1f1f1", padding: "10px", borderRadius: "5px" }}
      />
    </ListItem>
  );
};

export default Message;
