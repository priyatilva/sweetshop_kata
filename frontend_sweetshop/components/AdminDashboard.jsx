import React, { useEffect, useState } from "react";

function AdminDashboard({ token }) {
  const [sweets, setSweets] = useState([]);
  const [newSweet, setNewSweet] = useState({ name: "", category: "", price: 0, quantity: 0 });
  const [message, setMessage] = useState("");

  const fetchSweets = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/sweets", {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    setSweets(data);
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  const addSweet = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/sweets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(newSweet),
    });
    if (response.ok) {
      setMessage("Sweet added successfully!");
      setNewSweet({ name: "", category: "", price: 0, quantity: 0 });
      fetchSweets();
    } else {
      setMessage("Failed to add sweet");
    }
  };

  const deleteSweet = async (id) => {
    const response = await fetch(`http://127.0.0.1:8000/api/sweets/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      setMessage("Sweet deleted!");
      fetchSweets();
    } else {
      setMessage("Failed to delete");
    }
  };

  const restockSweet = async (id) => {
    const response = await fetch(`http://127.0.0.1:8000/api/sweets/${id}/restock`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      setMessage("Sweet restocked!");
      fetchSweets();
    } else {
      setMessage("Failed to restock");
    }
  };

  return (
    <div>
      <h2>? Admin Dashboard</h2>
      {message && <p style={{ color: "green" }}>{message}</p>}

      {/* Add Sweet Form */}
      <div style={{ marginBottom: "20px" }}>
        <h3>Add New Sweet</h3>
        <input
          type="text"
          placeholder="Name"
          value={newSweet.name}
          onChange={(e) => setNewSweet({ ...newSweet, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Category"
          value={newSweet.category}
          onChange={(e) => setNewSweet({ ...newSweet, category: e.target.value })}
        />
        <input
          type="number"
          placeholder="Price"
          value={newSweet.price}
          onChange={(e) => setNewSweet({ ...newSweet, price: Number(e.target.value) })}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={newSweet.quantity}
          onChange={(e) => setNewSweet({ ...newSweet, quantity: Number(e.target.value) })}
        />
        <button onClick={addSweet}>Add Sweet</button>
      </div>

      {/* Sweet List */}
      <h3>All Sweets</h3>
      <ul>
        {sweets.map((sweet) => (
          <li key={sweet.id}>
            {sweet.name} ({sweet.category}) - INR{sweet.price} | Qty: {sweet.quantity}
            <button onClick={() => deleteSweet(sweet.id)}>? Delete</button>
            <button onClick={() => restockSweet(sweet.id)}>? Restock</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
