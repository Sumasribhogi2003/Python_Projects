import React from "react";
import { ChatProvider } from "./contexts/ChatContext";
import Chatbot from "./components/Chatbot";

const App = () => {
  return (
    <ChatProvider>
      <Chatbot />
    </ChatProvider>
  );
};

export default App;
