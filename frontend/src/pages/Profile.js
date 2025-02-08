import { useState } from "react";
import { FaUser, FaClipboardList, FaKey, FaPlus, FaTrash } from "react-icons/fa";
import MainLayout from "../components/MainLayout";

const Profile = () => {
  const [accountType, setAccountType] = useState("Brand"); // Change to "Content Creator" or "Developer" to test
  const [apiKeys, setApiKeys] = useState(["API_KEY_12345", "API_KEY_67890"]); // Example API keys

  const handleAddApiKey = () => {
    const newKey = `API_KEY_${Math.floor(Math.random() * 100000)}`;
    setApiKeys([...apiKeys, newKey]);
  };

  const handleDeleteApiKey = (key) => {
    setApiKeys(apiKeys.filter((k) => k !== key));
  };

  return (
    <MainLayout>
      <div className="flex min-h-screen bg-gray-100">
        {/* Left Sidebar */}
        <div className="w-1/3 max-w-sm bg-white shadow-md p-6 flex flex-col items-center border-r">
          <FaUser className="text-gray-500 text-6xl" />
          <h2 className="mt-4 text-xl font-semibold">John Doe</h2>
          <p className="text-gray-600">{accountType} Account</p>
        </div>

        {/* Right Content Section */}
        <div className="flex-1 p-8">
          {accountType === "Brand" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <FaClipboardList className="mr-2 text-blue-500" /> Your Ad Campaigns
              </h3>
              <ul className="list-disc pl-6 text-gray-700">
                <li>Campaign 1 - Running</li>
                <li>Campaign 2 - Pending Review</li>
                <li>Campaign 3 - Completed</li>
              </ul>
            </div>
          )}

          {accountType === "Content Creator" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <FaClipboardList className="mr-2 text-green-500" /> Your Submissions
              </h3>
              <ul className="list-disc pl-6 text-gray-700">
                <li>Submission 1 - Approved</li>
                <li>Submission 2 - Under Review</li>
                <li>Submission 3 - Rejected</li>
              </ul>
            </div>
          )}

          {accountType === "Developer" && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <FaKey className="mr-2 text-red-500" /> API Keys Management
              </h3>
              <button
                onClick={handleAddApiKey}
                className="flex items-center bg-blue-500 text-white px-4 py-2 rounded-md mb-4 hover:bg-blue-600 transition"
              >
                <FaPlus className="mr-2" /> Generate New Key
              </button>
              <ul className="text-gray-700">
                {apiKeys.map((key, index) => (
                  <li key={index} className="flex justify-between bg-gray-100 p-2 rounded-md my-2">
                    <span>{key}</span>
                    <button onClick={() => handleDeleteApiKey(key)} className="text-red-500 hover:text-red-700">
                      <FaTrash />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default Profile;