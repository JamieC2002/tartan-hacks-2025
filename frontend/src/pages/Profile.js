import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FaUser, FaClipboardList, FaKey, FaPlus, FaTrash, FaTimes } from "react-icons/fa";
import MainLayout from "../components/MainLayout";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Profile = () => {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [apiKeys, setApiKeys] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newCampaign, setNewCampaign] = useState({
    title: "",
    description: "",
    deadline: new Date(),
    price_per_click: "",
    percentage_cut: "",
    keywords: [],
    keywordInput: "",
  });

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get(`/users/${id}/profile/`);
        setUser(response.data);
        if (response.data.user_type === "developer") {
          setApiKeys(response.data.api_keys || []);
        }
      } catch (error) {
        console.error("Error fetching user:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, [id]);

  const handleOpenCampaignWindow = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setNewCampaign({
      title: "",
      description: "",
      deadline: new Date(),
      price_per_click: "",
      percentage_cut: "",
      keywords: [],
      keywordInput: "",
    });
  };

  const handleInputChange = (e) => {
    setNewCampaign({ ...newCampaign, [e.target.name]: e.target.value });
  };

  const handleKeywordInput = (e) => {
    if (e.key === "Enter" && newCampaign.keywordInput.trim() !== "") {
      setNewCampaign({
        ...newCampaign,
        keywords: [...newCampaign.keywords, newCampaign.keywordInput.trim()],
        keywordInput: "",
      });
      e.preventDefault();
    }
  };

  const handleCreateCampaign = (e) => {
    e.preventDefault();
    const userData = localStorage.getItem('user');

    try {
      if (!userData) {
        throw new Error("No user data found in localStorage.");
      }
      const user = JSON.parse(userData);
    
      if (!user.id) {
        throw new Error("User ID is missing from stored user data.");
      }

      console.log("userData:", userData);

      axios.post("/postings/", {
        creator: userData["id"],
        title: newCampaign["title"],
        description: newCampaign["description"],
        deadline: newCampaign["deadline"],
        price_per_click: newCampaign["price_per_click"],
        percentage_cut: newCampaign["percentage_cut"],
        keywords: newCampaign["keywords"]
      }).then((response) => {
        console.log("posting create = ", response.data);
      })
    } catch (error) {
      alert(error.message);
    }
  }

  const handleRemoveKeyword = (keyword) => {
    setNewCampaign({
      ...newCampaign,
      keywords: newCampaign.keywords.filter((k) => k !== keyword),
    });
  };

  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  if (!user) return <div className="flex items-center justify-center h-screen">User not found</div>;

  return (
    <MainLayout>
      <div className="flex min-h-screen bg-gray-100">
        {/* Left Sidebar */}
        <div className="w-1/3 max-w-sm bg-white shadow-md p-6 flex flex-col items-center border-r">
          <FaUser className="text-gray-500 text-6xl" />
          <h2 className="mt-4 text-xl font-semibold">{user.username}</h2>
          <p className="text-gray-600">{user.user_type} Account</p>
        </div>

        {/* Right Content Section */}
        <div className="flex-1 p-8">
          {user.user_type === "brand" && (
            <div className="flex flex-col gap-2">
              <div className="flex flex-row gap-2 items-center">
                <h3 className="text-lg font-semibold flex items-center">
                  <FaClipboardList className="mr-2 text-blue-500" /> Your Ad Campaigns
                </h3>
                <button
                  className="px-3 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:bg-blue-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50"
                  onClick={handleOpenCampaignWindow}
                >
                  Create a Campaign
                </button>
              </div>
              <ul className="list-disc pl-6 text-gray-700">
                {user.campaigns?.length > 0 ? (
                  user.campaigns.map((campaign, index) => <li key={index}>{campaign}</li>)
                ) : (
                  <h1>No active campaigns</h1>
                )}
              </ul>
            </div>
          )}

          {/* Modal for Creating a Campaign */}
          {showModal && (
            <div className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm flex justify-center items-center z-50">
              <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full relative">
                <button
                  className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
                  onClick={handleCloseModal}
                >
                  <FaTimes size={20} />
                </button>
                <h2 className="text-xl font-semibold mb-4">Create Ad Campaign</h2>

                <input
                  type="text"
                  name="title"
                  placeholder="Title"
                  value={newCampaign.title}
                  onChange={handleInputChange}
                  className="w-full mb-2 px-3 py-2 border rounded"
                />
                <textarea
                  name="description"
                  placeholder="Description"
                  value={newCampaign.description}
                  onChange={handleInputChange}
                  className="w-full mb-2 px-3 py-2 border rounded"
                />
                <DatePicker
                  selected={newCampaign.deadline}
                  onChange={(date) => setNewCampaign({ ...newCampaign, deadline: date })}
                  showTimeSelect
                  dateFormat="Pp"
                  className="w-full mb-2 px-3 py-2 border rounded"
                />
                <input
                  type="number"
                  name="price_per_click"
                  placeholder="Price per click ($0.0000 - $99.9999)"
                  value={newCampaign.price_per_click}
                  onChange={handleInputChange}
                  className="w-full mb-2 px-3 py-2 border rounded"
                />
                <input
                  type="number"
                  name="percentage_cut"
                  step="0.01" // Allows decimal input
                  placeholder="Percentage cut (0.00 - 1.00)"
                  value={newCampaign.percentage_cut}
                  onChange={handleInputChange}
                  className="w-full mb-2 px-3 py-2 border rounded"
                />

                {/* Keyword Input */}
                <div className="mb-2">
                  <input
                    type="text"
                    name="keywordInput"
                    placeholder="Add keywords (press Enter)"
                    value={newCampaign.keywordInput}
                    onChange={(e) => setNewCampaign({ ...newCampaign, keywordInput: e.target.value })}
                    onKeyDown={handleKeywordInput}
                    className="w-full px-3 py-2 border rounded"
                  />
                  <div className="flex flex-wrap mt-2">
                    {newCampaign.keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="m-1 px-3 py-1 bg-blue-500 text-white rounded-full flex items-center"
                      >
                        {keyword}
                        <button onClick={() => handleRemoveKeyword(keyword)} className="ml-2 text-sm">
                          ✕
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <button className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
                  onClick={handleCreateCampaign}
                >
                  Submit Campaign
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default Profile;