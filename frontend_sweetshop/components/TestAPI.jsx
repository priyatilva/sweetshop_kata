import React, { useEffect, useState } from "react";

export default function TestApi() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")  // Backend URL
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage("Could not connect to backend"));
  }, []);

  return (
    <div>
      <h2>Backend says:</h2>
      <p>{message}</p>
    </div>
  );
}
