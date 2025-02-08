import { FaHome, FaUser } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const handleProfileClick = () => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        const user = JSON.parse(storedUser);
        if (user.id) {
          navigate(`/profile/${user.id}/`);
        }
      } catch (error) {
        console.error("Invalid user data in localStorage:", error);
      }
    }
  };

  return (
    <nav className="flex items-center justify-between bg-white px-6 py-4 shadow-md">
      {/* Left Side: Logo */}
      <div className="text-2xl font-bold text-blue-600">TartanAds</div>

      {/* Right Side: Icons */}
      <div className="flex items-center space-x-6">
        <FaHome className="text-gray-600 hover:text-blue-500 cursor-pointer text-2xl"
          onClick={() => {
            navigate("/");
          }}
        />
        <FaUser className="text-gray-600 hover:text-blue-500 cursor-pointer text-2xl"
          onClick={handleProfileClick}
        />
      </div>
    </nav>
  );
};

export default Navbar;