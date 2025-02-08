import { FaHome, FaUser } from "react-icons/fa";

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between bg-white px-6 py-4 shadow-md">
      {/* Left Side: Logo */}
      <div className="text-2xl font-bold text-blue-600">TartanAds</div>

      {/* Right Side: Icons */}
      <div className="flex items-center space-x-6">
        <FaHome className="text-gray-600 hover:text-blue-500 cursor-pointer text-2xl" />
        <FaUser className="text-gray-600 hover:text-blue-500 cursor-pointer text-2xl" />
      </div>
    </nav>
  );
};

export default Navbar;