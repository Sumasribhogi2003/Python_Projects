import axios from "axios";

const getChatbotResponse = async (query) => {
  try {
    const response = await axios.post("http://localhost:8000/query", { query });
    return response.data.message;
  } catch (error) {
    console.error("Error fetching chatbot response:", error);
    return "Sorry, something went wrong.";
  }
};
