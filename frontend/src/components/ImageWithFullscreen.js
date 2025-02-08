import { useState } from "react";

export default function ImageWithFullscreen({ submission }) {
  const [isFullscreen, setIsFullscreen] = useState(false);

  return (
    <>
      {/* Image container with black bars for aspect ratio */}
      <div
        className="w-full h-48 overflow-hidden rounded-lg bg-black flex items-center justify-center cursor-pointer"
        onClick={() => setIsFullscreen(true)}
      >
        <img
          src={submission.image}
          alt="Submission"
          className="max-w-full max-h-full object-contain rounded-lg"
        />
      </div>

      {/* Fullscreen Modal */}
      {isFullscreen && (
        <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-90 flex items-center justify-center z-50">
          <button
            className="absolute top-5 right-5 text-white text-3xl font-bold bg-gray-800 p-3 rounded-full hover:bg-gray-600"
            onClick={() => setIsFullscreen(false)}
          >
            ✕
          </button>
          <img
            src={submission.image}
            alt="Fullscreen Submission"
            className="w-auto h-auto max-w-screen max-h-screen object-contain"
          />
        </div>
      )}
    </>
  );
}