import React, { useState } from "react";
import { TextField, Button, Grid } from "@mui/material";

const QueryInput = ({ handleUserQuery }) => {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      handleUserQuery(query);
      setQuery("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={10}>
          <TextField
            fullWidth
            label="Ask me something"
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </Grid>
        <Grid item xs={2}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Send
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default QueryInput;
