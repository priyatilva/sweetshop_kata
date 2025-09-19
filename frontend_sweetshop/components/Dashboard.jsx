import React, { useEffect, useState } from "react";

export default function Dashboard({ token, isAdmin }) {
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSweets = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/sweets", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) {
          const err = await res.json();
          setError(err.detail || "Failed to fetch sweets");
          setLoading(false);
          return;
        }
        const data = await res.json();
        setSweets(data);
      } catch (err) {
        setError("Network error, please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchSweets();
  }, [token]);

  if (loading) return <p>Loading sweets...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="dashboard">
      <h2>{isAdmin ? "Admin Dashboard" : "User Dashboard"}</h2>
      <div className="sweet-list">
        {sweets.map((sweet) => (
          <div key={sweet.id} className="sweet-card">
            <img
              src={`/images/${sweet.name.toLowerCase()}.jpeg`}
              alt={sweet.name}
              className="sweet-img"
              onError={(e) => (e.target.src = "/images/default.jpeg")}
            />
            <h3>{sweet.name}</h3>
            <p>{sweet.category} | INR{sweet.price} | Qty: {sweet.quantity}</p>

            {!isAdmin ? (
              <button
                disabled={sweet.quantity === 0}
                className="btn-primary"
              >
                Purchase
              </button>
            ) : (
              <div className="admin-actions">
                <button className="btn-secondary">Update</button>
                <button className="btn-danger">Delete</button>
                <button className="btn-primary">Restock</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
