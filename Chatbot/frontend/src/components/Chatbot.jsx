import React, { useContext, useState } from "react";
import { ChatContext } from "../contexts/ChatContext";
import QueryInput from "./QueryInput";
import QueryHistory from "./QueryHistory";
import Message from "./Message";
import { Grid, Paper, Typography } from "@mui/material";

const Chatbot = () => {
  const { messages, addMessage } = useContext(ChatContext);
  const [loading, setLoading] = useState(false);

  const handleUserQuery = async (query) => {
    addMessage({ text: query, sender: "user" });
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/query", { query });
      const chatbotResponse = response.data.message;
      addMessage({ text: chatbotResponse, sender: "bot" });
    } catch (error) {
      addMessage({ text: "Sorry, something went wrong.", sender: "bot" });
    }

    setLoading(false);
  };

  return (
    <Grid container justifyContent="center" style={{ padding: "20px" }}>
      <Grid item xs={12} sm={8} md={6}>
        <Paper elevation={3} style={{ padding: "20px" }}>
          <Typography variant="h5" gutterBottom>AI Chatbot</Typography>
          <QueryHistory messages={messages} />
          {loading && <Typography>Loading...</Typography>}
          <QueryInput handleUserQuery={handleUserQuery} />
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Chatbot;
