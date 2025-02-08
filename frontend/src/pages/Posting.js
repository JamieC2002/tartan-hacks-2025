import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import MainLayout from "../components/MainLayout";

const Posting = () => {
  const { id } = useParams();
  const [posting, setPosting] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosting = async () => {
      try {
        const response = await axios.get(`/postings/${id}/`);
        setPosting(response.data);

        if (response.data.submissions) {
          setSubmissions(response.data.submissions);
        }
      } catch (error) {
        console.error("Error fetching posting:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosting();
  }, [id]);

  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  if (!posting) return <div className="flex items-center justify-center h-screen">Posting not found</div>;

  return (
    <MainLayout>
      <div className="flex min-h-screen bg-gray-100 p-8 w-full">
        {/* Left Side: Posting Details */}
        <div className="w-1/3 bg-white shadow-lg rounded-lg p-6 border border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">{posting.title}</h2>
          <p className="text-gray-600 mb-4">{posting.description}</p>

          {/* Keywords */}
          {posting.keywords.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {posting.keywords.map((keyword, idx) => (
                <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-600 text-xs font-semibold rounded-md">
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
        </div>

        {/* Right Side: Submissions Section (Scrollable) */}
        <div className="w-full ml-8 bg-white shadow-lg rounded-lg p-6 border border-gray-200 overflow-y-auto max-h-screen">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Submissions</h3>

          {submissions.length > 0 ? (
            <div className="space-y-4">
              {submissions.map((submission, index) => (
                <div key={index} className="bg-gray-100 p-4 rounded-lg shadow">
                  {/* Submitter */}
                  <p className="text-sm text-gray-700 mb-2">
                    Submitted by: <span className="font-semibold">{submission.submitter}</span>
                  </p>

                  {/* Image or Video */}
                  {submission.image ? (
                    <img
                      src={submission.image}
                      alt="Submission"
                      className="w-full h-48 object-cover rounded-lg mb-2"
                    />
                  ) : submission.video ? (
                    <video controls className="w-full h-48 rounded-lg mb-2">
                      <source src={submission.video} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  ) : null}

                  {/* Description */}
                  <p className="text-gray-600 text-sm mb-2">{submission.description}</p>

                  {/* Keywords */}
                  {submission.keywords.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-2">
                      {submission.keywords.map((keyword, idx) => (
                        <span key={idx} className="px-2 py-1 bg-green-100 text-green-600 text-xs font-semibold rounded-md">
                          #{keyword}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Qualification Status */}
                  <p className={`text-sm font-semibold ${submission.qualify ? "text-green-600" : "text-red-600"}`}>
                    {submission.qualify ? "✅ Qualified" : "❌ Not Qualified"}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center">No submissions yet.</p>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default Posting;