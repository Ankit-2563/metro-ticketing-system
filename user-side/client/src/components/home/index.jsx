import React, { useState } from "react";
import { useAuth } from "../../contexts/authContext";
import {
  getDocs,
  query,
  collection,
  where,
  updateDoc,
  doc,
  addDoc,
} from "firebase/firestore";
import { db, serverTimestamp } from "../../firebase/firebase";

const Home = () => {
  const { currentUser } = useAuth();
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");

  const handleAddMoneyClick = () => {
    setShowForm(true);
  };

  const handleAddFaceClick = () => {
    // Open the specified URL in a new tab
    window.open("http://192.168.112.187:5501/server/index.html", "_blank");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (parseInt(amount) < 0) {
        console.error("Amount cannot be negative");
        return; // Prevent form submission if amount is negative
      }

      // Call addAccount with current name and amount
      await addAccount(name, amount);
      // Reset form and hide it
      setName("");
      setAmount("");
      setShowForm(false);
    } catch (error) {
      console.error("Error adding account:", error);
    }
  };

  const addAccount = async (name, amount) => {
    // Check if name and amount are not empty
    if (name.trim() !== "" && amount.trim() !== "") {
      // Query Firestore to check if a document with the same name exists
      const querySnapshot = await getDocs(
        query(collection(db, "accounts"), where("name", "==", name))
      );
      const existingAccount = querySnapshot.docs[0];

      if (existingAccount) {
        // Update existing document with new amount
        const newAmount =
          parseInt(existingAccount.data().amount) + parseInt(amount);
        await updateDoc(doc(db, "accounts", existingAccount.id), {
          amount: newAmount,
          timestamp: serverTimestamp(),
        });
        console.log("Account updated successfully.");

        // Add transaction to transactions collection
        await addTransaction(name, amount, "added money");
      } else {
        // Create a new document
        await addDoc(collection(db, "accounts"), {
          name: name,
          amount: amount,
          timestamp: serverTimestamp(),
        });
        console.log("New account created successfully.");

        // Add transaction to transactions collection
        await addTransaction(name, amount, "added money");
      }

      // Reset form and hide it
      setName("");
      setAmount("");
      setShowForm(false);
    } else {
      console.error("Name and amount cannot be empty");
    }
  };

  const addTransaction = async (name, amount, type) => {
    await addDoc(collection(db, "transactions"), {
      name: name,
      amount: amount,
      timestamp: serverTimestamp(),
      type: type,
    });
    console.log("Transaction added successfully.");
  };

  return (
    <div className="text-2xl font-bold pt-14">
      Hello{" "}
      {currentUser.displayName ? currentUser.displayName : currentUser.email},
      you are now logged in.
      <div className="mt-4">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
          onClick={handleAddMoneyClick}
        >
          Add Money
        </button>
        <button
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleAddFaceClick}
        >
          Add Face
        </button>
      </div>
      {showForm && (
        <form className="mt-4" onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="name"
            >
              Name
            </label>
            <input
              className="shadow appearance-none border rounded w-40 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="name"
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="amount"
            >
              Amount
            </label>
            <input
              className="shadow appearance-none border rounded w-40 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="amount"
              type="number"
              placeholder="Amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </div>
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            type="submit"
          >
            Submit
          </button>
        </form>
      )}
    </div>
  );
};

export default Home;
