import React, { useEffect, useState } from "react";
import RegistrationForm from "./components/RegistrationForm";
import LoginForm from "./components/LoginForm";
import Dashboard from "./components/Dashboard";
import AdminDashboard from "./components/AdminDashboard";

function App() {
  const [backendMessage, setBackendMessage] = useState("");
  const [userToken, setUserToken] = useState(null);
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((data) => setBackendMessage(data.message))
      .catch(() => setBackendMessage("Could not connect to backend"));
  }, []);

  return (
    <div className="App">
      <h1>Sweetshop</h1>
      <p>{backendMessage}</p>

      {!userToken ? (
        <div style={{ display: "flex", gap: "20px" }}>
          <RegistrationForm />
          <LoginForm setUserToken={setUserToken} setUserInfo={setUserInfo} />
        </div>
      ) : userInfo?.is_admin ? (
        <AdminDashboard token={userToken} />
      ) : (
        <Dashboard token={userToken} />
      )}
    </div>
  );
}

export default App;
