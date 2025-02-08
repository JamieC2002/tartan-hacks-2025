import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { FaUser, FaClipboardList, FaKey, FaPlus, FaTrash, FaTimes, FaTag } from "react-icons/fa";
import MainLayout from "../components/MainLayout";
import axios from "axios";
import DatePicker from "react-datepicker";
import { BlobServiceClient } from "@azure/storage-blob";
import "react-datepicker/dist/react-datepicker.css";
import { FaCheckCircle } from "react-icons/fa"; // Import checkmark icon

const CONTAINER_NAME = "tartanads";
const AZURE_STORAGE_ACCOUNT_NAME = "hiloblobstorage";
const SAS_TOKEN = process.env.REACT_APP_AZURE_SAS_TOKEN;

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
  const [trigger, setTrigger] = useState(false);
  const [postings, setPostings] = useState([]);
  const navigate = useNavigate();

  const [fileUploads, setFileUploads] = useState({}); // Stores file per postingId

  const handleFileChange = (postingId) => (e) => {
    const selectedFile = e.target.files[0];
  
    if (selectedFile) {
      const fileType = selectedFile.type.split("/")[0]; // "image" or "video"
      if (fileType === "image" || fileType === "video") {
        setFileUploads((prev) => ({
          ...prev,
          [postingId]: selectedFile, // Store file for specific postingId
        }));
      } else {
        alert("Please upload an image or video file.");
      }
    }
  };

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

  useEffect(() => {
    axios.get(`/postings/?user_id=${id}`)
    .then((response) => {
      console.log("postings stuff = ", response.data);
      setPostings(response.data);
    })
  }, [trigger]);

  const handleOpenCampaignWindow = () => {
    setShowModal(true);
  };


  const handleCreateSubmission = (postingId) => async (e) => {
    e.preventDefault();
  
    const file = fileUploads[postingId]; // Get the file for the specific postingId
  
    if (!file) {
      alert("Please select a file before submitting.");
      return;
    }
  
    try {
      // ✅ Use SAS Token instead of Connection String
      const blobServiceClient = new BlobServiceClient(
        `https://${AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net?${SAS_TOKEN}`
      );
  
      const containerClient = blobServiceClient.getContainerClient(CONTAINER_NAME);
  
      const fileExtension = file.name.split(".").pop();
      const uniqueFileName = `submissions_${postingId}_${Date.now()}.${fileExtension}`;
  
      const blockBlobClient = containerClient.getBlockBlobClient(uniqueFileName);
  
      // Convert File to ArrayBuffer before upload
      const arrayBuffer = await file.arrayBuffer();
  
      await blockBlobClient.uploadData(new Uint8Array(arrayBuffer), {
        blobHTTPHeaders: { blobContentType: file.type },
      });
  
      const fileUrl = `https://${containerClient.accountName}.blob.core.windows.net/${CONTAINER_NAME}/${uniqueFileName}`;
  
      const userData = JSON.parse(localStorage.getItem("user"));
      await axios.post(`/submissions/create/`, {
        poster: postingId,
        submitter: userData.id,
        image: file.type.startsWith("image") ? fileUrl : null,
        video: file.type.startsWith("video") ? fileUrl : null,
        description: "User submitted content",
        qualify: false,
      });
  
      alert("Submission uploaded successfully!");
  
      setFileUploads((prev) => ({
        ...prev,
        [postingId]: null,
      }));
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload submission.");
    }
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

  const handleShowPosting = (postingId) => (e) => {
    e.preventDefault();
    navigate(`/posting/${postingId}/`);
  }

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

      axios.post("/postings/", {
        creator: user["id"],
        title: newCampaign["title"],
        description: newCampaign["description"],
        deadline: newCampaign["deadline"],
        price_per_click: newCampaign["price_per_click"],
        percentage_cut: newCampaign["percentage_cut"],
        keywords: newCampaign["keywords"]
      }).then((response) => {
        console.log("posting create = ", response.data);
        setTrigger(!trigger);
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

  const handleCreateApiKey = async () => {
    try {
      const response = await axios.get(`/users/${id}/api-keys/?creating=true`);
      setApiKeys([...apiKeys, response.data]);
      console.log("response data = ", response.data);
    } catch (error) {
      console.error("Error creating API key:", error);
      alert("Failed to create API key.");
    }
  };
  
  const handleDeleteApiKey = async (apiKey) => {
    try {
      await axios.delete(`/users/${id}/api-keys/?key_id=${apiKey.id}`);
      setApiKeys(apiKeys.filter(key => key !== apiKey)); // Remove from state
    } catch (error) {
      console.error("Error deleting API key:", error);
      alert("Failed to delete API key.");
    }
  };

  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  if (!user) return <div className="flex items-center justify-center h-screen">User not found</div>;

  return (
    <MainLayout>
      <div className="flex min-h-screen bg-gray-100">
        {/* Left Sidebar */}
        <div className="w-1/3 max-w-sm bg-white shadow-md p-6 flex flex-col items-center border-r">
          {(user.user_type === "developer") && 
            <div className="w-48 h-48 rounded-full overflow-hidden">
              <img className="w-full h-full object-cover" src="https://blog.prototion.com/content/images/2021/09/peep-1.png" alt="" />
            </div>
          }
          {(user.user_type === "content_creator") && 
            <div className="w-48 h-48 rounded-full overflow-hidden">
              <img className="w-full h-full object-cover" src="https://cdn.prod.website-files.com/63e37b9e98dcc91a51cc742f/651d72e5fb5e1d60c118fb72_avatar-1200x1200-651d725abb8ef.webp" alt="" />
            </div>
          }
          {(user.user_type === "brand") && 
            <div className="w-48 h-48 rounded-full overflow-hidden">
              <img className="w-full h-full object-cover" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqy4Fe4iQxVay6VCxH8uXEaXUiVAY_wp9lRw&s" alt="" />
            </div>
          }
          <h2 className="mt-4 text-xl font-semibold">{user.username}</h2>
          <p className={`text-lg font-semibold ${
            user.user_type === "content_creator" ? "text-blue-500" :
            user.user_type === "developer" ? "text-green-500" :
            user.user_type === "brand" ? "text-purple-500" :
            "text-gray-600"
          }`}>
            {user.user_type === "content_creator" && "🎥 Content Creator Account"}
            {user.user_type === "developer" && "💻 Developer Account"}
            {user.user_type === "brand" && "🏢 Brand Account"}
          </p>
          {(user.user_type === "developer" || user.user_type === "content_creator") && <h3 className="mt-4 text-xl font-semibold">
            Earnings:
            <span className="ml-2 text-green-600">
              {new Intl.NumberFormat("en-US", { 
                style: "currency", 
                currency: "USD",
                minimumFractionDigits: 4, // Ensures at least 4 decimal places
                maximumFractionDigits: 6  // Allows up to 6 decimal places
              }).format(user.money_earned)}
            </span>
          </h3>}
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
              <div className="flex flex-col gap-2 pl-6 text-gray-700">
              {postings.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {postings.map((posting, index) => (
                    <div key={index} className="bg-white shadow-lg rounded-lg p-6 border border-gray-200 z-50 hover:cursor-pointer"
                      onClick={handleShowPosting(posting.id)}
                    >
                      {/* Title */}
                      <h2 className="text-xl font-bold text-gray-800 mb-2">{posting.title}</h2>

                      {/* Description */}
                      <p className="text-gray-600 mb-3 text-sm">{posting.description}</p>

                      {/* Keywords */}
                      {posting.keywords && posting.keywords.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {posting.keywords.map((keyword, idx) => (
                            <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-600 text-xs font-semibold rounded-md">
                              #{keyword}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Price Per Click & Percentage Cut */}
                      <div className="flex justify-between items-center text-sm text-gray-700 mb-3">
                        <span className="font-semibold">💰 ${posting.price_per_click} / click</span>
                        <span className="font-semibold">✂️ {Math.round(posting.percentage_cut * 100)}% Cut for Creator</span>
                      </div>

                      {/* Deadline */}
                      <p className="text-sm text-gray-500">
                        ⏳ Deadline: <span className="font-medium">{new Date(posting.deadline).toLocaleString()}</span>
                      </p>

                      {/* Status */}
                      <div className="mt-4">
                        <span
                          className={`px-3 py-1 text-xs font-semibold rounded-full ${
                            posting.is_active ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600"
                          }`}
                        >
                          {posting.is_active ? "Active" : "Inactive"}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <h1 className="text-center text-gray-500 text-lg font-semibold">No active campaigns</h1>
              )}
              </div>
            </div>
          )}

          {user.user_type === "content_creator" && (
            <div className="flex flex-col gap-2">
              <div className="flex flex-row gap-2 items-center">
                <h3 className="text-lg font-semibold flex items-center">
                  <FaTag className="mr-2 text-blue-500" /> Available Campaigns
                </h3>
              </div>
              <div className="flex flex-col gap-2 pl-6 text-gray-700">
              {postings.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {postings.map((posting, index) => (
                    <div key={index} className="bg-white shadow-lg rounded-lg p-6 border border-gray-200 z-50 hover:cursor-pointer">
                      {/* Title */}
                      <h2 className="text-xl font-bold text-gray-800 mb-2">{posting.title}</h2>

                      {/* Description */}
                      <p className="text-gray-600 mb-3 text-sm">{posting.description}</p>

                      {/* Keywords */}
                      {posting.keywords && posting.keywords.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {posting.keywords.map((keyword, idx) => (
                            <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-600 text-xs font-semibold rounded-md">
                              #{keyword}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Price Per Click & Percentage Cut */}
                      <div className="flex justify-between items-center text-sm text-gray-700 mb-3">
                        <span className="font-semibold">💰 ${posting.price_per_click} / click</span>
                        <span className="font-semibold">✂️ {Math.round(posting.percentage_cut * 100)}% Cut</span>
                      </div>

                      {/* Deadline */}
                      <p className="text-sm text-gray-500">
                        ⏳ Deadline: <span className="font-medium">{new Date(posting.deadline).toLocaleString()}</span>
                      </p>

                      {/* Status */}
                      <div className="mt-4">
                        <span
                          className={`px-3 py-1 text-xs font-semibold rounded-full ${
                            posting.is_active ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600"
                          }`}
                        >
                          {posting.is_active ? "Active" : "Inactive"}
                        </span>
                      </div>

                      {(!posting.has_submitted) ? <div className="flex flex-col items-center">
                        <div className="flex flex-col items-center">
                          <button
                            onClick={() => document.getElementById(`fileInput-${posting.id}`).click()}
                            className="mt-4 px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:bg-blue-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50"
                          >
                            Upload File
                          </button>

                          <input
                            type="file"
                            id={`fileInput-${posting.id}`}
                            accept="image/*,video/*"
                            className="hidden"
                            onChange={handleFileChange(posting.id)}
                          />

                          {/* File Preview for the specific posting */}
                          {fileUploads[posting.id] && (
                            <div className="mt-4">
                              {fileUploads[posting.id].type.startsWith("image") ? (
                                <img
                                  src={URL.createObjectURL(fileUploads[posting.id])}
                                  alt="Preview"
                                  className="w-64 h-40 object-cover rounded-lg shadow"
                                />
                              ) : (
                                <video controls className="w-64 h-40 rounded-lg shadow">
                                  <source src={URL.createObjectURL(fileUploads[posting.id])} type={fileUploads[posting.id].type} />
                                  Your browser does not support the video tag.
                                </video>
                              )}
                            </div>
                          )}
                        </div>

                        <button
                          onClick={handleCreateSubmission(posting.id)}
                          className="mt-4 px-4 py-2 bg-green-600 text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:bg-green-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50"
                        >
                          Submit
                        </button>
                      </div> : <div className="flex flex-col items-center">
                        <div className="flex flex-row items-center space-x-2 text-green-600 font-semibold text-lg">
                          <FaCheckCircle className="text-2xl" />
                          <span>Submitted!</span>
                        </div>
                      </div>}
                    </div>
                  ))}
                </div>
              ) : (
                <h1 className="text-center text-gray-500 text-lg font-semibold">No active campaigns</h1>
              )}
              </div>
          </div>
          )}

          {user.user_type === "developer" && (
            <div className="flex flex-col gap-2">
              {/* Header and Create API Key Button */}
              <div className="flex flex-row gap-2 items-center">
                <h3 className="text-lg font-semibold flex items-center">
                  <FaKey className="mr-2 text-blue-500" /> Your API Keys
                </h3>
                <button
                  className="flex flex-row items-center px-3 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:bg-blue-700 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50"
                  onClick={handleCreateApiKey}
                >
                  <FaPlus className="mr-1" />
                  <span>Create API Key</span>
                </button>
              </div>

              {/* API Key List */}
              <div className="flex flex-col gap-2 pl-6 text-gray-700">
                {apiKeys.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {apiKeys.map((apiKey, index) => (
                      <div key={index} className="flex items-center justify-between bg-white shadow-lg rounded-lg p-4 border border-gray-200">
                        <span className="text-sm font-mono break-all">{apiKey.value}</span>
                        <button
                          className="ml-2 p-2 bg-red-600 text-white rounded-lg shadow-md transition duration-300 ease-in-out transform hover:bg-red-700 hover:scale-105 focus:outline-none"
                          onClick={() => handleDeleteApiKey(apiKey)}
                        >
                          <FaTrash />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No API keys found.</p>
                )}
              </div>
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