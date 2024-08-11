import React, { useState } from "react";
import { motion } from "framer-motion";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [mp3File, setMp3File] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePdfUpload = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleConvert = async () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setMp3File("sample.mp3"); // Placeholder for now
    }, 3000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <motion.div
        className="bg-white p-8 rounded-lg shadow-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <h1 className="text-2xl font-bold mb-6">PDF to MP3 Converter</h1>
        <input
          type="file"
          accept="application/pdf"
          onChange={handlePdfUpload}
          className="mb-4"
        />
        <button
          onClick={handleConvert}
          className={`py-2 px-4 rounded-lg text-white ${
            pdfFile
              ? "bg-blue-500 hover:bg-blue-700"
              : "bg-gray-500 cursor-not-allowed"
          }`}
          disabled={!pdfFile || loading}
        >
          {loading ? "Converting..." : "Convert to MP3"}
        </button>
        {mp3File && (
          <motion.a
            href={mp3File}
            download
            className="mt-4 block text-blue-500 hover:text-blue-700"
            initial={{ x: -100 }}
            animate={{ x: 0 }}
            transition={{ type: "spring", stiffness: 50 }}
          >
            Download MP3
          </motion.a>
        )}
      </motion.div>
    </div>
  );
}

export default App;
