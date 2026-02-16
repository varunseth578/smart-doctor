import React, { useState } from "react";
import { sendMessage } from "./api";

function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSend = async () => {

    if (!message.trim()) return;

    const userMessage = message;

    setMessage("");       
    setLoading(true);
    setResponse("");

    try {

      const res = await sendMessage(userMessage);

      setResponse(res.response);

    } catch (error) {

      setResponse("Server error");

    }

    setLoading(false);

  };


  return (

    <div style={{ padding: 20 }}>

      <h2>Doctor Appointment Assistant</h2>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "300px", padding: "8px" }}
        placeholder="Type your message"
      />

      <button
        onClick={handleSend}
        disabled={loading}
        style={{ marginLeft: 10, padding: "8px" }}
      >
        {loading ? "Sending..." : "Send"}
      </button>


      {loading && (
        <p style={{ color: "blue" }}>
          Processing... Please wait
        </p>
      )}


      {!loading && response && (
        <p style={{ marginTop: 20 }}>
          {response}
        </p>
      )}

    </div>

  );

}

export default App;
