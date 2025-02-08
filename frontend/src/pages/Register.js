import { useState } from "react";
import MainLayout from "../components/MainLayout";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [accountType, setAccountType] = useState("brand"); // brand, content_creator, developer
  const navigate = useNavigate();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("/users/register/", {
      "email": email,
      "password": password,
      "user_type": accountType
    }).then((response) => {
      localStorage.setItem("user", JSON.stringify(response.data));
      navigate(`/profile/${response.data["id"]}`)
    })
  };

  return (
    <MainLayout>
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-md">
          <h2 className="text-center text-2xl font-semibold text-gray-700">Register</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="email"
                className="w-full rounded-md border border-gray-300 px-4 py-2 text-gray-700 focus:border-blue-500 focus:outline-none"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <input
                type="password"
                className="w-full rounded-md border border-gray-300 px-4 py-2 text-gray-700 focus:border-blue-500 focus:outline-none"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div>
              <select
                className="w-full rounded-md border border-gray-300 px-4 py-2 text-gray-700 focus:border-blue-500 focus:outline-none"
                value={accountType}
                onChange={(e) => setAccountType(e.target.value)}
                required
              >
                <option value="brand">Brand</option>
                <option value="content_creator">Content Creator</option>
                <option value="developer">Developer</option>
              </select>
            </div>
            <button
              type="submit"
              className="w-full rounded-md bg-blue-500 px-4 py-2 text-white transition hover:bg-blue-600"
            >
              Register
            </button>
          </form>
        </div>
      </div>
    </MainLayout>
  );
};

export default Register;