import React, { useState } from "react";
import { sendMessage } from "./api";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    const res = await sendMessage(message);
    setResponse(res.response);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Doctor Appointment Assistant</h2>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "300px" }}
      />
      <button onClick={handleSend}>Send</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
